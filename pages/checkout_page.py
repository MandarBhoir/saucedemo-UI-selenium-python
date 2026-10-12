
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    # Checkout page URLs
    INFORMATION_URL = "https://www.saucedemo.com/checkout-step-one.html"
    OVERVIEW_URL = "https://www.saucedemo.com/checkout-step-two.html"
    COMPLETE_URL = "https://www.saucedemo.com/checkout-complete.html"

    # Checkout information page locators
    PAGE_TITLE = (By.CLASS_NAME, "title")
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # Checkout overview page locators
    SUMMARY_ITEMS = (By.CLASS_NAME, "cart_item")
    SUMMARY_ITEM_NAMES = (By.CSS_SELECTOR,".cart_item .inventory_item_name",)
    SUMMARY_ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    # Order confirmation page locators
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_page_title(self):
        return self.wait.until(
            lambda driver: driver.find_element(
                *self.PAGE_TITLE
            ).text
        )

    def enter_customer_information(self, first_name, last_name, postal_code):
        self.wait.until(
            EC.visibility_of_element_located(self.FIRST_NAME_INPUT)
        ).send_keys(first_name)

        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE_INPUT).send_keys(
            postal_code
        )

    def continue_checkout(self):
        self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_BUTTON)
        ).click()

    def get_error_message(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        ).text

    def cancel_checkout(self):
        self.wait.until(
            EC.element_to_be_clickable(self.CANCEL_BUTTON)
        ).click()

    def get_summary_item_count(self):
        self.wait.until(
            EC.url_contains("/checkout-step-two.html")
        )
        self.wait.until(
            EC.visibility_of_element_located(self.PAGE_TITLE)
        )
        return len(self.driver.find_elements(*self.SUMMARY_ITEMS))

    def get_summary_item_names(self):
        self.wait.until(
            EC.url_contains("/checkout-step-two.html")
        )
        self.wait.until(
            EC.visibility_of_element_located(self.PAGE_TITLE)
        )

        return [
            item.text.strip()
            for item in self.driver.find_elements(
                *self.SUMMARY_ITEM_NAMES
            )
        ]

    def get_summary_item_prices(self):
        self.wait.until(
            EC.url_contains("/checkout-step-two.html")
        )
        self.wait.until(
            EC.visibility_of_element_located(self.PAGE_TITLE)
        )

        return [
            item.text.strip()
            for item in self.driver.find_elements(
                *self.SUMMARY_ITEM_PRICES
            )
        ]

    def get_item_total(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.ITEM_TOTAL)
        ).text

    def get_tax(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.TAX)
        ).text

    def get_total(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.TOTAL)
        ).text

    def finish_order(self):
        self.wait.until(
            EC.element_to_be_clickable(self.FINISH_BUTTON)
        ).click()

    def get_order_confirmation(self):
        header = self.wait.until(
            EC.visibility_of_element_located(self.COMPLETE_HEADER)
        ).text

        message = self.wait.until(
            EC.visibility_of_element_located(self.COMPLETE_TEXT)
        ).text

        return {
            "header": header,
            "message": message,
        }

    def back_to_products(self):
        self.wait.until(
            EC.element_to_be_clickable(self.BACK_HOME_BUTTON)
        ).click()

        self.wait.until(
            EC.url_contains("/inventory.html")
        )

        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "title"), "Products"
            )
        )

