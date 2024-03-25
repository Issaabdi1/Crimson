import time
from .locator import *
from .element import BasePageElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select


class PageInput(BasePageElement):
    locator = MainPageLocators.PAGE_INPUT


class CommentInput(BasePageElement):
    locator = MainPageLocators.COMMENT_TEXT


class FindTermInput(BasePageElement):
    locator = MainPageLocators.FIND_TEXT


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):
    page_input = PageInput()
    comment_input = CommentInput()
    find_term_input = FindTermInput()

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

    # Checker
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

    # Actions
    def select_text(self):
        element = self.driver.find_element(*MainPageLocators.FIRST_PAGE_SECOND_SPAN)
        time.sleep(2)
        (self.actions.move_to_element(element)
         .move_by_offset(-100, 0)
         .click_and_hold()
         .move_by_offset(200, 0)
         .release()
         .perform())

    def click_voice_tab(self):
        voice_tab = self.driver.find_element(*MainPageLocators.VOICE_TAB)
        (self.actions.move_to_element(voice_tab)
         .move_by_offset(0, -10)
         .click()
         .perform())

    def click_text_tab(self):
        text_tab = self.driver.find_element(*MainPageLocators.TEXT_TAB)
        (self.actions.move_to_element(text_tab)
         .move_by_offset(0, -10)
         .click()
         .perform())

    def click_mark_button(self):
        mark_button = self.driver.find_element(*MainPageLocators.MARK_BTN)
        mark_button.click()

    def click_delete_mark_button(self):
        delete_mark_button = self.driver.find_element(*MainPageLocators.DELETE_MARK)
        delete_mark_button.click()

    def click_add_comment_button(self):
        add_comment_button = self.driver.find_element(*MainPageLocators.ADD_COMMENT)
        add_comment_button.click()

    def click_save_comment_button(self):
        save_comment_button = self.driver.find_element(*MainPageLocators.SAVE_COMMENT)
        (self.actions.move_to_element(save_comment_button)
         .click().click().click()
         .perform())

    def click_next_page_button(self):
        next_page_button = self.driver.find_element(*MainPageLocators.NEXT_BTN)
        next_page_button.click()

    def click_prev_page_button(self):
        prev_page_button = self.driver.find_element(*MainPageLocators.PREV_BTN)
        prev_page_button.click()

    def click_find_button(self):
        find_button = self.driver.find_element(*MainPageLocators.FIND_BTN)
        find_button.click()

    def click_thumbnail_button(self):
        thumbnail_button = self.driver.find_element(*MainPageLocators.THUMBNAIL_BTN)
        thumbnail_button.click()

    def click_comment_button(self):
        comment_button = self.driver.find_element(*MainPageLocators.COMMENT_BTN)
        comment_button.click()

    def click_outline_button(self):
        outline_button = self.driver.find_element(*MainPageLocators.OUTLINE_BTN)
        outline_button.click()

    def click_bookmark_button(self):
        bookmark_button = self.driver.find_element(*MainPageLocators.BOOKMARK_BTN)
        bookmark_button.click()

    def select_scale_input(self, input):
        scale_input = self.driver.find_element(*MainPageLocators.SCALE_INPUT)
        dropdown = Select(scale_input)
        dropdown.select_by_visible_text(input)

    def scroll_y(self, offset):
        viewer = self.driver.find_element(*MainPageLocators.VIEWER)
        self.driver.execute_script(f"arguments[0].scrollTop += {offset};", viewer)

    def scroll_y_back(self):
        viewer = self.driver.find_element(*MainPageLocators.VIEWER)
        self.driver.execute_script(f"arguments[0].scrollTop = 0;", viewer)


class OutlinePage(BasePage):

    def __init__(self, driver):
        super(OutlinePage, self).__init__(driver)
        self.actions = ActionChains(driver)

    # Checker
    def is_title_matches(self):
        return "Test Suite Viewer" in self.driver.title

    def is_num_pages_matches(self):
        num_pages = self.driver.find_element(*OutlinePageLocator.NUM_PAGE)
        return num_pages.text == "of 16"

    # Actions
    def click_outline_button(self):
        outline_button = self.driver.find_element(*OutlinePageLocator.OUTLINE_BTN)
        outline_button.click()

    # Getter
    def get_scroll_top(self):
        viewer = self.driver.find_element(*OutlinePageLocator.VIEWER)
        return self.driver.execute_script(f"return arguments[0].scrollTop", viewer)
