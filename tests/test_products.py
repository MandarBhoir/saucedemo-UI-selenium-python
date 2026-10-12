import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


@pytest.fixture
def products_page(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    page = ProductsPage(driver)
    page.wait_for_page()
    return page


def test_products_page_title(products_page):
    assert products_page.get_page_title() == "Products"


def test_all_six_products_are_displayed(products_page):
    assert products_page.get_product_count() == 6


def test_product_names_are_not_blank(products_page):
    names = products_page.get_product_names()

    assert len(names) == 6
    assert all(name.strip() for name in names)


def test_product_descriptions_are_not_blank(products_page):
    descriptions = products_page.get_product_descriptions()

    assert len(descriptions) == 6
    assert all(description.strip() for description in descriptions)


def test_product_prices_are_valid_and_positive(products_page):
    prices = products_page.get_product_prices()

    assert len(prices) == 6

    for price in prices:
        assert price.startswith("$")
        amount = float(price.replace("$", ""))
        assert amount > 0


def test_all_products_have_add_to_cart_buttons(products_page):
    assert products_page.get_add_to_cart_button_count() == 6


def test_product_images_are_loaded(products_page):
    statuses = products_page.get_product_image_statuses()

    assert len(statuses) == 6
    assert all(item["loaded"] for item in statuses)


@pytest.mark.parametrize(
    ("sort_option", "reverse"),
    [
        ("az", False),
        ("za", True),
    ],
)
def test_sort_products_by_name(products_page, sort_option, reverse):
    products_page.sort_products(sort_option)

    actual_names = products_page.get_product_names()
    expected_names = sorted(actual_names, reverse=reverse)

    assert actual_names == expected_names


@pytest.mark.parametrize(
    ("sort_option", "reverse"),
    [
        ("lohi", False),
        ("hilo", True),
    ],
)
def test_sort_products_by_price(products_page, sort_option, reverse):
    products_page.sort_products(sort_option)

    actual_prices = [
        float(price.replace("$", ""))
        for price in products_page.get_product_prices()
    ]
    expected_prices = sorted(actual_prices, reverse=reverse)

    assert actual_prices == expected_prices



def test_open_product_details(products_page):
    product_name = products_page.get_product_names()[0]

    products_page.open_product(product_name)

    assert "/inventory-item.html" in products_page.driver.current_url
    assert products_page.get_product_detail()["name"] == product_name


def test_product_details_have_valid_information(products_page):
    product_name = products_page.get_product_names()[0]

    products_page.open_product(product_name)
    details = products_page.get_product_detail()

    assert details["name"].strip()
    assert details["description"].strip()
    assert float(details["price"].replace("$", "")) > 0
    assert details["image_loaded"] is True


def test_return_from_details_to_products(products_page):
    product_name = products_page.get_product_names()[0]

    products_page.open_product(product_name)
    products_page.return_to_products()

    assert products_page.is_products_page_displayed()


def test_refresh_products_page(products_page):
    products_page.driver.refresh()
    products_page.wait_for_page()

    assert products_page.get_product_count() == 6


def test_inventory_without_login(driver):
    driver.get("https://www.saucedemo.com/inventory.html")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "login-button"))
    )

    assert "saucedemo.com" in driver.current_url
    assert driver.find_element(By.ID, "login-button").is_displayed()


def test_invalid_product_name_raises_error(products_page):
    with pytest.raises(ValueError, match="Product not found"):
        products_page.open_product("Nonexistent Product")


def test_problem_user_product_listing(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("problem_user", "secret_sauce")

    page = ProductsPage(driver)
    page.wait_for_page()

    assert page.get_product_count() == 6

    # Record image behavior without assuming every image must be correct.
    image_statuses = page.get_product_image_statuses()
    assert len(image_statuses) == 6
