
import pytest
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage


@pytest.fixture
def cart_page(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    products_page = ProductsPage(driver)
    products_page.wait_for_page()

    # Add the first two products to the cart.
    products = driver.find_elements(*products_page.INVENTORY_ITEMS)

    for product in products[:2]:
        product.find_element(
            *products_page.ADD_TO_CART_BUTTONS
        ).click()

    # Open the Cart page.
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    page = CartPage(driver)
    page.wait_for_page()
    return page


def test_cart_page_title(cart_page):
    assert cart_page.get_page_title() == "Your Cart"


def test_two_products_are_in_cart(cart_page):
    assert cart_page.get_cart_item_count() == 2


def test_cart_product_names_are_not_blank(cart_page):
    names = cart_page.get_cart_item_names()

    assert len(names) == 2
    assert all(name.strip() for name in names)


def test_cart_product_prices_are_valid(cart_page):
    prices = cart_page.get_cart_item_prices()

    assert len(prices) == 2

    for price in prices:
        assert price.startswith("$")
        assert float(price.replace("$", "")) > 0


def test_continue_shopping_returns_to_products(driver, cart_page):
    cart_page.continue_shopping()

    assert driver.current_url.endswith("/inventory.html")


def test_cart_badge_increments_when_products_are_added(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    products_page = ProductsPage(driver)
    products_page.wait_for_page()

    products = driver.find_elements(*products_page.INVENTORY_ITEMS)

    products[0].find_element(
        *products_page.ADD_TO_CART_BUTTONS
    ).click()

    assert products_page.get_cart_count() == 1

    products[1].find_element(
        *products_page.ADD_TO_CART_BUTTONS
    ).click()

    assert products_page.get_cart_count() == 2


def test_cart_contains_expected_product_names(cart_page):
    names = cart_page.get_cart_item_names()

    assert names == [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
    ]


def test_remove_one_product_from_cart(driver, cart_page):
    cart_page.remove_item("Sauce Labs Backpack")

    assert cart_page.get_cart_item_count() == 1
    assert cart_page.get_cart_item_names() == [
        "Sauce Labs Bike Light"
    ]


def test_remove_all_products_from_cart(cart_page):
    cart_page.remove_item("Sauce Labs Backpack")
    cart_page.remove_item("Sauce Labs Bike Light")

    assert cart_page.get_cart_item_count() == 0
    assert cart_page.get_cart_item_names() == []


def test_checkout_button_navigates_to_checkout(cart_page, driver):
    cart_page.proceed_to_checkout()

    assert "/checkout-step-one.html" in driver.current_url
