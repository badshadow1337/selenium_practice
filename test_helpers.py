from selenium.webdriver.remote.webelement import WebElement
from selenium.common import NoSuchElementException, StaleElementReferenceException
import requests


def element_exists(webelement: WebElement):
    try:
        webelement
    except NoSuchElementException:
        return False
    except StaleElementReferenceException:
        return False
    else:
        return True


# def element_does_not_exists(webelement: WebElement):
#     try:
#         webelement
#     except NoSuchElementException:
#         return True
#     else:
#         return False


def img_checker(images: list[WebElement]):
    broken_img = 0
    for img in images:
        response = requests.get(img.get_attribute('src'), stream=True)
        if response.status_code != 200:
            broken_img += 1
    return broken_img

