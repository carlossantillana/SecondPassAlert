from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import requests
import json
import time

TIMEOUT = 90
WEBHOOK_URL = "https://hooks.slack.com/services/you/incoming/slackwebhook"
TERM = "20W"
RETRY_TIMER = 60.0 * 15
USERNAME = "enter username"
PASSWORD = "enter password"

def slackMessage(message):
    webhook_url = WEBHOOK_URL
    slack_data = {'text': message}

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
            )

def login():
    driver.add_cookie({'name': 'iwe_term_student', 'value': TERM, 'path': '/', 'domain': '.ucla.edu'})
    driver.find_element_by_id("logon").send_keys(USERNAME)
    driver.find_element_by_id ("pass").send_keys(PASSWORD)
    driver.find_element_by_class_name("primary-button").click()

driver = webdriver.Chrome()
driver.get ("https://sa.ucla.edu/ro/classsearch/Enrollment/Appointments")
login()
starttime = time.time()
while True:
    if time.localtime().tm_hour >= 8 and time.localtime().tm_hour < 17:
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'span4'))
            WebDriverWait(driver, TIMEOUT).until(element_present)
        except TimeoutException:
            print("you have been logged out. ")
        try:
            maxUnits = driver.find_elements_by_class_name("span4")[1].text
        except IndexError:
            driver.refresh()
            login()
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'span4'))
            WebDriverWait(driver, TIMEOUT).until(element_present)
            maxUnits = driver.find_elements_by_class_name("span4")[1].text
        if float(maxUnits) <= 8:
            slackMessage("still at 8 units") 
        else:
            slackMessage("@here registration open!")
    time.sleep(RETRY_TIMER - ((time.time() - starttime) % RETRY_TIMER))
    driver.refresh();
