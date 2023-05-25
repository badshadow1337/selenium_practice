import time
import re
import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from test_helpers import check_element
from selenium.common import NoSuchElementException

import requests

driver = webdriver.Firefox()
driver.maximize_window()


class Test:

    def test_app1_ABTesting(self):
        driver.get("https://the-internet.herokuapp.com/abtest")
        h3 = driver.find_element(By.TAG_NAME, 'h3')

        assert "A/B Test Variation 1" in h3.text
        time.sleep(1)

    def test_app2_AddRemoveElements(self):
        driver.get("https://the-internet.herokuapp.com/add_remove_elements/")
        add_button = driver.find_element(By.XPATH, "//*[@id='content']/div/button")

        for i in range(5):
            add_button.click()

        del_button = driver.find_element(By.XPATH, f"//*[@id='elements']/button[1]")

        check_element(del_button)

        for k in range(5):
            driver.find_element(By.XPATH, f"//*[@id='elements']/button[1]").click()
            # del_button.click()

        check_element(del_button)

        time.sleep(1)

    def test_app3_BasicAuth(self):
        login = "admin"
        driver.get(f"http://{login}:{login}@the-internet.herokuapp.com/basic_auth")
        p = driver.find_element(By.TAG_NAME, "p")
        assert "Congratulations! You must have the proper credentials." in p.text

    def test_app4_BrokenImages(self):
        driver.get("https://the-internet.herokuapp.com/broken_images")
        images = driver.find_elements(By.TAG_NAME, "img")
        broken_img = 0
        for img in images:
            response = requests.get(img.get_attribute('src'), stream=True)
            if response.status_code != 200:
                broken_img += 1
        assert broken_img == 2

    def test_app5_ChallengingDOM(self):
        driver.get("https://the-internet.herokuapp.com/challenging_dom")
        assert driver.find_element(By.XPATH,
                                   '//*[@id="content"]/div/div/div/div[2]/table/thead/tr/th[1]').text == "Lorem"
        assert driver.find_element(By.XPATH,
                                   '//*[@id="content"]/div/div/div/div[2]/table/thead/tr/th[2]').text == "Ipsum"
        assert driver.find_element(By.XPATH,
                                   '//*[@id="content"]/div/div/div/div[2]/table/thead/tr/th[3]').text == "Dolor"
        assert driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[2]/table/thead/tr/th[4]').text == "Sit"
        assert driver.find_element(By.XPATH,
                                   '//*[@id="content"]/div/div/div/div[2]/table/thead/tr/th[5]').text == "Amet"
        assert driver.find_element(By.XPATH,
                                   '//*[@id="content"]/div/div/div/div[2]/table/thead/tr/th[6]').text == "Diceret"
        assert driver.find_element(By.XPATH,
                                   '//*[@id="content"]/div/div/div/div[2]/table/thead/tr/th[7]').text == "Action"

        assert driver.find_element(By.XPATH,
                                   '//*[@id="content"]/div/div/div/div[2]/table/tbody/tr[1]/td[1]').text == "Iuvaret0"
        assert driver.find_element(By.XPATH,
                                   '//*[@id="content"]/div/div/div/div[2]/table/tbody/tr[2]/td[2]').text == "Apeirian1"
        assert driver.find_element(By.XPATH,
                                   '//*[@id="content"]/div/div/div/div[2]/table/tbody/tr[3]/td[3]').text == "Adipisci2"
        assert driver.find_element(By.XPATH,
                                   '//*[@id="content"]/div/div/div/div[2]/table/tbody/tr[4]/td[4]').text == "Definiebas3"
        assert driver.find_element(By.XPATH,
                                   '//*[@id="content"]/div/div/div/div[2]/table/tbody/tr[5]/td[5]').text == "Consequuntur4"
        assert driver.find_element(By.XPATH,
                                   '//*[@id="content"]/div/div/div/div[2]/table/tbody/tr[6]/td[6]').text == "Phaedrum5"
        assert driver.find_element(By.XPATH,
                                   '//*[@id="content"]/div/div/div/div[2]/table/tbody/tr[7]/td[7]').text == "edit delete"

        # button 1
        el1 = driver.find_element(By.XPATH, '//div[@class="large-2 columns"]/a[@class="button"]')
        button_id = el1.get_attribute("id")
        el1.click()
        el1 = driver.find_element(By.XPATH, '//div[@class="large-2 columns"]/a[@class="button"]')
        assert el1.get_attribute("id") != button_id

        # button 2
        el2 = driver.find_element(By.XPATH, '//div[@class="large-2 columns"]/a[@class="button alert"]')
        button_id = el2.get_attribute("id")
        el2.click()
        el2 = driver.find_element(By.XPATH, '//div[@class="large-2 columns"]/a[@class="button alert"]')
        assert el2.get_attribute("id") != button_id

        # button 3
        el3 = driver.find_element(By.XPATH, '//div[@class="large-2 columns"]/a[@class="button success"]')
        button_id = el3.get_attribute("id")
        el3.click()
        el3 = driver.find_element(By.XPATH, '//div[@class="large-2 columns"]/a[@class="button success"]')
        assert el3.get_attribute("id") != button_id

        script_block = driver.find_element(By.XPATH, '//div[@id="content"]/script').get_attribute('innerHTML')
        first_answer = re.search(r"Answer:\s(\d+)", script_block).group(1)
        driver.refresh()
        script_block = driver.find_element(By.XPATH, '//div[@id="content"]/script').get_attribute('innerHTML')
        second_answer = re.search(r"Answer:\s(\d+)", script_block).group(1)

        assert first_answer != second_answer

    def test_app6_Checkboxes(self):
        driver.get("https://the-internet.herokuapp.com/checkboxes")
        checkbox1 = driver.find_element(By.XPATH, '//*[@id="checkboxes"]/input[1]')
        checkbox2 = driver.find_element(By.XPATH, '//*[@id="checkboxes"]/input[2]')

        checkbox1.click()
        checkbox2.click()

        assert checkbox1.is_selected() == True
        assert checkbox2.is_selected() == False

    def test_app7_ContextMenu(self):
        driver.get("https://the-internet.herokuapp.com/context_menu")
        hotspot = driver.find_element(By.XPATH, '//*[@id="hot-spot"]')
        actions = ActionChains(driver)
        actions.context_click(hotspot).perform()
        alert = driver.switch_to.alert
        assert alert.text == "You selected a context menu"
        alert.accept()

    def test_app8_DigestAuthentication(self):
        login = "admin"
        driver.get(f"http://{login}:{login}@the-internet.herokuapp.com/digest_auth")
        p = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/p')
        assert p.text == "Congratulations! You must have the proper credentials."

    def test_app9_DisappearingElements(self):
        driver.get("https://the-internet.herokuapp.com/disappearing_elements")
        # disappearing_el = driver.find_element(By.XPATH, '//*[@id="content"]/div/ul/li[5]/a')
        for i in range(7):
            try:
                driver.find_element(By.XPATH, '//*[@id="content"]/div/ul/li[5]/a')
            except NoSuchElementException:
                driver.refresh()
            else:
                driver.find_element(By.XPATH, '//*[@id="content"]/div/ul/li[5]/a').click()
                break
        assert driver.find_element(By.XPATH, '/html/body/h1').text == "Not Found"

    # dont work
    def test_app10_DragandDrop(self):
        driver.get("https://the-internet.herokuapp.com/drag_and_drop")
        a = driver.find_element(By.ID, 'column-a')
        b = driver.find_element(By.ID, 'column-b')
        aCol = driver.find_element(By.XPATH, '//*[@id="column-a"]/header')
        bCol = driver.find_element(By.XPATH, '//*[@id="column-b"]/header')

        assert aCol.text == "A"
        assert bCol.text == "B"

        # actions = ActionChains(driver)
        # actions.move_to_element(a).click_and_hold().move_to_element(b).release().perform()
        # actions.click_and_hold(a).release(b).perform()
        # actions.drag_and_drop(a,b)
        #
        # assert aCol.text == "B"
        # assert bCol.text == "A"

        # driver.close()
