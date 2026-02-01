import pytest
from playwright.sync_api import sync_playwright

from src.main.ui.pages.login_page import LoginPage


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page

    context.close()


@pytest.fixture
def auth_page(page):
    login_page = LoginPage(page)
    login_page.open_page()
    login_page.login("standard_user", "secret_sauce")
    return page
