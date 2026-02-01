from src.main.ui.pages.basket_page import BasketPage
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.checkout_page import CheckoutPage


class TestBasket:
    def test__add_item_to_basket_and_check(self, page):
        catalog = CatalogPage(page)
        basket = BasketPage(page)

        catalog.login("standard_user", "secret_sauce")
        catalog.add_to_cart("Sauce Labs Fleece Jacket")
        catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

        basket.open_cart()
        basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
        basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")


    def test__remove_item_from_cart(self, page):
        catalog = CatalogPage(page)
        basket = BasketPage(page)

        catalog.login("standard_user", "secret_sauce")
        catalog.add_to_cart("Sauce Labs Backpack")
        catalog.add_to_cart("Test.allTheThings() T-Shirt (Red)")

        basket.open_cart()
        basket.expect_item_in_cart("Sauce Labs Backpack")
        basket.expect_item_in_cart("Test.allTheThings() T-Shirt (Red)")

        basket.remove_item("Sauce Labs Backpack")
        basket.remove_item("Test.allTheThings() T-Shirt (Red)")

        basket.expect_item_not_in_cart("Sauce Labs Backpack")
        basket.expect_item_not_in_cart("Test.allTheThings() T-Shirt (Red)")


    def test__checkout_multiple_items(self, page):
        catalog = CatalogPage(page)
        basket = BasketPage(page)
        checkout = CheckoutPage(page)

        catalog.login("standard_user", "secret_sauce")
        catalog.add_to_cart("Sauce Labs Fleece Jacket")
        catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

        basket.open_cart()
        basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
        basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")

        basket_total = basket.get_items_total_price()

        basket.checkout()
        checkout.start_checkout(first_name="Test", last_name="User", postal_code="12345")

        checkout_total = checkout.get_item_total_after_continue()
        assert checkout_total == basket_total, ("Сумма товаров в Checkout не совпадает с корзиной")


    def test__checkout_without_items(self, page):
        catalog = CatalogPage(page)
        basket = BasketPage(page)
        checkout = CheckoutPage(page)

        catalog.login("standard_user", "secret_sauce")

        basket.open_cart()
        items = basket.get_item_names()
        assert len(items) == 0, "Корзина не пуста"

        basket.checkout()
        checkout.start_checkout(first_name="NewUser", last_name="Nkr", postal_code="")

        error_text = checkout.get_error_text()
        assert error_text != "", "Ожидалась ошибка при оформлении пустой корзины"