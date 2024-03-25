import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from .locator import MainPageLocators
from .page import MainPage, OutlinePage


class TestViewerOutline(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/test_viewer_2/")

    def test_title_must_correct(self):
        """
        Tests that page title is correct
        """
        outline_page = OutlinePage(self.driver)
        self.assertTrue(outline_page.is_title_matches())

    def test_num_pages_must_correct(self):
        """
        Tests that total page number is correctly displayed
        """
        outline_page = OutlinePage(self.driver)
        time.sleep(2)
        self.assertTrue(outline_page.is_num_pages_matches())

    def test_click_outline_section_should_navigate_to_correct_position(self):
        """
        Tests that outline functionality works correctly (can navigate to the corresponding position)
        """
        outline_page = OutlinePage(self.driver)
        outline_page.click_outline_button()
        time.sleep(1)
        first_section = outline_page.driver.find_element(By.XPATH, '//*[@id="outlineView"]/div/span')
        first_section.click()
        time.sleep(1)
        self.assertEqual(outline_page.get_scroll_top(), 148.5)
        first_subsection = outline_page.driver.find_element(By.XPATH, '//*[@id="outlineView"]/div/div[1]/span')
        first_subsection.click()
        self.assertEqual(outline_page.get_scroll_top(), 793.5)
        time.sleep(1)