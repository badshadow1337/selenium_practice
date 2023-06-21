import os.path
import time
import re
import requests

import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from test_helpers import element_exists
from test_helpers import img_checker
from selenium.common import NoSuchElementException

driver = webdriver.Chrome()


@pytest.mark.all
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

    @pytest.mark.skip
    def test_app7_context_menu(self):
        driver.get("https://the-internet.herokuapp.com/context_menu")
        hotspot = driver.find_element(By.XPATH, '//*[@id="hot-spot"]')
        ActionChains(driver).context_click(hotspot).perform()
        alert = driver.switch_to.alert
        assert alert.text == "You selected a context menu"
        alert.accept()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="content"]/div/h3').click()

    @pytest.mark.skip
    def test_app8_DigestAuthentication(self):
        login = "admin"
        driver.get(f"http://{login}:{login}@the-internet.herokuapp.com/digest_auth")
        p = driver.find_element(By.TAG_NAME, "p")
        assert p.text == "Congratulations! You must have the proper credentials."

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

    @pytest.mark.skip
    def test_app10_drag_and_drop(self):
        driver.get("https://the-internet.herokuapp.com/drag_and_drop")
        a = driver.find_element(By.ID, 'column-a')
        b = driver.find_element(By.ID, 'column-b')
        aCol = driver.find_element(By.XPATH, '//*[@id="column-a"]/header')
        bCol = driver.find_element(By.XPATH, '//*[@id="column-b"]/header')

        assert aCol.text == "A"
        assert bCol.text == "B"

        ActionChains(driver).drag_and_drop(a, b).perform()

        assert aCol.text == "B"
        assert bCol.text == "A"

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

    @pytest.mark.skip
    def test_app16_exit_intent(self):
        driver.get('https://the-internet.herokuapp.com/exit_intent')

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
        driver.find_element(By.ID, 'email').send_keys('zxc@gmail.com')
        driver.find_element(By.ID, 'form_submit').click()
        res = driver.find_element(By.TAG_NAME, 'h1')
        assert res.text == 'Internal Server Error'

    def test_app21_login(self):
        driver.get('https://the-internet.herokuapp.com/login')
        driver.find_element(By.ID, 'username').send_keys('tomsmith')
        driver.find_element(By.ID, 'password').send_keys('SuperSecretPassword!')
        driver.find_element(By.XPATH, '//*[@id="login"]/button').click()
        finish_text = driver.find_element(By.CLASS_NAME, 'subheader').text
        assert finish_text == 'Welcome to the Secure Area. When you are done click logout below.'

    def test_app22_frames(self):
        driver.get('https://the-internet.herokuapp.com/frames')
        driver.find_element(By.XPATH, '//*[@id="content"]/div/ul/li[2]/a').click()
        text_area_size = int(driver.find_element(By.XPATH, '//*[@id="content"]/div/div').size['height'])
        assert text_area_size == 200
        ActionChains(driver).drag_and_drop_by_offset(
            driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[2]/div[2]'), 0, 20).perform()
        text_area_size = int(driver.find_element(By.XPATH, '//*[@id="content"]/div/div').size['height'])
        assert text_area_size == 218

    # def test_app23_geolocation(self):

    def test_app24_horizontal_slider(self):
        driver.get('https://the-internet.herokuapp.com/horizontal_slider')
        slider = driver.find_element(By.TAG_NAME, 'input')
        for i in range(0, 4):
            slider.send_keys(Keys.ARROW_RIGHT)
        assert driver.find_element(By.ID, 'range').text == '2'

    def test_app25_hovers(self):
        driver.get('https://the-internet.herokuapp.com/hovers')

        img1 = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/img')
        ActionChains(driver).move_to_element(img1).perform()
        driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div/a').click()
        time.sleep(1)
        assert driver.current_url == 'https://the-internet.herokuapp.com/users/1'
        driver.back()

        img2 = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/img')
        ActionChains(driver).move_to_element(img2).perform()
        driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/a').click()
        time.sleep(1)
        assert driver.current_url == 'https://the-internet.herokuapp.com/users/2'
        driver.back()

        img3 = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/img')
        ActionChains(driver).move_to_element(img3).perform()
        driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/a').click()
        time.sleep(1)
        assert driver.current_url == 'https://the-internet.herokuapp.com/users/3'

    @pytest.mark.skip
    def test_app26_infinite_scroll(self):
        driver.get('https://the-internet.herokuapp.com/infinite_scroll')

    def test_apps27_inputs(self):
        driver.get('https://the-internet.herokuapp.com/inputs')
        inp = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/input')
        inp.send_keys(-222)
        assert inp.get_attribute('value') == '-222'
        inp.clear()
        inp.send_keys(222)
        assert inp.get_attribute('value') == '222'

    def test_apps28_jqueryui_menu(self):
        driver.get('https://the-internet.herokuapp.com/jqueryui/menu')
        a = driver.find_element(By.XPATH, '//*[@id="ui-id-3"]/a')
        b = driver.find_element(By.XPATH, '//*[@id="ui-id-4"]/a')
        c = driver.find_element(By.XPATH, '//*[@id="ui-id-6"]/a')
        ActionChains(driver).move_to_element(a).perform()
        time.sleep(1)
        ActionChains(driver).move_to_element(b).perform()
        assert c.get_attribute('href') == 'https://the-internet.herokuapp.com/download/jqueryui/menu/menu.csv'

    def test_app29_javascript_alerts(self):
        driver.get('https://the-internet.herokuapp.com/javascript_alerts')
        res = driver.find_element(By.XPATH, '//*[@id="result"]')
        driver.find_element(By.XPATH, '//*[@id="content"]/div/ul/li[1]/button').click()
        alert = driver.switch_to.alert
        alert.accept()
        assert res.text == 'You successfully clicked an alert'

        driver.find_element(By.XPATH, '//*[@id="content"]/div/ul/li[2]/button').click()
        alert = driver.switch_to.alert
        alert.dismiss()
        assert res.text == 'You clicked: Cancel'

        driver.find_element(By.XPATH, '//*[@id="content"]/div/ul/li[3]/button').click()
        alert = driver.switch_to.alert
        alert.send_keys('selenium')
        alert.accept()
        assert res.text == 'You entered: selenium'

    @pytest.mark.skip
    def test_app30_javascript_error(self):
        driver.get('https://the-internet.herokuapp.com/javascript_error')

    def test_app31_key_presses(self):
        driver.get('https://the-internet.herokuapp.com/key_presses')
        inp = driver.find_element(By.ID, 'target')
        res = driver.find_element(By.ID, 'result')
        inp.send_keys('z')
        assert res.text == 'You entered: Z'
        inp.send_keys('7')
        assert res.text == 'You entered: 7'
        inp.send_keys(Keys.CONTROL)
        assert res.text == 'You entered: CONTROL'

    def test_app32_large(self):
        driver.get('https://the-internet.herokuapp.com/large')
        latest = driver.find_element(By.ID, 'sibling-50.3')
        assert latest.text == '50.3'
        table_el = driver.find_element(By.XPATH, '//*[@id="large-table"]/tbody/tr[22]/td[8]')
        assert table_el.text == '22.8'

    def test_app33_windows(self):
        driver.get('https://the-internet.herokuapp.com/windows')
        assert len(driver.window_handles) == 1
        driver.find_element(By.XPATH, '//*[@id="content"]/div/a').click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        res = driver.find_element(By.TAG_NAME, 'h3')
        assert len(driver.window_handles) == 2
        assert res.text == 'New Window'
        driver.close()

    @pytest.mark.skip
    def test_app34_nested_frames(self):
        driver.get('https://the-internet.herokuapp.com/nested_frames')

    def test_app35_notification_message_rendered(self):
        driver.get('https://the-internet.herokuapp.com/notification_message_rendered')
        driver.find_element(By.XPATH, '//*[@id="content"]/div/p/a').click()
        notification = driver.find_element(By.ID, 'flash').text
        assert notification == 'Action successful' or 'Action unsuccessful, please try again'

    def test_app36_redirector(self):
        driver.get('https://the-internet.herokuapp.com/redirector')
        redirect = driver.find_element(By.XPATH, '//*[@id="redirect"]').get_attribute('href')
        driver.find_element(By.XPATH, '//*[@id="redirect"]').click()
        time.sleep(1)
        assert str(redirect) != driver.current_url

    @pytest.mark.skip
    def test_app37_download_secure(self):
        driver.get('https://the-internet.herokuapp.com/download_secure')

    def test_app37_shadowdom(self):
        driver.get('https://the-internet.herokuapp.com/shadowdom')
        shadow_host = driver.find_element(By.XPATH, '//*[@id="content"]/my-paragraph[1]')
        shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_host)
        shadow_content = shadow_root.find_element(By.NAME, 'my-text').text
        assert shadow_content == "My default text"

        shadow_host2 = driver.find_element(By.XPATH, '//*[@id="content"]/my-paragraph[2]')
        shadow_root2 = driver.execute_script('return arguments[0].shadowRoot', shadow_host2)
        shadow_content2 = shadow_root2.find_element(By.NAME, 'my-text').text
        assert shadow_content2 == "My default text"

    def test_app38_shifting_content_menu(self):
        driver.get('https://the-internet.herokuapp.com/shifting_content/menu')
        pos = driver.find_element(By.XPATH, '//*[@id="content"]/div/ul/li[5]/a').value_of_css_property('left')
        assert pos == '0px'

    def test_app39_shifting_content_image(self):
        driver.get('https://the-internet.herokuapp.com/shifting_content/image')
        pos = driver.find_element(By.XPATH, '//*[@id="content"]/div/img').value_of_css_property('left')
        assert pos == '0px'

    @pytest.mark.skip
    def test_app39_shifting_content_list(self):
        driver.get('https://the-internet.herokuapp.com/shifting_content/list')

    @pytest.mark.skip
    def test_app40_slow(self):
        driver.get('https://the-internet.herokuapp.com/slow')

    def test_app41_tables(self):
        driver.get('https://the-internet.herokuapp.com/tables')
        assert driver.find_element(By.XPATH, '//*[@id="table1"]/tbody/tr[1]/td[1]').text == 'Smith'
        assert driver.find_element(By.XPATH, '//*[@id="table1"]/tbody/tr[2]/td[1]').text == 'Bach'
        assert driver.find_element(By.XPATH, '//*[@id="table1"]/tbody/tr[3]/td[1]').text == 'Doe'
        assert driver.find_element(By.XPATH, '//*[@id="table1"]/tbody/tr[4]/td[1]').text == 'Conway'
        driver.find_element(By.XPATH, '//*[@id="table1"]/thead/tr/th[1]/span').click()
        assert driver.find_element(By.XPATH, '//*[@id="table1"]/tbody/tr[1]/td[1]').text == 'Bach'
        assert driver.find_element(By.XPATH, '//*[@id="table1"]/tbody/tr[2]/td[1]').text == 'Conway'
        assert driver.find_element(By.XPATH, '//*[@id="table1"]/tbody/tr[3]/td[1]').text == 'Doe'
        assert driver.find_element(By.XPATH, '//*[@id="table1"]/tbody/tr[4]/td[1]').text == 'Smith'

        driver.get('https://the-internet.herokuapp.com/tables')
        assert driver.find_element(By.XPATH, '//*[@id="table2"]/tbody/tr[1]/td[1]').text == 'Smith'
        assert driver.find_element(By.XPATH, '//*[@id="table2"]/tbody/tr[2]/td[1]').text == 'Bach'
        assert driver.find_element(By.XPATH, '//*[@id="table2"]/tbody/tr[3]/td[1]').text == 'Doe'
        assert driver.find_element(By.XPATH, '//*[@id="table2"]/tbody/tr[4]/td[1]').text == 'Conway'
        driver.find_element(By.XPATH, '//*[@id="table2"]/thead/tr/th[1]/span').click()
        assert driver.find_element(By.XPATH, '//*[@id="table2"]/tbody/tr[1]/td[1]').text == 'Bach'
        assert driver.find_element(By.XPATH, '//*[@id="table2"]/tbody/tr[2]/td[1]').text == 'Conway'
        assert driver.find_element(By.XPATH, '//*[@id="table2"]/tbody/tr[3]/td[1]').text == 'Doe'
        assert driver.find_element(By.XPATH, '//*[@id="table2"]/tbody/tr[4]/td[1]').text == 'Smith'

    def test_app42_status_codes(self):
        assert requests.get('https://the-internet.herokuapp.com/status_codes/200').status_code == 200
        assert requests.get('https://the-internet.herokuapp.com/status_codes/301').status_code == 301
        assert requests.get('https://the-internet.herokuapp.com/status_codes/404').status_code == 404
        assert requests.get('https://the-internet.herokuapp.com/status_codes/500').status_code == 500

    @pytest.mark.latest
    def test_app43_typos(self):
        driver.get('https://the-internet.herokuapp.com/typos')
        assert driver.find_element(By.XPATH,
                                   '//*[@id="content"]/div/p[2]').text == "Sometimes you'll see a typo, other times you won't."
        driver.quit()
