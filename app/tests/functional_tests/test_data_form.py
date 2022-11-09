from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.browser import make_chrome_browser


class DataFormFuncionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        # self.browser = make_chrome_browser('--headless')
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def test_home_page_title(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Currency Viewer', body.text)

    def _post_data_form(self, start_date, end_date):
        self.browser.get(self.live_server_url)
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="start"]'))).send_keys(start_date)

        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="end"]'))).send_keys(end_date)

        el = self.browser.find_element(By.XPATH, '//*[@id="currency"]')
        for option in el.find_elements(By.TAG_NAME, 'option'):
            if option.text == 'BRL':
                option.click()
                break
        button = self.browser.find_element(By.CSS_SELECTOR,
                                           'button[type="submit"]')
        button.click()

    def test_post_form_title_graph(self):
        self._post_data_form('10/25/2022', '10/27/2022')
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
            (By.ID, 'container')))

        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Currency Rate (BRL based on USD)', body.text)

    def test_post_form_end_date_must_be_earlier_or_equal_today(self):
        self._post_data_form('10/25/2022', '10/27/2030')
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'alert-danger')))

        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('End date must be earlier or equal than today',
                      body.text)

    def test_post_form_start_date_must_be_earlier_than_end_date(self):
        self._post_data_form('10/28/2022', '10/27/2022')
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'alert-danger')))

        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Start date must be earlier than End date',
                      body.text)

    def test_post_form_date_range_must_have_5_maximum_business_days(self):
        self._post_data_form('10/28/2022', '11/08/2022')
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'alert-danger')))

        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Maximum of 5 business days',
                      body.text)
