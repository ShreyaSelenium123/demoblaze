import time

import pytest
from selenium import webdriver
from selenium.webdriver.common import alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PageObjectModel.Signup import SignupPage


class TestSignup:
    baseURL = "https://www.demoblaze.com/"
    username = "shreya123@gmail.com"
    password = "Dhoni@07"

    @pytest.fixture(scope="class")
    def setup(self, request):
        self.driver = webdriver.Chrome()
        self.driver.get(self.baseURL)
        request.cls.driver = self.driver
        yield
        self.driver.quit()

    @pytest.mark.usefixtures("setup")
    def test_homepage_title(self):
        act_title = self.driver.title
        assert act_title == "STORE", f"Expected title 'STORE', but got '{act_title}'"

    @pytest.mark.usefixtures("setup")
    def test_signup(self):
        # Navigate to signup modal
        self.driver.find_element(By.ID, 'signin2').click()

        # Initialize the signup page object
        signup_page = SignupPage(self.driver)

        # Perform a signup operation
        signup_page.signup(self.username, self.password)

        try:
            # Wait for alert to be present
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())

            # Switch to the alert
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            assert "Sign up successful." in alert_text, f"Expected success message, but got '{alert_text}'"
            alert.accept()
        except Exception as e:
            print("No alert present. Checking for other success messages on the page.")
            # You can add alternative checks here, like checking for success messages in a specific element.
            # For example:
            # success_message = self.driver.find_element(By.ID, 'success_message_id')
            # assert "Sign up successful" in success_message.text, f"Expected success message, but got '{success_message.text}'"

        # Add any additional assertions or cleanup needed
    def test_001_signup(self):
        self.driver.find_element(By.ID,"sign-username").send_keys("shreya123@gmail.com")
        self.driver.find_element(By.ID,"sign-password").send_keys("Dhoni@07")
        self.driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[3]/button[2]").click()
        time.sleep(5)
        self.driver.find_element(By.ID, "alertButton").click()
        alert_text = alert.text
        print("Alert text:", alert_text)

        # Accept the alert (click OK)
        alert.accept()


