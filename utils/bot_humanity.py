import time
import random
import logging

from undetected_chromedriver import WebElement


logger = logging.getLogger(__name__)

def simulate_input_in_element(element_input: WebElement, text):
    logger.info('Input text')
    try:
        element_input.clear()
    except:
        pass
    for i in list(text):
        try:
            element_input.send_keys(f'{i}')
            time.sleep(float(f'0.{random_sleep()}'))
        except:
            pass


def random_sleep(minimum=1, maximum=2):
    time.sleep(random.uniform(minimum, maximum))
