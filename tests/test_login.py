
import pytest

from pages.login_page import LoginPage


@pytest.mark.parametrize(
    "username,password",
    [
        ("standard_user", "secret_sauce"),
        ("problem_user", "secret_sauce"),
        ("performance_glitch_user", "secret_sauce"),
        ("error_user", "secret_sauce"),
        ("visual_user", "secret_sauce"),
    ],
)
def test_login_with_valid_accounts(driver, username, password):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, password)

    assert driver.title == "Swag Labs"
    assert driver.current_url.endswith("/inventory.html")


def test_login_page_elements_are_visible(driver):
    login_page = LoginPage(driver)
    login_page.open()

    assert login_page.is_login_form_displayed()


@pytest.mark.parametrize(
    "username,password",
    [
        ("invalid_user", "secret_sauce"),
        ("standard_user", "wrong_password"),
        ("invalid_user", "wrong_password"),
    ],
)
def test_login_with_invalid_credentials(driver, username, password):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, password)

    assert login_page.is_error_displayed()
    assert login_page.is_login_form_displayed()
    assert not driver.current_url.endswith("/inventory.html")


@pytest.mark.parametrize(
    "username,password",
    [
        ("", "secret_sauce"),
        ("standard_user", ""),
        ("", ""),
    ],
)
def test_login_with_missing_credentials(driver, username, password):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, password)

    assert login_page.is_error_displayed()
    assert login_page.is_login_form_displayed()


def test_locked_out_user_cannot_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("locked_out_user", "secret_sauce")

    assert login_page.is_error_displayed()
    assert "locked out" in login_page.get_error_message().lower()
    assert not driver.current_url.endswith("/inventory.html")


def test_error_message_can_be_dismissed(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("invalid_user", "secret_sauce")

    assert login_page.is_error_displayed()

    login_page.close_error_message()

    assert not login_page.is_error_displayed()


def test_login_with_valid_credentials_after_failed_attempt(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("invalid_user", "wrong_password")

    assert login_page.is_error_displayed()

    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    assert driver.current_url.endswith("/inventory.html")


@pytest.mark.parametrize(
    "username,password",
    [
        ("STANDARD_USER", "secret_sauce"),
        ("standard_user", "SECRET_SAUCE"),
        (" standard_user", "secret_sauce"),
        ("standard_user ", "secret_sauce"),
        ("   ", "secret_sauce"),
        ("standard_user", "   "),
        ("x" * 300, "secret_sauce"),
        ("standard_user", "x" * 300),
        ("!@#$%^&*()", "secret_sauce"),
        ("standard_user", "!@#$%^&*()"),
        ("用户测试", "密码测试"),
        ("' OR '1'='1", "anything"),
        ("<script>alert(1)</script>", "anything"),
    ],
)
def test_login_handles_unusual_credentials(driver, username, password):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, password)

    assert not driver.current_url.endswith("/inventory.html")


def test_password_field_is_masked(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.enter_password("secret_sauce")

    assert login_page.get_password_field_type() == "password"


def test_error_can_be_cleared_before_retry(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("invalid_user", "wrong_password")

    assert login_page.is_error_displayed()
    login_page.close_error_message()
    assert not login_page.is_error_displayed()

    login_page.login("standard_user", "secret_sauce")
    assert driver.current_url.endswith("/inventory.html")


def test_refresh_login_page(driver):
    login_page = LoginPage(driver)
    login_page.open()
    driver.refresh()

    assert login_page.is_login_form_displayed()


def test_login_with_enter_key(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.press_enter_in_password()

    assert driver.current_url.endswith("/inventory.html")

