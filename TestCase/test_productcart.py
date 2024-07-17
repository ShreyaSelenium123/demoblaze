import time

import pytest
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PageObjectModel.Login import Loginpage


class TestShoppingCart:
    baseURL = "https://www.demoblaze.com/"
    username="shreya123@gmail.com"
    password="Dhoni@07"

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
        time.sleep(5)

    def test_add_product_to_cart(self, setup):
        driver = self.driver

        # Navigate to the last page by clicking the "Next" button repeatedly
        while True:
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "next2"))
                )
                next_button.click()
            except Exception as e:
                break

        # Select the last product on the last page
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "card-block"))
        )
        last_product = products[-1]
        last_product_name = last_product.find_element(By.CLASS_NAME, "card-title").text
        last_product.find_element(By.TAG_NAME, "a").click()

        # Add the product to the cart
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Add to cart')]"))
        )
        add_to_cart_button.click()
        time.sleep(5)

        # Handle alert
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()

        # Verify that the product has been added to the cart
        cart_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "cartur"))
        )
        cart_link.click()

        cart_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr"))
        )
        product_names_in_cart = [item.find_element(By.XPATH, "./td[2]").text for item in cart_items]

        assert last_product_name in product_names_in_cart, f"Product '{last_product_name}' not found in the cart"

    def test_logout(self, setup):
        # Perform login first
        self.login()

        try:
            # Click on logout button
            logout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "logout2"))
            )
            logout_button.click()

            # Verify logout was successful
            login_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "login2"))
            )
            assert login_button.is_displayed(), "Logout was not successful"

        except (TimeoutException, NoSuchElementException) as e:
            pytest.fail(f"Logout failed: {e}")

    def login(self):
        pass


if __name__ == "__main__":
    pytest.main()
