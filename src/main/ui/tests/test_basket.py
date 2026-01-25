from playwright.sync_api import expect


class TestBasket:
    def test__add_item_to_basket_and_check(self, auth_page):
        auth_page.locator("[data-test='add-to-cart-sauce-labs-fleece-jacket']").click()
        auth_page.locator("[data-test='add-to-cart-sauce-labs-bolt-t-shirt']").click()

        auth_page.locator("[data-test='shopping-cart-link']").click()

        items_names = auth_page.locator("[data-test='inventory-item-name']").all_text_contents()
        assert "Sauce Labs Fleece Jacket" in items_names
        assert "Sauce Labs Bolt T-Shirt" in items_names


    def test__remove_item_from_cart(self, auth_page):
        auth_page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
        auth_page.locator("[data-test='add-to-cart-test.allthethings()-t-shirt-(red)']").click()

        auth_page.locator("[data-test='shopping-cart-link']").click()

        item1 = auth_page.locator("[data-test='inventory-item']", has_text="Sauce Labs Backpack")
        item2 = auth_page.locator("[data-test='inventory-item']", has_text="Test.allTheThings() T-Shirt (Red)")

        expect(item1).to_be_visible()
        expect(item2).to_be_visible()

        auth_page.locator("[data-test='remove-sauce-labs-backpack']").click()
        expect(item1).not_to_be_visible()
        auth_page.locator("[data-test='remove-test.allthethings()-t-shirt-(red)']").click()
        expect(item2).not_to_be_visible()


    def test__checkout_multiple_items(self, auth_page):
        jacket_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Fleece Jacket")
        t_shirt_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Bolt T-Shirt")

        jacket_card.locator("button").click()
        t_shirt_card.locator("button").click()

        auth_page.locator('[data-test="shopping-cart-link"]').click()

        jacket_name = auth_page.locator(".inventory_item_name", has_text="Sauce Labs Fleece Jacket")
        t_shirt_name = auth_page.locator(".inventory_item_name", has_text="Sauce Labs Bolt T-Shirt")

        expect(jacket_name).to_be_visible()
        expect(t_shirt_name).to_be_visible()

        prices_text = auth_page.locator(".inventory_item_price").all_text_contents()
        prices = [float(p.replace("$", "")) for p in prices_text]
        expected_total = sum(prices)

        auth_page.locator('[data-test="checkout"]').click()
        auth_page.locator('[data-test="firstName"]').fill("Test")
        auth_page.locator('[data-test="lastName"]').fill("User")
        auth_page.locator('[data-test="postalCode"]').fill("12345")
        auth_page.locator('[data-test="continue"]').click()

        item_total_text = auth_page.locator(".summary_subtotal_label").inner_text()
        item_total_value = float(item_total_text.split("$")[1])

        assert item_total_value == expected_total, (f"Item total ({item_total_value}) не совпадает с суммой товаров ({expected_total})")

        tax_text = auth_page.locator(".summary_tax_label").inner_text()
        tax_value = float(tax_text.split("$")[1])

        total_text = auth_page.locator(".summary_total_label").inner_text()
        total_value = float(total_text.split("$")[1])

        assert total_value == round(item_total_value + tax_value, 2), ("Total не совпадает с суммой Item total + Tax")

        auth_page.locator('[data-test="finish"]').click()

        success_message = auth_page.locator(".complete-header")
        expect(success_message).to_have_text("Thank you for your order!")


    def test__checkout_without_items(self, auth_page):
        auth_page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()

        auth_page.locator('[data-test="shopping-cart-link"]').click()

        jacket = auth_page.locator(".inventory_item_name", has_text="Sauce Labs Fleece Jacket")
        expect(jacket).to_be_visible()

        auth_page.locator('[data-test="checkout"]').click()

        auth_page.get_by_placeholder("First Name").fill("NewUser")
        auth_page.get_by_placeholder("Last Name").fill("Nrk")

        auth_page.locator('[data-test="continue"]').click()

        error_message = auth_page.locator('[data-test="error"]')
        expect(error_message).to_have_text("Error: Postal Code is required")