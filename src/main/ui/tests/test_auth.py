from playwright.sync_api import expect

from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.login_page import LoginPage


class TestAuth:
    def test__auth(self, page):
        login_page = LoginPage(page)
        login_page.open_page()
        login_page.login("standard_user", "secret_sauce")

        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


    def test__auth_locked_out_user(self, page):
        login_page = LoginPage(page)
        login_page.open_page()
        login_page.login("locked_out_user", "secret_sauce")

        expect(page).to_have_url(login_page.URL)
        expect(login_page.login_error_msg).to_be_visible()
        expect(login_page.login_error_msg).to_have_text("Epic sadface: Sorry, this user has been locked out.")


    def test__auth_visual_user(self, page):
        login_page = LoginPage(page)
        login_page.open_page()
        login_page.login("visual_user", "secret_sauce")

        catalog_page = CatalogPage(page)
        assert catalog_page.get_products_count() > 0

        catalog_page.logout()
        expect(page).to_have_url(LoginPage.URL)


    def test__logout(self, page):
        login_page = LoginPage(page)
        login_page.open_page()
        login_page.login("standard_user", "secret_sauce")

        catalog_page = CatalogPage(page)
        assert catalog_page.get_products_count() > 0

        catalog_page.logout()
        expect(page).to_have_url(LoginPage.URL)