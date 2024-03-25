import time
from .locator import *
from .element import BasePageElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


class PageInput(BasePageElement):
    locator = MainPageLocators.PAGE_INPUT


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):
    page_input = PageInput()

    def __init__(self, driver):
        super(MainPage, self).__init__(driver)
        self.actions = ActionChains(driver)
        self.thumbs = []
        for i in range(1, 7):
            thumb_locator = getattr(MainPageLocators, f"THUMBNAIL_{i}")
            thumb_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(thumb_locator)
            )
            self.thumbs.append(thumb_element)

    def select_text(self):
        element = self.driver.find_element(By.XPATH, '//*[@id="textlayer-1"]/span[2]')
        time.sleep(2)
        (self.actions.move_to_element(element)
         .move_by_offset(-100, 0)
         .click_and_hold()
         .move_by_offset(200, 0)
         .release()
         .perform())

    def click_mark_button(self):
        mark_button = self.driver.find_element(*MainPageLocators.MARK_BTN)
        mark_button.click()

    def is_title_matches(self):
        return "Test Suite Viewer" in self.driver.title

    def is_num_pages_matches(self):
        num_pages = self.driver.find_element(*MainPageLocators.NUM_PAGE)
        return num_pages.text == "of 6"

    def is_thumbnail_selected(self, num):
        if 1 <= num <= len(self.thumbs):
            return self.thumbs[num - 1].get_attribute('aria-selected') == 'true'
        else:
            return False
