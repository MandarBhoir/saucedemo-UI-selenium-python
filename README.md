# SauceDemo UI Automation Framework

A UI test automation framework built using **Python, Selenium WebDriver, and Pytest** to validate end-to-end e-commerce workflows on the SauceDemo demo application.

## Tech Stack

- **Language:** Python
- **UI Automation:** Selenium WebDriver
- **Test Framework:** Pytest
- **Design Pattern:** Page Object Model (POM)
- **Reporting:** Allure Reports
- **IDE:** PyCharm
- **Version Control:** Git and GitHub

## Features

- Login testing with valid and invalid credentials
- Product listing, sorting, and product detail validation
- Shopping cart operations
- Checkout form validation
- Order summary and price calculations
- Order completion and navigation validation
- Explicit waits for browser interactions
- Allure test reporting

## Project Structure

```text
saucedemo-UI-selenium-python/
├── pages/
│   ├── login_page.py
│   ├── products_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── test_login.py
│   ├── test_products.py
│   ├── test_cart.py
│   └── test_checkout.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.12 or compatible version
- Google Chrome
- PyCharm (recommended)
- Git

## Setup

Clone the repository:

```bash
git clone https://github.com/MandarBhoir/saucedemo-UI-selenium-python
cd saucedemo-UI-selenium-python
```

Create and activate a virtual environment on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run Tests

Run the complete test suite:

```powershell
python -m pytest -v
```

Run a specific test module:

```powershell
python -m pytest tests/test_login.py -v
```

## Allure Reporting

Generate Allure result files while running tests:

```powershell
python -m pytest -v --alluredir=allure-results
```

Generate the HTML report:

```powershell
allure generate allure-results --clean -o allure-report
```

Open the report:

```powershell
allure open allure-report
```

**Note:** The Allure command-line tool must be installed separately from the `allure-pytest` Python package.

## Test Coverage

| Module | Coverage |
|---|---|
| Login | Authentication and validation |
| Products | Listing, sorting and product details |
| Cart | Add, remove and cart validation |
| Checkout | Form validation, totals and order completion |

## Application Under Test

[SauceDemo](https://www.saucedemo.com/)

This is a demo application. Checkout and payment information are simulated; no real payment is processed.

## Author

Mandar Bhoir