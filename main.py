import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver import ActionChains
import os
import dotenv
from selenium.webdriver.common.keys import Keys
# from datetime import datetime
# import re


class EasyApply:

    def __init__(self):
        dotenv.load_dotenv()
        self.linkedin_username = os.getenv("LINKEDIN_USERNAME")
        self.linkedin_password = os.getenv("LINKEDIN_PASSWORD")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        flask_job_postings_url = ("https://www.linkedin.com/jobs/search/?f_AL=true&f_T=25169&"
                                  "f_TPR=r604800&f_WT=2&geoId=103644278&keywords=flask")
        self.driver.get(flask_job_postings_url)
        sign_in = self.driver.find_element(by=By.CSS_SELECTOR, value=('a[data-tracking-control-name='
                                                                      '"public_jobs_conversion-modal-signin"]'))
        time.sleep(2)
        sign_in_page_link = sign_in.get_attribute("href")
        self.driver.get(sign_in_page_link)
        username_box = self.driver.find_element(by=By.ID, value="username")
        username_box.send_keys(self.linkedin_username, Keys.TAB, self.linkedin_password, Keys.ENTER)
        time.sleep(5)
        self.build_job_posting_list()

    def build_job_posting_list(self):
        job_title_link_class = "disabled ember-view job-card-container__link job-card-list__title"
        first_job_title_el = self.driver.find_element(by=By.CSS_SELECTOR, value=f"a[class='{job_title_link_class}']")
        for _ in range(10):
            first_job_title_el.send_keys(Keys.PAGE_DOWN)
        job_title_els = self.driver.find_elements(by=By.CSS_SELECTOR, value=f"a[class='{job_title_link_class}']")
        python_developer_job_title_els = [job for job in job_title_els if "Python Developer" in job.text]
        for job in python_developer_job_title_els:
            print(job.text)


application = EasyApply()
