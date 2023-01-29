import time
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import dotenv
from selenium.webdriver.common.keys import Keys


class EasyApply:

    def __init__(self):
        dotenv.load_dotenv()
        self.linkedin_username = os.getenv("LINKEDIN_USERNAME")
        self.linkedin_password = os.getenv("LINKEDIN_PASSWORD")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--start-maximized')
        # chrome_options.add_argument('--start-fullscreen')
        # chrome_options.add_argument('--single-process')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument("--incognito")
        # chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        # chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        # chrome_options.add_experimental_option('useAutomationExtension', False)
        # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # chrome_options.add_argument("disable-infobars")
        self.driver = webdriver.Chrome(options=chrome_options)
        flask_job_postings_url = ("https://www.linkedin.com/jobs/search/?distance=25&f_AL=true&"
                                  "f_T=25169&f_WT=2&geoId=103644278&keywords=flask")
        self.driver.get(flask_job_postings_url)
        sign_in = self.driver.find_element(by=By.CSS_SELECTOR, value=('a[data-tracking-control-name='
                                                                      '"public_jobs_conversion-modal-signin"]'))
        time.sleep(2)
        sign_in_page_link = sign_in.get_attribute("href")
        self.driver.get(sign_in_page_link)
        username_box = self.driver.find_element(by=By.ID, value="username")
        username_box.send_keys(self.linkedin_username, Keys.TAB, self.linkedin_password, Keys.ENTER)
        input("Click here and press 'ENTER' after passing bot detection...")
        self.current_page = 1
        self.build_job_posting_list()

    def build_job_posting_list(self):
        job_title_link_class = "disabled ember-view job-card-container__link job-card-list__title"
        first_job_title_el = self.driver.find_element(by=By.CSS_SELECTOR, value=f"a[class='{job_title_link_class}']")
        for _ in range(10):
            first_job_title_el.send_keys(Keys.PAGE_DOWN)
        job_title_els = self.driver.find_elements(by=By.CSS_SELECTOR, value=f"a[class='{job_title_link_class}']")
        python_developer_job_title_els = [job for job in job_title_els
                                          if "Python" in job.text
                                          and "remote" not in job.text.lower()]
        for job in python_developer_job_title_els:
            print(job.text)
            self.apply_to_job(job)
        else:
            self.current_page += 1
            next_page_button = self.driver.find_element(by=By.CSS_SELECTOR,
                                                        value=f'button[aria-label="Page {self.current_page}"]')
            next_page_button.click()
            time.sleep(2)
            self.build_job_posting_list()

    def apply_to_job(self, job):
        job.click()
        time.sleep(1)

        # skips jobs you have already applied to
        try:
            easy_apply_button = self.driver.find_element(by=By.CSS_SELECTOR,
                                                         value='div[class="jobs-apply-button--top-card"]')
        except NoSuchElementException:
            return
        easy_apply_button.click()
        time.sleep(1)

        # do not follow company by default:
        try:
            follow_company_checkbox = self.driver.find_element(by=By.CSS_SELECTOR,
                                                               value='label[for="follow-company-checkbox"]')
            follow_company_checkbox.click()
            time.sleep(1)
        except NoSuchElementException:
            pass

        try:
            submit_application_button = self.driver.find_element(by=By.CSS_SELECTOR,
                                                                 value='button[aria-label="Submit application"]')
            submit_application_button.click()
            time.sleep(3)
            self.close_application()
        except NoSuchElementException:
            self.close_application()

    def close_application(self):
        dismiss_button = self.driver.find_element(by=By.CSS_SELECTOR,
                                                  value='button[aria-label="Dismiss"]')
        dismiss_button.click()
        time.sleep(1)
        try:
            confirm_button = self.driver.find_element(by=By.CSS_SELECTOR,
                                                      value=('button[data-control-name='
                                                             '"discard_application_confirm_btn"]'))
            confirm_button.click()
        except NoSuchElementException:
            print("Application submitted.")
            print()
        finally:
            time.sleep(1)


application = EasyApply()
