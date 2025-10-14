# tests/test_day6.py
import pytest
import time
from pages.home_page import HomePage

@pytest.mark.smoke
@pytest.mark.android
def test_appium_automacao_pass(driver):
    home_page = HomePage(driver)
    # 1 - Start the application and ensure that the home screen has loaded.
    time.sleep(2)
    home_page.click_popup_button()
    home_page.dismiss_popup()
    home_page.click_popup_button()
    home_page.accept_popup()
    home_page.click_notification_button()
    home_page.allow_notifications()
    home_page.click_notification_button()

    assert 1 == 1

@pytest.mark.regression
@pytest.mark.android
def test_appium_automacao_fail(driver):
    home_page = HomePage(driver)
    # 1 - Start the application and ensure that the home screen has loaded.
    time.sleep(2)
    home_page.click_popup_button()
    home_page.dismiss_popup()
    home_page.click_popup_button()
    home_page.accept_popup()
    home_page.click_notification_button()
    home_page.allow_notifications()
    home_page.click_notification_button()

    assert 1 == 2