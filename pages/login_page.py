
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    URL = "https://www.saucedemo.com/"

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_CLOSE_BUTTON = (By.CLASS_NAME, "error-button")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def enter_username(self, username):
        field = self.wait.until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        )
        field.clear()
        field.send_keys(username)

    def enter_password(self, password):
        field = self.wait.until(
            EC.visibility_of_element_located(self.PASSWORD_INPUT)
        )
        field.clear()
        field.send_keys(password)

    def click_login(self):
        self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        ).click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        ).text

    def is_error_displayed(self):
        return bool(
            self.driver.find_elements(*self.ERROR_MESSAGE)
        )

    def close_error_message(self):
        self.wait.until(
            EC.element_to_be_clickable(self.ERROR_CLOSE_BUTTON)
        ).click()

    def is_login_form_displayed(self):
        return (
            self.driver.find_element(*self.USERNAME_INPUT).is_displayed()
            and self.driver.find_element(*self.PASSWORD_INPUT).is_displayed()
            and self.driver.find_element(*self.LOGIN_BUTTON).is_displayed()
        )


    def press_enter_in_password(self):
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys("\n")

    def get_password_field_type(self):
        return self.driver.find_element(*self.PASSWORD_INPUT).get_attribute("type")

    def get_username_value(self):
        return self.driver.find_element(*self.USERNAME_INPUT).get_attribute("value")

    def get_password_value(self):
        return self.driver.find_element(*self.PASSWORD_INPUT).get_attribute("value")

