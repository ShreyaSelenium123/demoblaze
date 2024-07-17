import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PageObjectModel.Login import Loginpage


class TestProductBrowsing:
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

    def test_products_displayed(self, setup):

        products = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "card-block"))
        )
        assert len(products) > 0, "No products found on the homepage"

    def test_navigate_product_categories(self, setup):
        categories = ["Phones", "Laptops", "Monitors"]
        for category in categories:

            category_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, category))
            )
            category_link.click()


            products = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "card-block"))
            )
            assert len(products) > 0, f"No products found in category '{category}'"


            product_names = [product.find_element(By.CLASS_NAME, "card-title").text for product in products]
            print(f"Products in category '{category}': {product_names}")


if __name__ == "__main__":
    pytest.main()
