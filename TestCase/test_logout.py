import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from PageObjectModel.Login import Loginpage

class TestLogout:
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

    def login(self):
        self.lp = Loginpage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clicklogin()

        # Wait for the login button to disappear
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "login2"))
        )

    def test_logout(self, setup):
        # Perform login first
        self.login()

        try:
            # Perform the logout operation
            logout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "logout2"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", logout_button)
            logout_button.click()

            # Verify successful logout
            login_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "login2"))
            )
            assert login_button.is_displayed(), "Logout was not successful"

        except (TimeoutException, ElementClickInterceptedException) as e:
            pytest.fail(f"Logout failed: {e}")

if __name__ == "__main__":
    pytest.main()
