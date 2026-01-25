from playwright.sync_api import expect


class TestCatalog:
    def test__count_of_product_cards(self, auth_page):
        product_cards = auth_page.locator("//div[@data-test='inventory-item']")

        expect(product_cards).to_have_count(6)


    def test__sorted_by_name(self, auth_page):
        sort_select = auth_page.locator("//select[@data-test='product-sort-container']")
        expect(sort_select).to_be_visible()

        sort_select.click()
        sort_select.select_option("az")

        names_of_products = auth_page.locator("//div[@data-test='inventory-item-name']").all_text_contents()

        assert names_of_products == sorted(names_of_products)


    def test__sorted_by_name_reversed(self, auth_page):
        sort_select = auth_page.locator("//select[@data-test='product-sort-container']")
        expect(sort_select).to_be_visible()

        sort_select.click()
        sort_select.select_option("za")

        names_of_products = auth_page.locator("//div[@data-test='inventory-item-name']").all_text_contents()

        assert names_of_products == sorted(names_of_products, reverse=True)


    def test__sorted_by_price(self, auth_page):
        sort_select = auth_page.locator("//select[@data-test='product-sort-container']")
        expect(sort_select).to_be_visible()

        sort_select.select_option("lohi")

        prices_text = auth_page.locator("//div[@data-test='inventory-item-price']").all_text_contents()
        prices_list = [float(price.replace("$", "")) for price in prices_text]

        assert prices_list == sorted(prices_list)  # Сортировка цен по возрастанию

        sort_select.select_option("hilo")

        prices_text = auth_page.locator("//div[@data-test='inventory-item-price']").all_text_contents()
        prices_list = [float(price.replace("$", "")) for price in prices_text]

        assert prices_list == sorted(prices_list, reverse=True)  # Сортировка цен по убыванию


    def test__add_to_cart(self, auth_page):
        product_card = auth_page.locator("//div[@data-test='inventory-item']", has_text="Sauce Labs Bike Light")
        add_btn = product_card.locator("#add-to-cart-sauce-labs-bike-light")

        add_btn.click()

        remove_btn = product_card.locator("#remove-sauce-labs-bike-light")

        expect(remove_btn).to_have_text("Remove")
        expect(auth_page.locator("//span[@data-test='shopping-cart-badge']")).to_have_text("1")


    def test__add_and_delete_from_cart(self, auth_page):
        product_card = auth_page.locator("//div[@data-test='inventory-item']", has_text="Sauce Labs Onesie")
        add_btn = product_card.locator("#add-to-cart-sauce-labs-onesie")

        add_btn.click()

        remove_btn = product_card.locator("#remove-sauce-labs-onesie")

        expect(remove_btn).to_have_text("Remove")
        expect(auth_page.locator("//span[@data-test='shopping-cart-badge']")).to_have_text("1")

        remove_btn.click()

        expect(add_btn).to_have_text("Add to cart")
        expect(auth_page.locator("//span[@data-test='shopping-cart-badge']")).not_to_be_visible()


    def test__product_details_fleece_jacket(self, auth_page):
        product_card = auth_page.locator("//div[@data-test='inventory-item']", has_text="Sauce Labs Fleece Jacket")

        product_name = product_card.locator("[data-test='inventory-item-name']").inner_text()
        product_price = product_card.locator("[data-test='inventory-item-price']").inner_text()

        product_card.locator("[data-test='inventory-item-name']").click()

        detail_name = auth_page.locator("[data-test='inventory-item-name']").inner_text()
        detail_price = auth_page.locator("[data-test='inventory-item-price']").inner_text()

        assert product_name == detail_name
        assert product_price == detail_price


