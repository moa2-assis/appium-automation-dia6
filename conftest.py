# conftest.py
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional
import pytest
from appium import webdriver
from appium.options.common.base import AppiumOptions

from utils import reporting as R  # <-- só o dashboard

# ===== helpers locais (screenshot/vídeo) =====
def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)

def test_failed(request) -> bool:
    rep = getattr(request.node, "rep_call", None)
    return bool(rep and rep.failed)

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

# ===== pytest config opcional =====
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="browser to execute tests (chrome or firefox)")

def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames:
        browsers = metafunc.config.getoption("browser").split(",")
        metafunc.parametrize("browser", browsers)

# ===== hooks =====
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # anexa o report por fase ao item (para test_failed)
    setattr(item, f"rep_{rep.when}", rep)

    # alimenta o dashboard (só na fase call)
    R.upsert_result(item, rep)

    # screenshot apenas em falha
    if rep.when == "call" and rep.failed and "driver" in item.fixturenames:
        driver = item.funcargs["driver"]
        path = save_screenshot(driver, item)
        R.add_screenshot(item, path)

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
        "appium:androidScreenshotOnFai": True,
        "appium:nativeWebScreenshot": True,
        "appium:recordVideo": "true",
        "appium:videoType": "mpeg4"
    })
    try:
        _driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        _driver.start_recording_screen()  # grava sempre, mas salva arquivo só se falhar
    except Exception as e:
        pytest.skip(f"Failed to create Appium driver: {e}")

    yield _driver

    # teardown: vídeo só se falhou
    try:
        if test_failed(request):
            vid = save_video_from_driver(_driver, request.node.name)
            if vid:
                R.add_video(request.node, vid)
        else:
            _ = _driver.stop_recording_screen()
    finally:
        _driver.quit()

def pytest_sessionfinish(session, exitstatus):
    # Gera e abre o dashboard ao final da sessão
    R.write_and_open_dashboard()