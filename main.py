import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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
        flask_job_postings_url = ("https://www.linkedin.com/jobs/search/?currentJobId=3453175796&f_AL=true&"
                                  "f_E=2&f_JT=F&f_T=25169&f_WT=2&geoId=103644278&keywords=flask&"
                                  "location=United%20States&"
                                  "refresh=true&sortBy=DD")
        self.driver.get(flask_job_postings_url)
        sign_in = self.driver.find_element(by=By.CSS_SELECTOR, value=('a[data-tracking-control-name='
                                                                      '"public_jobs_conversion-modal-signin"]'))
        time.sleep(2)
        sign_in_page_link = sign_in.get_attribute("href")
        self.driver.get(sign_in_page_link)
        username_box = self.driver.find_element(by=By.ID, value="username")
        username_box.send_keys(self.linkedin_username, Keys.TAB, self.linkedin_password, Keys.ENTER)


application = EasyApply()
