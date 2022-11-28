import re
from pathlib import Path
from csv import writer
import threading
import time

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from . import const

driver_location = ChromeDriverManager().install()

def get_driver(chrome_options) -> webdriver.chrome.webdriver.WebDriver:
    """
    This functuion returns new chrome driver using the given options
    :param chrome_options:
    :return:
    """
    driver = webdriver.Chrome(options=chrome_options,
                              executable_path=driver_location)
    driver.get(const.URL)

    lan_div = driver.find_element(By.ID, 'LangDD')
    if lan_div.text == 'English':
        lan_div.click()
        lan_div = driver.find_element(By.ID, 'LangDD')
        lan_div.find_element(By.XPATH, "//li[@aria-label='עברית']").click()

    return driver


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
        table = driver.find_element(By.CLASS_NAME, 'body_resulte')
    except NoSuchElementException:
        try:
            time.sleep(const.DELAY_SEC/2)
            table = driver.find_element(By.CLASS_NAME, 'body_resulte')
        except NoSuchElementException:
            return [chip] + [-1] * len(const.ELEMENT_LIST)
    chip_num = driver.find_element(By.ID, 'head_resulte').text
    chip_num = re.findall(r'\d+', chip_num)[0]
    return [chip_num] + [get_element(table, element) for element in const.ELEMENT_LIST]


class Scraper(threading.Thread):

    def __init__(self, thread_limiter: threading.BoundedSemaphore, output: Path, options: dict):
        super().__init__()
        self.output = Path(output)
        self.thread_limiter = thread_limiter
        self.chrome_options = options['chrome_options']
        if options['new_file'] or not self.output.exists():
            self.create_file()

    def create_file(self):
        """
        This function opened the create new csv file with only header in the output location
        :return: None
        """
        with open(self.output, 'w', newline='') as csvfile:
            writer_object = writer(csvfile)
            writer_object.writerow(['chip_number'] + const.ELEMENT_LIST)

    def run(self, chip_num):
        self.thread_limiter.acquire()
        try:
            self.scrap_dog_info(chip_num)
        finally:
            self.thread_limiter.release()

    def scrap_dog_info(self, chip_num):
        driver = get_driver(self.chrome_options)

        driver.get(const.URL)
        dog_info = get_dog_info(driver, chip_num)
        with open(const.OUTPUT_FILE, 'a', newline='') as file:
            writer_object = writer(file)
            writer_object.writerow(dog_info)
            file.close()
