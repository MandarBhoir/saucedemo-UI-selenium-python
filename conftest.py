
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()

    # Use a fresh, temporary browser profile for each test.
    options.add_argument("--incognito")

    # Disable Chrome password-manager services where supported.
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        },
    )

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    yield driver

    driver.quit()
