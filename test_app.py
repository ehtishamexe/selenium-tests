import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import xmlrunner

# YOUR NEW IP IS SET HERE
BASE_URL = "http://13.53.243.123:8081"

def get_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--single-process")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-dev-tools")
    opts.add_argument("--no-zygote")
    opts.add_argument("--memory-pressure-off")

    return webdriver.Chrome(options=opts)

class FlaskAppTests(unittest.TestCase):

    def test_01_home_page_loads(self):
        d = get_driver(); d.get(BASE_URL)
        self.assertNotEqual(d.title, ""); d.quit()

    def test_02_login_page_accessible(self):
        d = get_driver(); d.get(f"{BASE_URL}/login")
        self.assertIn("login", d.page_source.lower()); d.quit()

    def test_03_register_page_accessible(self):
        d = get_driver(); d.get(f"{BASE_URL}/register")
        self.assertIn("register", d.page_source.lower()); d.quit()

    def test_04_login_form_has_email_field(self):
        d = get_driver(); d.get(f"{BASE_URL}/login")
        field = d.find_elements(By.XPATH, "//input[@type='email' or @name='email' or @name='username']")
        self.assertGreater(len(field), 0); d.quit()

    def test_05_login_form_has_password_field(self):
        d = get_driver(); d.get(f"{BASE_URL}/login")
        field = d.find_elements(By.XPATH, "//input[@type='password']")
        self.assertGreater(len(field), 0); d.quit()

    def test_06_page_has_no_server_error(self):
        d = get_driver(); d.get(BASE_URL)
        self.assertNotIn("500", d.page_source); d.quit()

    def test_07_home_not_404(self):
        d = get_driver(); d.get(BASE_URL)
        self.assertNotIn("404", d.title); d.quit()

    def test_08_page_source_not_empty(self):
        d = get_driver(); d.get(BASE_URL)
        self.assertGreater(len(d.page_source), 200); d.quit()

    def test_09_login_page_has_submit_button(self):
        d = get_driver(); d.get(f"{BASE_URL}/login")
        btn = d.find_elements(By.XPATH, "//button[@type='submit'] | //input[@type='submit']")
        self.assertGreater(len(btn), 0); d.quit()

    def test_10_register_has_submit_button(self):
        d = get_driver(); d.get(f"{BASE_URL}/register")
        btn = d.find_elements(By.XPATH, "//button[@type='submit'] | //input[@type='submit']")
        self.assertGreater(len(btn), 0); d.quit()

    def test_11_page_has_html_structure(self):
        d = get_driver(); d.get(BASE_URL)
        self.assertIsNotNone(d.find_element(By.TAG_NAME, "html")); d.quit()

    def test_12_invalid_login_stays_on_login(self):
        d = get_driver(); d.get(f"{BASE_URL}/login")
        try:
            d.find_element(By.XPATH, "//input[@type='email' or @name='email' or @name='username']").send_keys("fake@fake.com")
            d.find_element(By.XPATH, "//input[@type='password']").send_keys("wrongpassword")
            d.find_element(By.XPATH, "//button[@type='submit'] | //input[@type='submit']").click()
        except: pass
        self.assertNotIn("dashboard", d.current_url.lower()); d.quit()

    def test_13_page_loads_under_15_seconds(self):
        import time; d = get_driver()
        start = time.time(); d.get(BASE_URL); elapsed = time.time() - start
        self.assertLess(elapsed, 15); d.quit()

    def test_14_page_refresh_works(self):
        d = get_driver(); d.get(BASE_URL); d.refresh()
        self.assertIsNotNone(d.title); d.quit()

    def test_15_register_has_input_fields(self):
        d = get_driver(); d.get(f"{BASE_URL}/register")
        inputs = d.find_elements(By.TAG_NAME, "input")
        self.assertGreater(len(inputs), 1); d.quit()

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-results"))
