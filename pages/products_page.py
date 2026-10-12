
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class ProductsPage:
    URL = "https://www.saucedemo.com/inventory.html"

    # Products page locators
    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_DESCRIPTIONS = (By.CLASS_NAME, "inventory_item_desc")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".inventory_item_img img")
    ADD_TO_CART_BUTTONS = (
        By.CSS_SELECTOR,
        ".inventory_item button.btn_inventory",
    )
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    # Product details page locators
    PRODUCT_DETAIL_NAME = (By.CLASS_NAME, "inventory_details_name")
    PRODUCT_DETAIL_DESCRIPTION = (
        By.CLASS_NAME,
        "inventory_details_desc",
    )
    PRODUCT_DETAIL_PRICE = (By.CLASS_NAME, "inventory_details_price")
    PRODUCT_DETAIL_IMAGE = (By.CSS_SELECTOR, ".inventory_details_img")
    BACK_TO_PRODUCTS_BUTTON = (By.ID, "back-to-products")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Products page methods
    def wait_for_page(self):
        self.wait.until(
            EC.visibility_of_element_located(self.PAGE_TITLE)
        )
        self.wait.until(
            EC.visibility_of_all_elements_located(self.INVENTORY_ITEMS)
        )

    def get_page_title(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.PAGE_TITLE)
        ).text

    def get_product_count(self):
        self.wait_for_page()
        return len(self.driver.find_elements(*self.INVENTORY_ITEMS))

    def get_product_names(self):
        self.wait_for_page()
        return [
            element.text
            for element in self.driver.find_elements(*self.PRODUCT_NAMES)
        ]

    def get_product_descriptions(self):
        self.wait_for_page()
        return [
            element.text
            for element in self.driver.find_elements(
                *self.PRODUCT_DESCRIPTIONS
            )
        ]

    def get_product_prices(self):
        self.wait_for_page()
        return [
            element.text
            for element in self.driver.find_elements(*self.PRODUCT_PRICES)
        ]

    def get_product_image_statuses(self):
        self.wait_for_page()
        images = self.driver.find_elements(*self.PRODUCT_IMAGES)

        return [
            {
                "alt": image.get_attribute("alt"),
                "loaded": self.driver.execute_script(
                    "return arguments[0].complete "
                    "&& arguments[0].naturalWidth > 0;",
                    image,
                ),
            }
            for image in images
        ]

    def get_add_to_cart_button_count(self):
        self.wait_for_page()
        return len(
            self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
        )

    def sort_products(self, option):
        valid_options = {"az", "za", "lohi", "hilo"}

        if option not in valid_options:
            raise ValueError(
                f"Invalid sort option: {option}. "
                f"Choose one of {sorted(valid_options)}"
            )

        dropdown = self.wait.until(
            EC.element_to_be_clickable(self.SORT_DROPDOWN)
        )
        Select(dropdown).select_by_value(option)

    def get_cart_count(self):
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    # Product details navigation
    def open_product(self, product_name):
        self.wait_for_page()

        for product in self.driver.find_elements(*self.INVENTORY_ITEMS):
            name_element = product.find_element(*self.PRODUCT_NAMES)

            if name_element.text.strip() == product_name.strip():
                old_url = self.driver.current_url

                self.wait.until(
                    EC.element_to_be_clickable(name_element)
                ).click()

                try:
                    self.wait.until(EC.url_changes(old_url))
                    self.wait.until(
                        EC.visibility_of_element_located(
                            self.PRODUCT_DETAIL_NAME
                        )
                    )
                except Exception as exc:
                    raise AssertionError(
                        f"Could not open product details for "
                        f"'{product_name}'. "
                        f"URL before click: {old_url}. "
                        f"URL after click: {self.driver.current_url}"
                    ) from exc

                return

        raise ValueError(f"Product not found: {product_name}")

    def is_products_page_displayed(self):
        return (
            self.driver.current_url.endswith("/inventory.html")
            and self.get_page_title() == "Products"
        )

    # Product details methods
    def get_product_detail(self):
        name = self.wait.until(
            EC.visibility_of_element_located(self.PRODUCT_DETAIL_NAME)
        ).text

        description = self.wait.until(
            EC.visibility_of_element_located(
                self.PRODUCT_DETAIL_DESCRIPTION
            )
        ).text

        price = self.wait.until(
            EC.visibility_of_element_located(self.PRODUCT_DETAIL_PRICE)
        ).text

        image = self.wait.until(
            EC.visibility_of_element_located(self.PRODUCT_DETAIL_IMAGE)
        )

        image_loaded = self.driver.execute_script(
            "return arguments[0].complete "
            "&& arguments[0].naturalWidth > 0;",
            image,
        )

        return {
            "name": name,
            "description": description,
            "price": price,
            "image_loaded": image_loaded,
        }

    def return_to_products(self):
        self.wait.until(
            EC.element_to_be_clickable(self.BACK_TO_PRODUCTS_BUTTON)
        ).click()

        self.wait_for_page()
