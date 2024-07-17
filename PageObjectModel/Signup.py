from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException



class SignupPage:
    textbox_username_id = "Username"
    textbox_password_id = "Password"
    textbox_signup_linktext = "Signup"

    def __init__(self, driver):
        self.driver = driver

    def setUsername(self, username):
        self.driver.find_element(By.ID, self.textbox_username_id).clear()
        self.driver.find_element(By.ID, self.textbox_username_id).send_keys(username)

    def setPassword(self, password):
        self.driver.find_element(By.ID, self.textbox_password_id).clear()
        self.driver.find_element(By.ID, self.textbox_password_id).send_keys(password)

    def ClickSignup(self):
        self.driver.find_element(By.LINK_TEXT, self.textbox_signup_linktext).click()

    def signup(self, username, password):
        pass
