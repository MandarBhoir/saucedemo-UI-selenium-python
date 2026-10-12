
import pytest
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture
def checkout_page(driver):
    # Log in
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    # Add two specific products
    products_page = ProductsPage(driver)
    products_page.wait_for_page()

    product_names = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
    ]

    for product_name in product_names:
        products = driver.find_elements(
            *products_page.INVENTORY_ITEMS
        )

        for product in products:
            name = product.find_element(
                *products_page.PRODUCT_NAMES
            ).text

            if name == product_name:
                product.find_element(
                    *products_page.ADD_TO_CART_BUTTONS
                ).click()
                break
        else:
            pytest.fail(f"Product not found: {product_name}")

    # Verify both products were added
    assert products_page.get_cart_count() == 2

    # Open cart
    driver.find_element(
        By.CLASS_NAME, "shopping_cart_link"
    ).click()

    cart_page = CartPage(driver)
    cart_page.wait_for_page()

    assert cart_page.get_cart_item_count() == 2

    # Proceed to checkout
    cart_page.proceed_to_checkout()
    print("URL after checkout click:", driver.current_url)
    print("Page title after checkout click:", driver.title)
    print("Heading after checkout click:",
          driver.find_element(By.CLASS_NAME, "title").text)

    return CheckoutPage(driver)


def test_checkout_information_page_title(checkout_page):
    assert checkout_page.get_page_title() == "Checkout: Your Information"


def test_checkout_requires_first_name(checkout_page):
    checkout_page.enter_customer_information("", "Bhoir", "400001")
    checkout_page.continue_checkout()

    assert "First Name is required" in checkout_page.get_error_message()


def test_checkout_requires_last_name(checkout_page):
    checkout_page.enter_customer_information("Mandar", "", "400001")
    checkout_page.continue_checkout()

    assert "Last Name is required" in checkout_page.get_error_message()


def test_checkout_requires_postal_code(checkout_page):
    checkout_page.enter_customer_information("Mandar", "Bhoir", "")
    checkout_page.continue_checkout()

    assert "Postal Code is required" in checkout_page.get_error_message()


def test_valid_information_opens_checkout_overview(checkout_page):
    checkout_page.enter_customer_information(
        "Mandar", "Bhoir", "400001"
    )
    checkout_page.continue_checkout()

    assert checkout_page.driver.current_url.endswith(
        "/checkout-step-two.html"
    )
    assert checkout_page.get_page_title() == "Checkout: Overview"


def test_checkout_overview_contains_two_products(checkout_page):
    checkout_page.enter_customer_information(
        "Mandar", "Bhoir", "400001"
    )
    checkout_page.continue_checkout()

    assert checkout_page.get_summary_item_count() == 2


def test_checkout_overview_shows_product_names(checkout_page):
    checkout_page.enter_customer_information(
        "Mandar", "Bhoir", "400001"
    )
    checkout_page.continue_checkout()

    assert checkout_page.get_summary_item_names() == [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
    ]


def test_checkout_overview_shows_valid_prices(checkout_page):
    checkout_page.enter_customer_information(
        "Mandar", "Bhoir", "400001"
    )
    checkout_page.continue_checkout()

    prices = checkout_page.get_summary_item_prices()

    assert len(prices) == 2
    assert all(
        price.startswith("$")
        and float(price.replace("$", "")) > 0
        for price in prices
    )


def test_cancel_checkout_returns_to_cart(checkout_page):
    checkout_page.cancel_checkout()

    assert checkout_page.driver.current_url.endswith("/cart.html")


def test_complete_order(checkout_page):
    checkout_page.enter_customer_information(
        "Mandar", "Bhoir", "400001"
    )
    checkout_page.continue_checkout()
    checkout_page.finish_order()

    confirmation = checkout_page.get_order_confirmation()

    assert confirmation["header"] == "Thank you for your order!"
    assert confirmation["message"].strip()


def test_checkout_subtotal_matches_product_prices(checkout_page):
    checkout_page.enter_customer_information(
        "Mandar", "Bhoir", "400001"
    )
    checkout_page.continue_checkout()

    prices = checkout_page.get_summary_item_prices()
    subtotal_text = checkout_page.get_item_total()

    subtotal = float(subtotal_text.split("$")[1])
    expected_subtotal = sum(
        float(price.replace("$", "")) for price in prices
    )

    assert len(prices) == 2
    assert subtotal == pytest.approx(expected_subtotal, abs=0.01)


def test_checkout_tax_is_valid_and_non_negative(checkout_page):
    checkout_page.enter_customer_information(
        "Mandar", "Bhoir", "400001"
    )
    checkout_page.continue_checkout()

    tax_text = checkout_page.get_tax()
    tax = float(tax_text.split("$")[1])

    assert tax >= 0


def test_checkout_total_equals_subtotal_plus_tax(checkout_page):
    checkout_page.enter_customer_information(
        "Mandar", "Bhoir", "400001"
    )
    checkout_page.continue_checkout()

    subtotal = float(
        checkout_page.get_item_total().split("$")[1]
    )
    tax = float(checkout_page.get_tax().split("$")[1])
    total = float(checkout_page.get_total().split("$")[1])

    assert total == pytest.approx(subtotal + tax, abs=0.01)


def test_checkout_accepts_unexpected_postal_code(checkout_page):
    checkout_page.enter_customer_information(
        "Mandar", "Bhoir", "INVALID-POSTAL"
    )
    checkout_page.continue_checkout()

    assert checkout_page.driver.current_url.endswith(
        "/checkout-step-two.html"
    )
    assert checkout_page.get_page_title() == "Checkout: Overview"


def test_back_to_products_after_order_completion(checkout_page):
    checkout_page.enter_customer_information(
        "Mandar", "Bhoir", "400001"
    )
    checkout_page.continue_checkout()
    checkout_page.finish_order()

    confirmation = checkout_page.get_order_confirmation()
    assert confirmation["header"] == "Thank you for your order!"

    checkout_page.back_to_products()

    assert checkout_page.driver.current_url.endswith("/inventory.html")
    assert checkout_page.driver.find_element(
        *ProductsPage.PAGE_TITLE
    ).text == "Products"
