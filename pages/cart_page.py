
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    URL = "https://www.saucedemo.com/cart.html"

    # Cart page locators
    PAGE_TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CART_ITEM_DESCRIPTIONS = (By.CLASS_NAME, "inventory_item_desc")
    CART_ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    REMOVE_BUTTONS = (
        By.CSS_SELECTOR,
        ".cart_item button.cart_button",
    )
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_page(self):
        self.wait.until(
            EC.visibility_of_element_located(self.PAGE_TITLE)
        )

    def get_page_title(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.PAGE_TITLE)
        ).text

    def get_cart_item_count(self):
        self.wait_for_page()
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def get_cart_item_names(self):
        self.wait_for_page()
        return [
            item.text
            for item in self.driver.find_elements(*self.CART_ITEM_NAMES)
        ]

    def get_cart_item_descriptions(self):
        self.wait_for_page()
        return [
            item.text
            for item in self.driver.find_elements(
                *self.CART_ITEM_DESCRIPTIONS
            )
        ]

    def get_cart_item_prices(self):
        self.wait_for_page()
        return [
            item.text
            for item in self.driver.find_elements(*self.CART_ITEM_PRICES)
        ]

    def remove_item(self, product_name):
        self.wait_for_page()

        for item in self.driver.find_elements(*self.CART_ITEMS):
            name = item.find_element(*self.CART_ITEM_NAMES)

            if name.text.strip() == product_name.strip():
                remove_button = item.find_element(
                    By.CSS_SELECTOR,
                    "button.cart_button",
                )
                self.wait.until(
                    EC.element_to_be_clickable(remove_button)
                ).click()
                return

        raise ValueError(f"Product not found in cart: {product_name}")

    def continue_shopping(self):
        self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_SHOPPING_BUTTON)
        ).click()

    def proceed_to_checkout(self):
        self.wait.until(
            EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
        ).click()

    def is_cart_page_displayed(self):
        return (
            self.driver.current_url.endswith("/cart.html")
            and self.get_page_title() == "Your Cart"
        )
