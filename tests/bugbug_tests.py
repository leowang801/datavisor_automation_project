from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest

class BugBugTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)
    
    def login(self):
        email_entry = self.driver.find_element(By.NAME, "email")
        email_entry.send_keys("leowang801@gmail.com")
        password_entry = self.driver.find_element(By.NAME, "password")
        password_entry.send_keys("LW123456")
        sign_in_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        self.driver.execute_script("arguments[0].click();", sign_in_button)

    def create_new_project(self, project_name, project_url):
        self.driver.get("https://app.bugbug.io/organizations/")
        self.login()

        wait = WebDriverWait(self.driver, 10)

        new_project_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='ProjectList.NewProjectButton']")))
        new_project_button.click()

        project_name_entry = self.driver.find_element(By.NAME, "name")
        project_name_entry.send_keys(project_name)
        project_url_entry = self.driver.find_element(By.NAME, "homepageUrl")
        project_url_entry.send_keys(project_url)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
        element.click()   
    

    def test_successfully_create_new_project(self):
        self.create_new_project("Google", "https://www.google.com")
        assert "Google" in self.driver.page_source
        self.driver.quit()

    def test_unsuccessfully_create_new_project_no_name(self):
        self.create_new_project("", "https://www.google.com")
        assert "This field is required" in self.driver.page_source
        self.driver.quit()

    def test_unsuccessfully_create_new_project_no_url(self):
        self.create_new_project("GOOGLE", "")
        assert "This field is required" in self.driver.page_source
        self.driver.quit()

    def test_unsuccessfully_create_new_project_invalid_url(self):
        self.create_new_project("GOOGLE", "   ")
        assert "This URL is not valid" in self.driver.page_source
        self.driver.quit()
        
if __name__ == "__main__":
    unittest.main()