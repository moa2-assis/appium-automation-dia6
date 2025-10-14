# pages/home_page.py
from .base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
import time

class HomePage(BasePage):
    # ... other locators
    POPUP_TITLE = (AppiumBy.ID, "android:id/alertTitle")
    POPUP_MESSAGE = (AppiumBy.ID, "android:id/message")
    OK_BUTTON = (AppiumBy.ID, "android:id/button1")
    CANCEL_BUTTON = (AppiumBy.ID, "android:id/button2")

    show_popup_button = 'new UiSelector().text("Show Popup")'
    show_notification_button = 'new UiSelector().text("Notification")'
    automation_module_button = 'new UiSelector().text("Automation Module")'
    text_changed_button = 'new UiSelector().text("Text Changed")'
    wait_10_seconds_button = 'new UiSelector().text("Wait 10 seconds...")'

    permission_allow_button = 'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_button")'
    permission_dontallow_button = 'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_deny_button")'

    def get_popup_title(self):
        return self.get_element_text(*self.POPUP_TITLE)

    def get_popup_message(self):
        return self.get_element_text(*self.POPUP_MESSAGE)

    def accept_popup(self):
        # self.click_element(*self.OK_BUTTON)
        self.click_by_text("Accept")
        time.sleep(1)

    def dismiss_popup(self):
        # self.click_element(*self.CANCEL_BUTTON)
        self.click_by_text("Cancel")
        time.sleep(1)

    def click_popup_button(self):
        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.show_popup_button)
        time.sleep(1)

    def click_notification_button(self):
        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.show_notification_button)
        time.sleep(1)

    def allow_notifications(self):
        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.permission_allow_button)

    def dontallow_notifications(self):
        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.permission_dontallow_button)
    
