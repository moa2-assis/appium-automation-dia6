# utils/reporting.py
import os
import base64
import webbrowser
from typing import Optional
from pathlib import Path
from datetime import datetime

# ====== estado do relatório ======
_REPORTS = []            # list[dict]
_REPORT_INDEX = {}       # nodeid -> index
_SESSION_START = datetime.now()

# ====== helpers básicos ======
def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)

def html_escape(s: str) -> str:
    if s is None:
        return ""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def test_failed(request) -> bool:
    rep = getattr(request.node, "rep_call", None)
    return bool(rep and rep.failed)

def _fmt_hms(seconds: float) -> str:
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

# ====== artefatos ======
def save_screenshot(driver, item) -> str:
    ensure_dir("screenshots")
    name = f"screenshots/{timestamp()}_screenshot_{item.name}.png"
    driver.get_screenshot_as_file(name)
    print(f"Screenshot saved as {name}")
    return name

def save_video_from_driver(driver, test_name: str) -> Optional[str]:
    data = driver.stop_recording_screen()
    if not data:
        return None
    ensure_dir("videos")
    name = f"videos/{timestamp()}_video_{test_name}.mp4"
    with open(name, "wb") as f:
        f.write(base64.b64decode(data))
    print(f"Video saved as {name}")
    return name

# ====== coleta ======
def attach_phase_report(item, rep):
    """Guarda rep_setup/rep_call/rep_teardown no próprio item para consulta no teardown."""
    setattr(item, f"rep_{rep.when}", rep)

def upsert_result(item, rep):
    """Cria/atualiza registro do teste no _REPORTS durante a fase 'call'."""
    if rep.when != "call":
        return
    nodeid = item.nodeid
    payload = {
        "nodeid": nodeid,
        "name": item.name,
        "outcome": rep.outcome,   # "passed"/"failed"/"skipped"
        "duration": getattr(rep, "duration", None),
        "error": rep.longreprtext if rep.failed else "",
        "screenshot": "",
        "video": "",
    }
    if nodeid in _REPORT_INDEX:
        idx = _REPORT_INDEX[nodeid]
        _REPORTS[idx].update(payload)
    else:
        _REPORT_INDEX[nodeid] = len(_REPORTS)
        _REPORTS.append(payload)

def add_screenshot(item, path: str):
    idx = _REPORT_INDEX.get(item.nodeid)
    if idx is not None:
        _REPORTS[idx]["screenshot"] = path

def add_video(item, path: Optional[str]):
    if not path:
        return
    idx = _REPORT_INDEX.get(item.nodeid)
    if idx is not None:
        _REPORTS[idx]["video"] = path

# ====== dashboard (dark mode) ======
_DARK_CSS = """
body { background:#121212; color:#E0E0E0; font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin:16px; }
.wrap { max-width:none; margin:0; }  /* ocupar toda a largura da janela */
h1 { margin:0 0 8px; color:#FAFAFA; }
.meta { color:#9AA0A6; margin-bottom:12px; }
.card { background:#1E1E1E; border:1px solid #2A2A2A; border-radius:12px; padding:16px; box-shadow: 0 8px 24px rgba(0,0,0,0.35); }
.row { display:flex; gap:12px; flex-wrap:wrap; align-items:center; }
.badge { display:inline-flex; align-items:center; gap:6px; padding:6px 10px; border-radius:999px; font-weight:600; font-size:14px; }
.badge.pass { background:linear-gradient(180deg,#1B5E20,#153F17); color:#C8E6C9; border:1px solid #2E7D32; }
.badge.fail { background:linear-gradient(180deg,#7F1D1D,#4A1212); color:#FFCDD2; border:1px solid #B71C1C; }
.badge.skip { background:linear-gradient(180deg,#37474F,#222C31); color:#CFD8DC; border:1px solid #455A64; }
.badge.tot  { background:linear-gradient(180deg,#263238,#1A2327); color:#ECEFF1; border:1px solid #37474F; }
.controls { position:sticky; top:0; z-index:2; margin:16px 0; padding:10px; background:rgba(18,18,18,0.85); backdrop-filter:saturate(160%) blur(8px); border:1px solid #2A2A2A; border-radius:12px; }
button { background:#2C2C2C; color:#E0E0E0; border:1px solid #3A3A3A; padding:8px 12px; border-radius:10px; cursor:pointer; transition:all .2s ease; }
button:hover { transform:translateY(-1px); background:#353535; }
button.active { border-color:#64B5F6; box-shadow:0 0 0 3px rgba(100,181,246,.15); }

.table-wrap { border-radius:12px; border:1px solid #2A2A2A; }
table { width:100%; border-collapse:collapse; }  /* agora ocupa toda a largura */
th, td { border-bottom:1px solid #2A2A2A; padding:10px 12px; vertical-align: top; }
th { background:#1A1A1A; text-align:left; position:sticky; top:0; z-index:1; }
tbody tr { transition: background .2s ease; }
tbody tr:hover { background:#1A1A1A; }
tr.pass { background:#142016; }
tr.fail { background:#2A1414; }
tr.skip { background:#1A2125; }
.center { text-align:center; }

/* evitar scroll horizontal */
td, th { white-space: normal; word-break: break-word; overflow-wrap: anywhere; }

pre { margin:0; white-space:pre-wrap; word-wrap:break-word; overflow-wrap:anywhere; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "JetBrains Mono", monospace; font-size: 12px; line-height: 1.4; color:#E6E6E6; }
a { color:#80CBC4; }
.progress { display:flex; height:10px; border-radius:999px; overflow:hidden; border:1px solid #2A2A2A; background:#1A1A1A; }
.bar.pass { background:#4CAF50; }
.bar.fail { background:#EF5350; }
.bar.skip { background:#9E9E9E; }
"""

_DARK_JS = """
function filterRows(mode) {
  const rows = document.querySelectorAll('tbody tr');
  const btns = document.querySelectorAll('.controls button');
  btns.forEach(b => b.classList.remove('active'));
  document.querySelector(`[data-mode="${mode}"]`).classList.add('active');
  rows.forEach(r => {
    const isFail = r.classList.contains('fail');
    const isPass = r.classList.contains('pass');
    const isSkip = r.classList.contains('skip');
    r.style.display =
      mode === 'all' ? '' :
      mode === 'fail' ? (isFail ? '' : 'none') :
      mode === 'pass' ? (isPass ? '' : 'none') :
      mode === 'skip' ? (isSkip ? '' : 'none') : '';
  });
}
"""

def _build_dashboard_html() -> str:
    total = len(_REPORTS)
    failed = sum(1 for r in _REPORTS if r["outcome"] == "failed")
    passed = sum(1 for r in _REPORTS if r["outcome"] == "passed")
    skipped = sum(1 for r in _REPORTS if r["outcome"] == "skipped")

    # barras de progresso proporcionais
    def pct(x: int) -> float:
        return (x / total * 100.0) if total else 0.0

    rows = []
    for r in _REPORTS:
        outcome = r["outcome"]
        cls = {"failed": "fail", "passed": "pass", "skipped": "skip"}.get(outcome, "")
        err = html_escape((r.get("error") or "")[:2000])  # trunc
        shot = r.get("screenshot") or ""
        vid = r.get("video") or ""
        files = " | ".join([x for x in [
            f'📸 <a href="{shot}">screenshot</a>' if shot else "",
            f'🎥 <a href="{vid}">video</a>' if vid else ""
        ] if x])
        dur = f'{r.get("duration"):.2f}s' if r.get("duration") else ""
        rows.append(
            f"<tr class='{cls}'>"
            f"<td>{html_escape(r['name'])}</td>"
            f"<td>{html_escape(r['nodeid'])}</td>"
            f"<td class='center'>{html_escape(outcome)}</td>"
            f"<td class='center'>{dur}</td>"
            f"<td>{files}</td>"
            f"<td><pre>{err}</pre></td>"
            f"</tr>"
        )

    started = _SESSION_START.strftime("%Y-%m-%d %H:%M:%S")
    finished = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Test Dashboard</title>
<style>{_DARK_CSS}</style>
<script>{_DARK_JS}</script>
</head>
<body>
  <div class="wrap">
    <h1>Test Dashboard</h1>
    <div class="meta">Started: {started} &nbsp;|&nbsp; Finished: {finished}</div>

    <div class="card" style="margin-bottom:16px">
      <div class="row" style="align-items:center; justify-content:space-between;">
        <div class="row">
          <span class="badge pass">✔ Passed: {passed}</span>
          <span class="badge fail">✖ Failed: {failed}</span>
          <span class="badge skip">⏭ Skipped: {skipped}</span>
          <span class="badge tot">Σ Total: {total}</span>
        </div>
      </div>
      <div class="progress" style="margin-top:12px;">
        <div class="bar pass" style="width:{pct(passed)}%"></div>
        <div class="bar fail" style="width:{pct(failed)}%"></div>
        <div class="bar skip" style="width:{pct(skipped)}%"></div>
      </div>
    </div>

    <div class="controls">
      <button data-mode="all"  class="active" onclick="filterRows('all')">All</button>
      <button data-mode="fail" onclick="filterRows('fail')">Failed</button>
      <button data-mode="pass" onclick="filterRows('pass')">Passed</button>
      <button data-mode="skip" onclick="filterRows('skip')">Skipped</button>
    </div>

    <div class="table-wrap card">
      <table>
        <thead>
          <tr>
            <th>Test</th>
            <th>NodeID</th>
            <th>Outcome</th>
            <th>Duration</th>
            <th>Artifacts</th>
            <th>Error (truncated)</th>
          </tr>
        </thead>
        <tbody>
          {''.join(rows)}
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>"""

def write_and_open_dashboard():
    ensure_dir("reports")
    path = Path("reports") / "dashboard.html"
    html = _build_dashboard_html()
    path.write_text(html, encoding="utf-8")
    print(f"\nDashboard written to {path}")
    if not os.environ.get("CI"):
        try:
            webbrowser.open(path.resolve().as_uri())
        except Exception:
            pass