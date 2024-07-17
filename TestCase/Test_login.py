import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PageObjectModel.Login import Loginpage


class TestLogin:
    baseURL = "https://www.demoblaze.com/"
    username = "shreya123@gmail.com"
    password = "Dhoni@07"

    @pytest.fixture(scope="class")
    def setup(self, request):
        driver = webdriver.Chrome()
        driver.get(self.baseURL)
        request.cls.driver = driver
        yield driver
        driver.quit()

    def test_login(self, setup):
        self.lp = Loginpage(self.driver)

        # Ensure that the login modal is opened before interacting with elements
        self.driver.find_element(By.ID, "login2").click()

        # Wait for login modal to appear
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "logInModal"))
        )

        # Enter username
        username_field = self.driver.find_element(By.ID, "loginusername")
        username_field.clear()
        username_field.send_keys(self.username)

        # Enter password
        password_field = self.driver.find_element(By.ID, "loginpassword")
        password_field.clear()
        password_field.send_keys(self.password)

        # Click login button
        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]")
        login_button.click()

        # Wait for login to complete and assert
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "nameofelementafterlogin"))
            # Update this with actual element after login
        )
        act_title = self.driver.title
        assert act_title == "Expected Title After Login", f"Login failed, expected title 'Expected Title After Login', but got '{act_title}'"

    def test_products_displayed(self, setup):
        # Wait for products to be displayed
        products = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "card-block"))
        )
        assert len(products) > 0, "No products found on the homepage"

    def test_navigate_product_categories(self, setup):
        categories = ["Phones", "Laptops", "Monitors"]
        for category in categories:
            # Click on the category
            category_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, category))
            )
            category_link.click()

            # Wait for products in the selected category to be displayed
            products = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "card-block"))
            )
            assert len(products) > 0, f"No products found in category '{category}'"

            # Print out the product names (optional, for debugging purposes)
            product_names = [product.find_element(By.CLASS_NAME, "card-title").text for product in products]
            print(f"Products in category '{category}': {product_names}")


if __name__ == "__main__":
    pytest.main()
