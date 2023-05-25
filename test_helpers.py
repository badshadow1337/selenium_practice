from selenium.webdriver.remote.webelement import WebElement
from selenium.common import NoSuchElementException


def check_el_by_xpath(webelement: WebElement):
    try:
        webelement
    except NoSuchElementException:
        return False
    return True


# def image_checker(image: WebElement):
#     if image.get_attribute("naturalWidth") == 0:
#         print(image.get_attribute("outerHTML") + "is broken")
