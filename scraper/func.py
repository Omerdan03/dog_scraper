import re
from bs4 import BeautifulSoup

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import random
from csv import writer
from tqdm import tqdm

from . import const

def print_html(element):
    html_text = element.get_attribute("outerHTML")
    soup = BeautifulSoup(html_text, 'html.parser')
    print(soup.prettify())


def get_driver(chrome_options):
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(const.URL)

    lan_div = driver.find_element(By.ID, 'LangDD')
    if lan_div.text == 'English':
        lan_div.click()
        lan_div = driver.find_element(By.ID, 'LangDD')
        lan_div.find_element(By.XPATH, "//li[@aria-label='עברית']").click()

    return driver

def add_header(file):
    with open(file, 'w') as csvfile:
        writer_object = writer(csvfile)
        writer_object.writerow(['chip_number'] + const.ELEMENT_LIST)


def get_element(table, element_id):
    try:
        element = table.find_element(By.ID, f'for-{element_id}').text
    except NoSuchElementException:
        element = -1
    return element


def get_dog_info(driver, chip):
    input_box = driver.find_elements(By.XPATH, "//input")[1]
    input_box.clear()
    input_box.send_keys(chip)
    driver.find_element(By.ID, 'locPetButton').click()
    time.sleep(const.DELAY_SEC/2)
    try:
        table = driver.find_element(By.ID, '0print')
    except NoSuchElementException:
        try:
            time.sleep(const.DELAY_SEC/2)
            table = driver.find_element(By.ID, '0print')
        except NoSuchElementException:
            return [chip] + [-1] * len(const.ELEMENT_LIST)
    chip_num = driver.find_element(By.ID, 'head_resulte').text
    chip_num = re.findall(r'\d+', chip_num)[0]
    return [chip_num] + [get_element(table, element) for element in const.ELEMENT_LIST]


def write_dog_info(chrome_options, chip_num):
    driver = get_driver(chrome_options)

    driver.get(const.URL)
    dog_info = get_dog_info(driver, chip_num)
    with open(const.OUTPUT_FILE, 'a') as file:
        writer_object = writer(file)
        writer_object.writerow(dog_info)
        file.close()
    print(chip_num)