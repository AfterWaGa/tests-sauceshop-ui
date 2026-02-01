class LoginPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_btn = page.locator("#login-button")
        self.login_error_msg = page.locator("//h3[@data-test='error']")

    def open_page(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_btn.click()

    def get_login_error_text(self):
        return self.login_error_msg.inner_text()