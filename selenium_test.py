import os.path
import time
import re

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from test_helpers import element_exists
from test_helpers import img_checker
from selenium.common import NoSuchElementException

driver = webdriver.Firefox()


class Test:

    def test_app1_abtest(self):
        driver.get("https://the-internet.herokuapp.com/abtest")
        h3 = driver.find_element(By.TAG_NAME, 'h3')

        assert "A/B Test Control" or "A/B Test Variation 1" in h3.text

    def test_app2_add_remove_elements(self):
        driver.get("https://the-internet.herokuapp.com/add_remove_elements/")
        add_button = driver.find_element(By.XPATH, "//*[@id='content']/div/button")

        for i in range(5):
            add_button.click()

        del_button = driver.find_element(By.XPATH, f"//*[@id='elements']/button[1]")

        assert element_exists(del_button) == True

        for k in range(5):
            driver.find_element(By.XPATH, f"//*[@id='elements']/button[1]").click()
            # del_button.click()

        assert element_exists(del_button) == True

    def test_app3_basic_auth(self):
        login = "admin"
        driver.get(f"http://{login}:{login}@the-internet.herokuapp.com/basic_auth")
        p = driver.find_element(By.TAG_NAME, "p")
        assert "Congratulations! You must have the proper credentials." in p.text

    def test_app4_broken_images(self):
        driver.get("https://the-internet.herokuapp.com/broken_images")
        images = driver.find_elements(By.TAG_NAME, "img")

        assert img_checker(images) == 2

    def test_app5_challenging_dom(self):
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

    def test_app6_checkboxes(self):
        driver.get("https://the-internet.herokuapp.com/checkboxes")
        checkbox1 = driver.find_element(By.XPATH, '//*[@id="checkboxes"]/input[1]')
        checkbox2 = driver.find_element(By.XPATH, '//*[@id="checkboxes"]/input[2]')

        checkbox1.click()
        checkbox2.click()

        assert checkbox1.is_selected() == True
        assert checkbox2.is_selected() == False

    # def test_app7_context_menu(self):
    #     driver.get("https://the-internet.herokuapp.com/context_menu")
    #     hotspot = driver.find_element(By.XPATH, '//*[@id="hot-spot"]')
    #     ActionChains(driver).context_click(hotspot).perform()
    #     alert = driver.switch_to.alert
    #     assert alert.text == "You selected a context menu"
    #     alert.accept()

    # def test_app8_DigestAuthentication(self):
    #     login = "admin"
    #     driver.get(f"http://{login}:{login}@the-internet.herokuapp.com/digest_auth")
    #     p = driver.find_element(By.TAG_NAME, "p")
    #     assert p.text == "Congratulations! You must have the proper credentials."

    def test_app9_disappearing_elements(self):
        driver.get("https://the-internet.herokuapp.com/disappearing_elements")
        for i in range(7):
            try:
                driver.find_element(By.XPATH, '//*[@id="content"]/div/ul/li[5]/a')
            except NoSuchElementException:
                driver.refresh()
            else:
                driver.find_element(By.XPATH, '//*[@id="content"]/div/ul/li[5]/a').click()
                break
        assert driver.find_element(By.XPATH, '/html/body/h1').text == "Not Found"

    # def test_app10_drag_and_drop(self):
    #     driver.get("https://the-internet.herokuapp.com/drag_and_drop")
    #     a = driver.find_element(By.ID, 'column-a')
    #     b = driver.find_element(By.ID, 'column-b')
    #     aCol = driver.find_element(By.XPATH, '//*[@id="column-a"]/header')
    #     bCol = driver.find_element(By.XPATH, '//*[@id="column-b"]/header')
    #
    #     assert aCol.text == "A"
    #     assert bCol.text == "B"
    #
    #     actions = ActionChains(driver)
    #     actions.drag_and_drop(a,b).perform()
    #
    #     assert aCol.text == "B"
    #     assert bCol.text == "A"

    def test_app11_dropdown(self):
        driver.get("https://the-internet.herokuapp.com/dropdown")
        select = driver.find_element(By.XPATH, '//*[@id="dropdown"]')
        opt1 = driver.find_element(By.XPATH, '//*[@id="dropdown"]/option[2]')
        opt2 = driver.find_element(By.XPATH, '//*[@id="dropdown"]/option[3]')

        select.click()
        opt1.click()
        assert opt1.is_selected() == True
        assert opt2.is_selected() == False

        select.click()
        opt2.click()
        assert opt2.is_selected() == True
        assert opt1.is_selected() == False

    def test_app12_dynamic_content(self):
        driver.get('https://the-internet.herokuapp.com/dynamic_content')
        images = driver.find_elements(By.TAG_NAME, 'img')
        txt = 0

        assert img_checker(images) == 0

        for i in range(1, 4):
            driver.find_element(By.XPATH, f'//*[@id="content"]/div[{i}]/div[2]')
            if driver.find_element(By.XPATH, f'//*[@id="content"]/div[{i}]/div[2]').text.replace(" ", "")[
               0:9].isalpha():
                txt += 1
        assert txt == 3

    def test_app13_dynamic_Controls(self):
        driver.get('https://the-internet.herokuapp.com/dynamic_controls')
        checkbox = driver.find_element(By.XPATH, '//*[@id="checkbox"]/input')
        but_checkbox = driver.find_element(By.XPATH, '//*[@id="checkbox-example"]/button')
        inputt = driver.find_element(By.XPATH, '//*[@id="input-example"]/input')
        but_input = driver.find_element(By.XPATH, '//*[@id="input-example"]/button')

        assert element_exists(checkbox) == True
        but_checkbox.click()
        time.sleep(5)
        try:
            driver.find_element(By.XPATH, '//*[@id="checkbox"]/input')
        except NoSuchElementException:
            input_exist = True
        else:
            input_exist = False
        assert input_exist == True

        assert inputt.is_enabled() == False
        but_input.click()
        time.sleep(5)
        assert inputt.is_enabled() == True

    def test_app14_dynamic_loading(self):
        driver.get('https://the-internet.herokuapp.com/dynamic_loading')
        wait = WebDriverWait(driver, 10)

        driver.find_element(By.XPATH, '//*[@id="content"]/div/a[1]').click()
        driver.find_element(By.XPATH, '//*[@id="start"]/button').click()
        result1 = wait.until(expected_conditions.visibility_of_element_located((By.ID, 'finish')))
        assert result1.text == 'Hello World!'

        driver.back()

        driver.find_element(By.XPATH, '//*[@id="content"]/div/a[2]').click()
        driver.find_element(By.XPATH, '//*[@id="start"]/button').click()
        result2 = wait.until(expected_conditions.visibility_of_element_located((By.ID, 'finish')))
        assert result2.text == 'Hello World!'

    def test_app15_entry_ad(self):
        driver.get('https://the-internet.herokuapp.com/entry_ad')
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="modal"]/div[2]/div[3]/p').click()

    # def test_app16_exit_intent(self):
    #     driver.get('https://the-internet.herokuapp.com/exit_intent')

    def test_app17_download(self):
        driver.get('https://the-internet.herokuapp.com/download')
        file_name = driver.find_element(By.XPATH, '//*[@id="content"]/div/a[1]').text
        driver.find_element(By.XPATH, '//*[@id="content"]/div/a[1]').click()
        file_path = fr'C:\Users\1chud\Downloads\{file_name}'
        time.sleep(2)
        if os.path.exists(file_path):
            file = True
        else:
            file = False
        assert file == True

    def test_app18_upload(self):
        driver.get('https://the-internet.herokuapp.com/upload')
        file_path = r'C:\Users\1chud\Downloads\ChatGPTbot.png'
        driver.find_element(By.XPATH, '//*[@id="file-upload"]').send_keys(file_path)
        driver.find_element(By.XPATH, '//*[@id="file-submit"]').click()
        file_result = driver.find_element(By.XPATH, '//*[@id="uploaded-files"]').text
        assert file_result == file_path.rpartition('\\')[2]

    def test_app19_floating_menu(self):
        driver.get('https://the-internet.herokuapp.com/floating_menu')
        home_url = 'https://the-internet.herokuapp.com/floating_menu#home'
        news_url = 'https://the-internet.herokuapp.com/floating_menu#news'
        contact_url = 'https://the-internet.herokuapp.com/floating_menu#contact'
        about_url = 'https://the-internet.herokuapp.com/floating_menu#about'

        driver.find_element(By.XPATH, '//*[@id="menu"]/ul/li[1]/a').click()
        assert driver.current_url == home_url
        driver.find_element(By.XPATH, '//*[@id="menu"]/ul/li[2]/a').click()
        assert driver.current_url == news_url
        driver.find_element(By.XPATH, '//*[@id="menu"]/ul/li[3]/a').click()
        assert driver.current_url == contact_url
        driver.find_element(By.XPATH, '//*[@id="menu"]/ul/li[4]/a').click()
        assert driver.current_url == about_url

    def test_app20_forgot_password(self):
        driver.get('https://the-internet.herokuapp.com/forgot_password')
        driver.find_element(By.ID,'email').send_keys('zxc@gmail.com')
        driver.find_element(By.ID,'form_submit').click()
        res = driver.find_element(By.TAG_NAME,'h1')
        assert res.text == 'Internal Server Error'

        driver.close()
