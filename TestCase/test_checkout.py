import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PageObjectModel.Login import Loginpage


class TestCheckout:
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

    def add_product_to_cart(self):
        driver = self.driver
        # Add the first product to the cart
        first_product = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "card-block"))
        )
        first_product.find_element(By.TAG_NAME, "a").click()

        # Add to cart
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Add to cart')]"))
        )
        add_to_cart_button.click()

        # Handle alert
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()

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

    def test_checkout_positive(self, setup):
        self.add_product_to_cart()

        # Go to the cart
        cart_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "cartur"))
        )
        cart_link.click()

        # Verify that the product is in the cart
        cart_items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr"))
        )
        assert len(cart_items) > 0, "No items in the cart"

        # Proceed to checkout
        place_order_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Place Order')]"))
        )
        place_order_button.click()

        # Fill out the order form
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "orderModal"))
        )
        self.driver.find_element(By.ID, "name").send_keys("John Doe")
        self.driver.find_element(By.ID, "country").send_keys("USA")
        self.driver.find_element(By.ID, "city").send_keys("New York")
        self.driver.find_element(By.ID, "card").send_keys("1234567812345678")
        self.driver.find_element(By.ID, "month").send_keys("12")
        self.driver.find_element(By.ID, "year").send_keys("2023")
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Purchase')]").click()

        # Verify purchase success
        confirmation = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "sweet-alert"))
        )
        assert "Thank you for your purchase!" in confirmation.text, "Purchase not successful"

    def test_logout(self, setup):
        # Perform the logout operation
        logout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "logout2"))
        )
        logout_button.click()


if __name__ == "__main__":
    pytest.main()
