# pages/base_page.py
import time
from utils.logger import log
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # Initialize WebDriverWait with a 10-second timeout
        self.wait = WebDriverWait(driver, 10)

    def open_notifications(self):
        self.driver.open_notifications()

    def click_by_text(self, text: str):
        # """Clica em QUALQUER elemento cujo texto seja exatamente `text`."""
        self.click_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{text}")'
        )

    def click_by_text_contains(self, text_substring: str):
        # """Clica em elemento cujo texto CONTÉM `text_substring`."""
        self.click_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().textContains("{text_substring}")'
        )

    def is_notification_displayed(self, expected_title):
        try:
            notification_title_locator = (AppiumBy.XPATH, f"//*[@resource-id='android:id/title' and @text='{expected_title}']")
            self.wait_for_visibility_of_element(*notification_title_locator)
            return True
        except TimeoutException:
            return False
        finally:
            self.driver.back() # Always close the notification shade

    def get_notification_text(self, expected_title):
        try:
            # Find the title to anchor our search
            title_element = self.wait_for_visibility_of_element(AppiumBy.XPATH, f"//*[@resource-id='android:id/title' and @text='{expected_title}']")
            # The notification text is often a sibling element
            notification_text = title_element.find_element(AppiumBy.XPATH, "following-sibling::*[@resource-id='android:id/text']").text
            return notification_text
        except Exception:
            return None
        finally:
            self.driver.back() # Always close the notification shade

    def find_element(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def click_element(self, by, locator):
        log.info(f"Clicking element with locator: {locator}")
        try:
            self.wait_for_element_to_be_clickable(by, locator).click()
            log.info("Element clicked successfully.")
        except Exception as e:
            log.error(f"Failed to click element with locator: {locator}", exc_info=True)
            raise

    def send_keys_to_element(self, by, locator, text):
        # Wait for the element to be visible, then send keys
        self.wait_for_visibility_of_element(by, locator).clear().send_keys(text)

    def get_element_text(self, by, locator):
        return self.find_element(by, locator).text

    def is_element_displayed(self, by, locator):
        try:
            # We try to wait for the element to be visible
            self.wait_for_visibility_of_element(by, locator)
            # If the above line doesn't throw an exception, the element is visible
            return True
        except TimeoutException:
            # If a TimeoutException occurs, it means the element was not found in time
            return False
            # try:
            #     return self.find_element(by, locator).is_displayed()
            # except:
            #     return False
        
    def wait_for_visibility_of_element(self, by, locator):
        # Waits up to 10s for an element to be visible on the screen
        return self.wait.until(EC.visibility_of_element_located((by, locator)))

    def wait_for_element_to_be_clickable(self, by, locator):
        # Waits up to 10s for an element to be visible and enabled
        return self.wait.until(EC.element_to_be_clickable((by, locator)))
        
    def scroll_screen_down(self, percent: float = 0.8):
        """Scrolla a tela toda pra BAIXO. percent entre 0 e 1."""
        size = self.driver.get_window_size()
        self.driver.execute_script(
            "mobile: scrollGesture",
            {
                "left": 0,
                "top": size["height"] * 0.3,
                "width": size["width"],
                "height": size["height"] * 0.5,
                "direction": "down",
                "percent": percent,
            },
        )
        time.sleep(0.5)

    def scroll_screen_up(self, percent: float = 0.8):
        """Scrolla a tela toda pra CIMA. percent entre 0 e 1."""
        size = self.driver.get_window_size()
        self.driver.execute_script(
            "mobile: scrollGesture",
            {
                "left": 0,
                "top": size["height"] * 0.3,
                "width": size["width"],
                "height": size["height"] * 0.5,
                "direction": "up",
                "percent": percent,
            },
        )
        time.sleep(0.5)

    def get_button_state(self, by, locator):
        return self.find_element(by, locator).get_attribute('enabled')