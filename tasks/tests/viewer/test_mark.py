import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from .locator import MainPageLocators
from .page import MainPageComment


class TestMarks(unittest.TestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        self.driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(self.driver, 5)
        self.driver.get("http://localhost:8000/log_in/")
        wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys("@admin")
        wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys("Password123")
        wait.until(EC.element_to_be_clickable((By.ID, "btn-submit"))).click()
        self.driver.get("http://localhost:8000/filelist/")
        wait.until(EC.element_to_be_clickable((By.ID, "viewerForm1"))).click()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def test_create_mark(self):
        """
        Tests that marks are created
        # Select Text, click mark, click marked section,
        """
        main_page = MainPageComment(self.driver)
        main_page.select_text_voice()
        time.sleep(0.5)
        main_page.click_mark_button()
        time.sleep(0.5)
        marked_sections = self.driver.find_elements(*MainPageLocators.MARKED_SECTION)
        self.assertEqual(len(marked_sections), 1)
        marked_sections[0].click()
        main_page.click_delete_mark_button()

    def test_delete_mark(self):
        """
        Tests that marks are deleted
        # Select Text, click mark, click marked section, X2 
        """
        NO_OF_MARKED_SECTIONS = 2
        main_page = MainPageComment(self.driver)
        main_page.select_text_voice()
        time.sleep(0.5)
        main_page.click_mark_button()
        time.sleep(0.5)

        main_page.select_text_text()
        time.sleep(0.5)
        main_page.click_mark_button()
        time.sleep(0.5)

        marked_sections = self.driver.find_elements(*MainPageLocators.MARKED_SECTION)
        deleted_marks_counter = 0
        for section in marked_sections:
            section.click()
            time.sleep(0.5)
            main_page.click_delete_mark_button()
            time.sleep(0.5)
            deleted_marks_counter +=1
            self.assertEqual(len(self.driver.find_elements(*MainPageLocators.MARKED_SECTION))
                             , NO_OF_MARKED_SECTIONS - deleted_marks_counter)

    def test_marks_stay_deleted_after_reload(self):
        NO_OF_MARKED_SECTIONS = 2
        main_page = MainPageComment(self.driver)
        main_page.select_text_voice()
        time.sleep(0.5)
        main_page.click_mark_button()
        time.sleep(0.5)
        marked_sections = self.driver.find_elements(*MainPageLocators.MARKED_SECTION)
        marked_sections[0].click()
        main_page.click_delete_mark_button()
        time.sleep(0.5)

        self.driver.navigate().refresh() 
        marked_sections = self.driver.find_elements(*MainPageLocators.MARKED_SECTION)
        self.assertEqual(len(marked_sections), 0)

    def test_colour_change_of_selected_mark(self):
        main_page = MainPageComment(self.driver)
        main_page.select_text_voice()
        time.sleep(0.5)
        main_page.click_mark_button()
        time.sleep(0.5)
        marked_section = self.driver.find_element(*MainPageLocators.MARKED_SECTION)
        marked_section_colour = marked_section.get_attribute("background-color") #
        self.assertEqual(marked_section_colour, "yellow")
        marked_section.click()

        marked_section = self.driver.find_element(*MainPageLocators.MARKED_SECTION) #may be redundant
        marked_section_colour = marked_section.get_attribute("background-color") #
        self.assertEqual(marked_section_colour, "orange")

        main_page.click_delete_mark_button()

    def test_colour_change_between_2_marks(self):
        main_page = MainPageComment(self.driver)
        main_page.select_text_voice()
        time.sleep(0.5)
        main_page.click_mark_button()
        time.sleep(0.5)

        main_page.select_text_text()
        time.sleep(0.5)
        main_page.click_mark_button()
        time.sleep(0.5)

        marked_sections = self.driver.find_elements(*MainPageLocators.MARKED_SECTION)

        for section in marked_sections:
            self.assertEquals(section.get_attribute("background-color"),"yellow")

        marked_sections[0].click()
        time.sleep(0.5)
        self.assertEqual(marked_sections[0].get_attribute("background-color"), "orange")
        self.assertEqual(marked_sections[1].get_attribute("background-color"), "yellow")

        marked_sections[1].click()
        time.sleep(0.5)
        self.assertEqual(marked_sections[0].get_attribute("background-color"), "yellow")
        self.assertEqual(marked_sections[1].get_attribute("background-color"), "orange")

        time.sleep(0.5)
        main_page.click_delete_mark_button()
        time.sleep(0.5)
        marked_sections[0].click()
        time.sleep(0.5)
        main_page.click_delete_mark_button()


    def find_card_text(self, card):
        return card.find_element(By.CLASS_NAME, "card-body").find_element(By.CLASS_NAME, "card-text").find_element(
            By.TAG_NAME, "textarea").get_attribute("value")

    def tearDown(self):
        self.driver.close()