import argparse
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

from scraper import func

import threading

def str2bool(str):
    if isinstance(str, bool):
        return str
    if str.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif str.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    parser = argparse.ArgumentParser(
        prog='dog_scraper',
        formatter_class=argparse.RawTextHelpFormatter,
        description="Runs the scrapper")

    parser.add_argument('-debug', metavar='debug_mode', default=False, type=str2bool,
                        help='option for running with or without debugging.')

    args = parser.parse_args()


    chrome_options = Options()

    if args.debug:
        chrome_options.add_argument("--headless")

    #func.add_header(OUTPUT_FILE)

    start = 900032001799568
    for chip_num in tqdm(range(start, start + 500)):
        tread = threading.Thread(target=func.write_dog_info, args=(chrome_options, chip_num))
        tread.start()


if __name__ == '__main__':
    main()
