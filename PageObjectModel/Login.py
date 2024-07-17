import pytest
from selenium.webdriver.common.by import By
from PageObjectModel.Signup import SignupPage
from selenium.common.exceptions import NoSuchElementException


class Loginpage:
    textbox_username_id = "loginusername"
    textbox_password_id = "loginpassword"
    button_login_xpath = "/html/body/div[3]/div/div/div[3]/button[2]"
    link_logout_linktext = "Logout"

    def __init__(self, driver):
        self.driver = driver

    def setUserName(self, loginusername):
        self.driver.find_element(By.ID, self.textbox_username_id).clear()
        self.driver.find_element(By.ID, self.textbox_username_id).send_keys(loginusername)

    def setPassword(self, loginpassword):
        self.driver.find_element(By.ID, self.textbox_password_id).clear()
        self.driver.find_element(By.ID, self.textbox_password_id).send_keys(loginpassword)

    def clicklogin(self):
        self.driver.find_element(By.XPATH, self.button_login_xpath).click()

    def clickLogout(self):
        self.driver.find_element(By.LINK_TEXT, self.link_logout_linktext).click()
