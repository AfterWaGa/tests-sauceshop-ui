from playwright.sync_api import expect


class TestAuth:
    def test__auth(self, page):
        page.goto("https://www.saucedemo.com/")

        page.locator("#user-name").fill("standard_user")
        page.locator("#password").fill("secret_sauce")
        page.locator("#login-button").click()

        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


    def test__auth_locked_out_user(self, page):
        page.goto("https://www.saucedemo.com/")

        page.locator("#user-name").fill("locked_out_user")
        page.locator("#password").fill("secret_sauce")
        page.locator("#login-button").click()

        expect(page).to_have_url("https://www.saucedemo.com/")

        login_error = page.locator("//h3[@data-test='error']")

        expect(login_error).to_be_visible()
        expect(login_error).to_have_text("Epic sadface: Sorry, this user has been locked out.")


    def test__auth_visual_user(self, page):
        page.goto("https://www.saucedemo.com/")

        page.locator("#user-name").fill("visual_user")
        page.locator("#password").fill("secret_sauce")
        page.locator("#login-button").click()

        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

        page.locator("#react-burger-menu-btn").click()
        page.locator("#logout_sidebar_link").click()

        page.goto("https://www.saucedemo.com/")
        expect(page.locator("#login-button")).to_be_visible()


    def test__logout(self, page):
        page.goto("https://www.saucedemo.com/")

        page.locator("#user-name").fill("standard_user")
        page.locator("#password").fill("secret_sauce")
        page.locator("#login-button").click()

        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

        page.locator("#react-burger-menu-btn").click()
        page.locator("#logout_sidebar_link").click()

        page.goto("https://www.saucedemo.com/")
        expect(page.locator("#login-button")).to_be_visible()



