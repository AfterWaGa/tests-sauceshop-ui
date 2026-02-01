from playwright.sync_api import expect
from src.main.ui.pages.catalog_page import CatalogPage


class TestCatalog:
    def test__count_of_product_cards(self, page):
        catalog_page = CatalogPage(page)
        catalog_page.login("standard_user", "secret_sauce")

        assert catalog_page.get_products_count() == 6


    def test__sorted_by_name(self, page):
        catalog_page = CatalogPage(page)
        catalog_page.login("standard_user", "secret_sauce")

        catalog_page.sort_items("az")
        assert catalog_page.get_product_names() == sorted(catalog_page.get_product_names())

        catalog_page.sort_items("za")
        assert catalog_page.get_product_names() == sorted(catalog_page.get_product_names(), reverse=True)


    def test__sorted_by_price(self, page):
        catalog_page = CatalogPage(page)
        catalog_page.login("standard_user", "secret_sauce")

        catalog_page.sort_items("lohi")
        assert catalog_page.get_product_prices() == sorted(catalog_page.get_product_prices())

        catalog_page.sort_items("hilo")
        assert catalog_page.get_product_prices() == sorted(catalog_page.get_product_prices(), reverse=True)


    def test__add_to_cart(self, page):
        catalog_page = CatalogPage(page)
        catalog_page.login("standard_user", "secret_sauce")

        button = catalog_page.add_to_cart("Sauce Labs Bike Light")
        expect(button).to_have_text("Remove")
        assert catalog_page.get_cart_count() == 1


    def test__add_and_remove_onesie(self, page):
        catalog = CatalogPage(page)
        catalog.login("standard_user", "secret_sauce")

        catalog.add_to_cart("Sauce Labs Onesie")
        assert catalog.get_cart_count() == 1

        catalog.remove_from_cart("Sauce Labs Onesie")
        assert catalog.get_cart_count() == 0


    def test__product_details_onesie(self, page):
        catalog = CatalogPage(page)
        catalog.login("standard_user", "secret_sauce")

        name, price, detail_name, detail_price = catalog.open_product_details("Sauce Labs Onesie")

        assert name == detail_name
        assert price == detail_price


    def test__product_details_fleece_jacket(self, page):
        catalog = CatalogPage(page)
        catalog.login("standard_user", "secret_sauce")

        name, price, detail_name, detail_price = catalog.open_product_details("Sauce Labs Fleece Jacket")

        assert name == detail_name
        assert price == detail_price


    def test__remove_item_from_catalog(self, page):
        catalog = CatalogPage(page)
        catalog.login("standard_user", "secret_sauce")

        remove_button = catalog.remove_from_cart("Test.allTheThings() T-Shirt (Red)")

        expect(remove_button).to_have_text("Add to cart")