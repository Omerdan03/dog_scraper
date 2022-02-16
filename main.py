import re
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import random
from csv import writer
from tqdm import tqdm

import threading

URL = 'https://dogsearch.moag.gov.il/#/pages/pets'
ELEMENT_LIST = ['name', 'gender', 'breed', 'birthDate', 'owner', 'address', 'city', 'phone1', 'phone2',
                'neutering', 'rabies-vaccine', 'rabies-vaccine-date', 'vet', 'viewReport', 'license',
                'license-date-start', 'domain', 'license-latest-update', 'status']
OUTPUT_FILE = 'dogs.csv'
DELAY_SEC = 5


def print_html(element):
    html_text = element.get_attribute("outerHTML")
    soup = BeautifulSoup(html_text, 'html.parser')
    print(soup.prettify())


def get_driver(chrome_options):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)

    lan_div = driver.find_element(By.ID, 'LangDD')
    if lan_div.text == 'English':
        lan_div.click()
        lan_div = driver.find_element(By.ID, 'LangDD')
        lan_div.find_element(By.XPATH, "//li[@aria-label='עברית']").click()

    return driver

def add_header(file):
    with open(file, 'w') as csvfile:
        writer_object = writer(csvfile)
        writer_object.writerow(['chip_number'] + ELEMENT_LIST)


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
    time.sleep(DELAY_SEC/2)
    try:
        table = driver.find_element(By.ID, '0print')
    except NoSuchElementException:
        try:
            time.sleep(DELAY_SEC/2)
            table = driver.find_element(By.ID, '0print')
        except NoSuchElementException:
            return [chip] + [-1] * len(ELEMENT_LIST)
    chip_num = driver.find_element(By.ID, 'head_resulte').text
    chip_num = re.findall(r'\d+', chip_num)[0]
    return [chip_num] + [get_element(table, element) for element in ELEMENT_LIST]


def write_dog_info(chrome_options, chip_num):
    driver = get_driver(chrome_options)
    driver.get(URL)
    dog_info = get_dog_info(driver, chip_num)
    with open(OUTPUT_FILE, 'a') as file:
        writer_object = writer(file)
        writer_object.writerow(dog_info)
        file.close()
    print(chip_num)


def main(debug=True):
    chrome_options = Options()

    if not debug:
        chrome_options.add_argument("--headless")

    add_header(OUTPUT_FILE)

    start = 900032001799568
    for chip_num in tqdm(range(start, start + 10)):
        tread = threading.Thread(target=write_dog_info, args=(chrome_options, chip_num))
        tread.start()


if __name__ == '__main__':
    main(debug=False)
