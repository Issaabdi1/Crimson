import time
import unittest
from selenium import webdriver
from .locator import MainPageLocators
from .page import MainPage


class TestViewer(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/test_viewer_1/")

    def test_title_must_correct(self):
        main_page = MainPage(self.driver)
        self.assertTrue(main_page.is_title_matches())

    def test_num_pages_must_correct(self):
        main_page = MainPage(self.driver)
        time.sleep(2)
        self.assertTrue(main_page.is_num_pages_matches())

    def test_num_pages_input_must_navigate_to_corresponding_page(self):
        main_page = MainPage(self.driver)
        main_page.page_input = "4"
        time.sleep(1)
        self.assertTrue(main_page.is_thumbnail_selected(4))
        main_page.page_input = "3"
        time.sleep(1)
        self.assertTrue(main_page.is_thumbnail_selected(3))

    def test_must_correctly_mark_text(self):
        main_page = MainPage(self.driver)
        main_page.select_text()
        time.sleep(1)
        main_page.click_mark_button()
        marked_section = self.driver.find_element(*MainPageLocators.MARKED_SECTION)
        self.assertEqual(marked_section.text, 'of the printing and typesetting ')

    def tearDown(self):
        self.driver.close()