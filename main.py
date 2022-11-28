import argparse
import threading
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

from scraper import const, Scraper


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

    parser.add_argument('-thredlimit', '-limit', metavar='thred_limits', default=-1, type=int,
                        help='limiting number of threads opened.')

    args = parser.parse_args()

    chrome_options = Options()
    if args.debug:
        chrome_options.add_argument("--headless")
    if args.thredlimit != -1:
        thread_limiter = threading.BoundedSemaphore(args.thredlimit)
    else:
        pass

    scraper_options = {'chrome_options': chrome_options,
                       'new_file': True}
    scraper = Scraper(thread_limiter, const.OUTPUT_FILE, scraper_options)
    start = 900032001799568
    number_queries = 100
    for chip_num in range(start, start + number_queries):
        tread = threading.Thread(target=scraper.run, args=[chip_num])
        tread.start()


if __name__ == '__main__':
    main()
