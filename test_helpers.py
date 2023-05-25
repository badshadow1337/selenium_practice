from selenium.webdriver.remote.webelement import WebElement
from selenium.common import NoSuchElementException
from selenium import webdriver



def check_element(webelement: WebElement):
    try:
        webelement
    except NoSuchElementException:
        return False
    return True

# def image_checker(image: WebElement):
#     if image.get_attribute("naturalWidth") == 0:
#         print(image.get_attribute("outerHTML") + "is broken")
