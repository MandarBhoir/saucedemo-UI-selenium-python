import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    """Create and clean up a Chrome WebDriver instance."""
    options = Options()
    options.add_argument("--start-maximized")

    browser = webdriver.Chrome(options=options)

    yield browser

    browser.quit()
