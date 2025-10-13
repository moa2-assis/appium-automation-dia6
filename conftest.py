import pytest
import pytest_html
from selenium import webdriver
import json
from pathlib import Path
import time
import os, pytest_html
from datetime import datetime
import sys
import subprocess
import webbrowser
from html import escape
from datetime import datetime
import csv
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

"""Conftest para executar o setup de testes com Selenium WebDriver."""

report_data = []

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser to execute tests (chrome or firefox)")

def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames:
        browser = metafunc.config.getoption("browser").split(",")
        metafunc.parametrize("browser", browser)
        
import pytest
from appium import webdriver
from appium.options.common.base import AppiumOptions

@pytest.fixture(scope="function")
def driver():
    # --- SETUP PHASE ---
    options = AppiumOptions()
    options.load_capabilities({ "platformName": "Android",
	"appium:deviceName": "emulator-5554",
	"appium:automationName": "UiAutomator2",
	"appium:appPackage": "com.saucelabs.mydemoapp.android",
	"appium:ensureWebviewsHavePages": True,
	"appium:nativeWebScreenshot": True,
	"appium:newCommandTimeout": 3600,
	"appium:connectHardwareKeyboard": True,
    "appWaitActivity": "com.saucelabs.mydemoapp.android.view.activities.MainActivity",
    "appWaitDuration": 30000 }) # Capabilities defined here
    _driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    
    # The 'yield' keyword passes control to the test function
    yield _driver
    
    # --- TEARDOWN PHASE ---
    # This code runs AFTER the test function completes (or fails)
    print("\nQuitting driver...")
    _driver.quit()

LOG_FILE = Path("test_durations.log")

@pytest.fixture(scope="session")
def load_capabilities():
    """Lê o JSON de dados de teste a partir de /root/data/appium_test_day3.json"""
    json_path = Path(__file__).resolve().parent / "data" / "appium_test_day3.json"
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_android_capabilities(load_capabilities):
    android_caps = load_capabilities["android"]
    assert android_caps["platformName"] == "Android"
    assert "deviceName" in android_caps


def test_ios_capabilities(load_capabilities):
    ios_caps = load_capabilities["ios"]
    assert ios_caps["automationName"] == "XCUITest"

# relatórios

# @pytest.hookimpl(tryfirst=True)
# def pytest_runtest_setup(item):
#     """Hook para ver tempo de início de cada teste."""
#     item.start_time = time.time()
#     item.start_str = time.strftime("%H:%M:%S", time.localtime())
#     msg = f"\n[START] Test '{item.nodeid}' - {item.start_str}"
#     print(msg)
    
#     with LOG_FILE.open("a", encoding="utf-8") as f:
#         f.write(msg + "\n")

# @pytest.hookimpl(trylast=True)
# def pytest_runtest_teardown(item):
#     """Hook para ver o tempo de término de cada teste."""
#     duration = time.time() - item.start_time
#     msg = f"[END] Test '{item.nodeid}' finished in {duration:.2f} seconds."
#     print(msg)

#     # salva em arquivo
#     with LOG_FILE.open("a", encoding="utf-8") as f:
#         f.write(msg + "\n")

# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, "extra", [])
#     if report.when == "call":  # and report.failed:
#         status = 'Passed' if report.passed else 'Failed'
#         browser = getattr(item, 'browser', 'N/A')
#         test_name = item.name
#         duration = f"{report.duration:.4f}s"

#         if report.failed:
#             # Create screenshots directory if it doesn't exist
#             if not os.path.exists("screenshots"):
#                 os.makedirs("screenshots")
#             # Take screenshot
#             driver = item.funcargs['driver']
#             ts = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f"{ts}_{test_name}_error_{browser}.png"
#             screenshot_file = os.path.join("screenshots", filename)
#             driver.save_screenshot(screenshot_file)
#             # Add screenshot to the HTML report
#             if screenshot_file:
#                 html = (
#                     f'<div><img src="{screenshot_file}" alt="screenshot" '
#                     f'style="width:304px;height:228px;" onclick="window.open(this.src)" align="right"/></div>'
#                 )
#                 extra.append(pytest_html.extras.html(html))
        
#         report_data.append({
#             "browser": browser.capitalize(),
#             "test_case_name": test_name,
#             "status": status,
#             "duration_s": f"{report.duration:.4f}",
#         })

#     report.extra = extra

# def pytest_sessionfinish(session, exitstatus):
#     """Gera e abre o dashboard antigo (script externo) e cria o CSV final."""
#      # >>> ADICIONE ESSA LINHA <<<
#     if _is_worker(session.config):
#         return  # não gera/abre nada dentro dos workers

#     root = Path.cwd()

#     # 1) Dashboard antigo (script externo)
#     try:
#         script = root / "dashboard.py"
#         subprocess.run([sys.executable, str(script)], check=True)
#     except Exception as e:
#         print(f"[dashboard-old] erro ao executar dashboard.py: {e}")

#     # tenta abrir o HTML do dashboard antigo (tenta alguns caminhos comuns)
#     old_candidates = [
#         root / "dashboard.html",
#         root / "dashboard" / "dashboard.html",
#         root / "dashboard" / "index.html",
#     ]
#     opened_old = False
#     for cand in old_candidates:
#         if cand.exists():
#             _open_if_exists(cand, "dashboard antigo")
#             opened_old = True
#             break
#     if not opened_old:
#         print("[dashboard-old] nenhum arquivo HTML encontrado nos caminhos padrão.")

#     # 2) CSV com resultados
#     if not report_data:
#         return
        
#     # Ordena os dados por browser e nome do teste (corrigido: 'browser')
#     sorted_reports = sorted(report_data, key=lambda x: (x['browser'], x['test_case_name']))
    
#     keys = ["browser", "test_case_name", "status", "duration_s"]
    
#     with open('test_report.csv', 'w', newline='', encoding='utf-8') as output_file:
#         dict_writer = csv.DictWriter(output_file, fieldnames=keys)
#         dict_writer.writeheader()
#         dict_writer.writerows(sorted_reports)

#     print("\nReport 'test_report.csv' generated successfully")

# def _open_if_exists(path: Path, label: str):
#     if path.exists():
#         try:
#             webbrowser.open(path.resolve().as_uri())
#             print(f"[dashboard] aberto: {label} -> {path}")
#         except Exception as e:
#             print(f"[dashboard] gerado em: {path} (abra manualmente). Motivo: {e}")
#     else:
#         print(f"[dashboard] não encontrado: {label} -> {path}")

# def _is_worker(config) -> bool:
#     # True dentro de um worker do xdist (gw0, gw1, ...)
#     return hasattr(config, "workerinput") or bool(os.environ.get("PYTEST_XDIST_WORKER"))

# @pytest.fixture(scope="class")
# def class_resource():
#     print("\n[SETUP] class_resource")
#     yield "class fixture"
#     print("[TEARDOWN] class_resource")

# @pytest.fixture(scope="module")
# def module_resource():
#     print("\n[SETUP] module_resource")
#     yield "module fixture"
#     print("[TEARDOWN] module_resource")

# @pytest.fixture(scope="session")
# def session_resource():
#     print("\n[SETUP] session_resource")
#     yield "session fixture"
#     print("[TEARDOWN] session_resource")