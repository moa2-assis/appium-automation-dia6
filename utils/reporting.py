import os
import json
import webbrowser
from pathlib import Path
from datetime import datetime

_REPORTS = []
_REPORT_INDEX = {}
_SESSION_START = datetime.now()

def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)

def html_escape(s: str) -> str:
    if s is None:
        return ""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def _read_session_meta(dir_path: Path):
    p = Path(dir_path) / "session_meta.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def upsert_result(item, rep, order=None, test_dirname=None) -> None:
    nodeid = item.nodeid
    payload = {
        "nodeid": nodeid,
        "name": item.name,
        "when": getattr(rep, "when", "call"),
        "outcome": rep.outcome,
        "duration": getattr(rep, "duration", None),
        "error": rep.longreprtext if rep.failed else "",
    }
    if order is not None:
        payload["order"] = order
    if test_dirname:
        payload["dir"] = test_dirname

    idx = _REPORT_INDEX.get(nodeid)
    if idx is not None:
        _REPORTS[idx].update(payload)
    else:
        _REPORT_INDEX[nodeid] = len(_REPORTS)
        _REPORTS.append(payload)

def add_screenshot(item, rel_path: str) -> None:
    idx = _REPORT_INDEX.get(item.nodeid)
    if idx is not None:
        _REPORTS[idx]["screenshot"] = rel_path

def add_video(item, rel_path: str) -> None:
    idx = _REPORT_INDEX.get(item.nodeid)
    if idx is not None:
        _REPORTS[idx]["video"] = rel_path

# CSS e JS do dashboard omitidos por brevidade
_DARK_CSS = """..."""
_DARK_JS = """..."""

def _build_dashboard_html(session_dir_name: str, dir_path: Path) -> str:
    total = len(_REPORTS)
    failed = sum(1 for r in _REPORTS if r["outcome"] == "failed")
    passed = sum(1 for r in _REPORTS if r["outcome"] == "passed")
    skipped = sum(1 for r in _REPORTS if r["outcome"] == "skipped")

    def pct(x): return (x / total * 100) if total else 0

    rows = []
    for r in sorted(_REPORTS, key=lambda x: x.get("order", 999999)):
        cls = {"failed": "fail", "passed": "pass", "skipped": "skip"}.get(r["outcome"], "")
        err = html_escape((r.get("error") or "")[:2000])
        dur = f"{r.get('duration', 0):.2f}s" if r.get("duration") else ""
        files = " | ".join([x for x in [
            f"📸 <a href='{r.get('screenshot')}'>screenshot</a>" if r.get("screenshot") else "",
            f"🎥 <a href='{r.get('video')}'>video</a>" if r.get("video") else ""
        ] if x])
        rows.append(
            f"<tr class='{cls}'><td>{r.get('order','')}</td><td>{html_escape(r['name'])}</td>"
            f"<td>{html_escape(r.get('when',''))}</td><td>{html_escape(r['outcome'])}</td>"
            f"<td>{dur}</td><td>{files}</td><td><pre>{err}</pre></td></tr>"
        )

    caps = _read_session_meta(dir_path).get("capabilities", {})
    env_html = ""
    if caps:
        env_html = (
            f"<div class='card'><b>Environment</b><br>"
            f"deviceName: {html_escape(str(caps.get('appium:deviceName', '')))} | "
            f"platform: {html_escape(str(caps.get('platformName', '')))} | "
            f"appPackage: {html_escape(str(caps.get('appium:appPackage', '')))}</div>"
        )

    return f"""<!doctype html>
<html><head><meta charset='utf-8'><title>Test Dashboard</title>
<style>{_DARK_CSS}</style><script>{_DARK_JS}</script></head>
<body><h1>Test Dashboard</h1>{env_html}
<table><thead><tr><th>Order</th><th>Test</th><th>When</th><th>Outcome</th><th>Duration</th><th>Artifacts</th><th>Error</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></body></html>"""

def write_dashboard(output_dir: Path) -> Path:
    """Gera o dashboard.html sem abrir o navegador."""
    ensure_dir(str(output_dir))
    path = Path(output_dir) / "dashboard.html"
    html = _build_dashboard_html(Path(output_dir).name, output_dir)
    path.write_text(html, encoding="utf-8")
    print(f"\nDashboard written to {path}")
    return path

def write_and_open_dashboard(output_dir: Path) -> None:
    """Gera o dashboard.html e abre no navegador."""
    path = write_dashboard(output_dir)
    if not os.environ.get("CI"):
        try:
            webbrowser.open(path.resolve().as_uri())
        except Exception:
            pass

def write_session_summary(output_dir: Path, exitstatus: int) -> None:
    ensure_dir(str(output_dir))
    total = len(_REPORTS)
    failed = sum(1 for r in _REPORTS if r["outcome"] == "failed")
    passed = sum(1 for r in _REPORTS if r["outcome"] == "passed")
    skipped = sum(1 for r in _REPORTS if r["outcome"] == "skipped")
    finished = datetime.now()

    payload = {
        "session_info": {
            "timestamp": Path(output_dir).name,
            "started_at": _SESSION_START.strftime("%Y-%m-%d %H:%M:%S"),
            "finished_at": finished.strftime("%Y-%m-%d %H:%M:%S"),
            "pytest_exitstatus": exitstatus,
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped
        },
        "tests": _REPORTS
    }

    (Path(output_dir) / "session_summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")