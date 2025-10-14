# conftest.py
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional

import pytest
from appium import webdriver
from appium.options.common.base import AppiumOptions

from utils import reporting as R
from utils.logger import setup_logger

# ===== logging de sessão =====
LOG = None
SESSION_LOG_PATH = None

def _timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def _ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    global LOG, SESSION_LOG_PATH
    _ensure_dir("logs")
    SESSION_LOG_PATH = Path("logs") / f"{_timestamp()}_log_session.txt"
    LOG = setup_logger(SESSION_LOG_PATH)
    LOG.info("=== Pytest session STARTED ===")

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    R.write_and_open_dashboard()
    if LOG:
        LOG.info(f"=== Pytest session FINISHED (exitstatus={exitstatus}) ===")
        LOG.info(f"Dashboard: reports/dashboard.html")
        LOG.info(f"Session log: {SESSION_LOG_PATH}")

# ===== helpers locais (screenshot/vídeo) =====
def save_screenshot(driver, item) -> str:
    _ensure_dir("screenshots")
    name = f"screenshots/{_timestamp()}_screenshot_{item.name}.png"
    driver.get_screenshot_as_file(name)
    if LOG:
        LOG.info(f"[ARTIFACT] screenshot saved -> {name} (test={item.nodeid})")
    return name

def save_video_from_driver(driver, test_name: str, nodeid: str) -> Optional[str]:
    data = driver.stop_recording_screen()
    if not data:
        return None
    _ensure_dir("videos")
    name = f"videos/{_timestamp()}_video_{test_name}.mp4"
    with open(name, "wb") as f:
        f.write(base64.b64decode(data))
    if LOG:
        LOG.info(f"[ARTIFACT] video saved -> {name} (test={nodeid})")
    return name

# ===== pytest options/matrix (se usar) =====
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="browser to execute tests (chrome or firefox)")

def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames:
        browsers = metafunc.config.getoption("browser").split(",")
        metafunc.parametrize("browser", browsers)

# ===== hooks de teste =====
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    if LOG:
        LOG.info(f"=== START test: {item.nodeid} ===")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # alimenta o dashboard (fase call)
    R.upsert_result(item, rep)

    # screenshot apenas em falha
    if rep.when == "call" and rep.failed and "driver" in item.fixturenames:
        driver = item.funcargs["driver"]
        path = save_screenshot(driver, item)
        R.add_screenshot(item, path)

    # log de fim na fase call (onde temos outcome/duration)
    if rep.when == "call" and LOG:
        dur = getattr(rep, "duration", None)
        dur_s = f"{dur:.2f}s" if dur is not None else "n/a"
        LOG.info(f"=== END test: {item.nodeid} | outcome={rep.outcome} | duration={dur_s} ===")

@pytest.fixture(scope="function")
def driver(request):
    options = AppiumOptions()
    options.load_capabilities({
        "platformName": "Android",
        "appium:deviceName": "emulator-5554",
        "appium:automationName": "UiAutomator2",
        "appium:appPackage": "com.automationmodule",
        "appium:ensureWebviewsHavePages": True,
        "appium:nativeWebScreenshot": True,
        "appium:newCommandTimeout": 3600,
        "appium:connectHardwareKeyboard": True,
        # remova caps redundantes/typos se quiser
    })
    try:
        _driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        _driver.start_recording_screen()  # grava sempre; salva arquivo só se falhar
        if LOG:
            LOG.info(f"[DRIVER] session started: {getattr(_driver, 'session_id', 'n/a')}")
    except Exception as e:
        if LOG:
            LOG.error(f"[DRIVER] failed to create Appium driver: {e}")
        pytest.skip(f"Failed to create Appium driver: {e}")

    yield _driver

    # teardown: vídeo só se falhou
    try:
        # checa status do teste atual
        rep_call = getattr(request.node, "rep_call", None)
        failed = bool(rep_call and rep_call.failed)
        if failed:
            vid = save_video_from_driver(_driver, request.node.name, request.node.nodeid)
            if vid:
                R.add_video(request.node, vid)
        else:
            _ = _driver.stop_recording_screen()
    finally:
        if LOG:
            LOG.info("[DRIVER] quitting session")
        _driver.quit()
