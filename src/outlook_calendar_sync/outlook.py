from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from outlook_calendar_sync.utils import find_event, get_event

# from outlook_calendar_sync.utils import find_event, get_event, log


def outlook_login(
    driver,
    username: str,
    password: str,
    calendar_uri: str,
    auth_code=None,
    no_auth_code: bool = False,
):
    password = password.strip()
    driver.get(calendar_uri)

    driver.implicitly_wait(10)

    # username_field = driver.find_element(By.ID, "i0116")
    # signin_btn = driver.find_element(By.ID, "idSIButton9")
    username_field = driver.find_element(By.XPATH, r'//*[@id="i0116"]')
    signin_btn = driver.find_element(By.XPATH, r'//*[@id="idSIButton9"]')

    username_field.send_keys(username)
    signin_btn.click()

    # password_field = driver.find_element(By.ID, "passwordInput")
    # signin_btn_auth = driver.find_element(By.ID, "submitButton")
    password_field = driver.find_element(By.XPATH, r'//*[@id="passwordInput"]')
    signin_btn_auth = driver.find_element(By.XPATH, r'//*[@id="submitButton"]')

    # password_field.send_keys(password)
    password_field.send_keys(input("Password: "))
    signin_btn_auth.click()

    if not no_auth_code:
        # Handle 2fa
        auth_code_field = driver.find_element(By.ID, "idTxtBx_SAOTCC_OTC")
        auth_code_submit = driver.find_element(By.ID, "idSubmit_SAOTCC_Continue")

        if not auth_code:
            auth_code = input("Provide the authenticator code: ")

        auth_code_field.send_keys(auth_code)
        auth_code_submit.click()

    stay_signed_in_btn = driver.find_element(By.ID, "idBtn_Back")
    stay_signed_in_btn.click()

    return driver


def outlook_select_page_events(driver, days=1, delay=5):
    sleep(delay)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    yield [get_event(i["aria-label"]) for i in soup.find_all(find_event)]

    for _ in range(days - 1):
        next_page = driver.find_element(By.XPATH, '//*[@id="MainModule"]/div[3]/div/div[1]/div[1]/button[3]')
        next_page.click()
        sleep(delay)

        # Dump the page source into BS
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        yield [get_event(i["aria-label"]) for i in soup.find_all(find_event)]

        # Get the next page

    driver.quit()


def get_selenium_driver(debug=False):
    chrome_opt = Options()
    if not debug:
        chrome_opt.add_argument("--headless")
    chrome_opt.add_argument("executable_path=/usr/local/bin/chromedriver")
    return webdriver.Chrome(options=chrome_opt)
