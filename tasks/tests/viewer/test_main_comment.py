import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from .locator import MainPageLocators
from .page import MainPageComment


class TestViewer2(unittest.TestCase):

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

    def test_num_pages_must_correct(self):
        """
        Tests that total page number is correctly displayed
        """
        main_page = MainPageComment(self.driver)
        time.sleep(2)
        self.assertTrue(main_page.is_num_pages_matches())

    def test_insert_text_comments_correctly(self):
        """
        Tests that text comments should be inserted correctly into marked text
        # Select Text, click mark, click marked section, click text tab, click add note, write first,
         save first, click add note, write second, save second
        """
        main_page = MainPageComment(self.driver)
        main_page.select_text_text()
        time.sleep(1)
        main_page.click_mark_button()
        time.sleep(1)
        marked_section = self.driver.find_element(*MainPageLocators.MARKED_SECTION)
        marked_section.click()
        main_page.click_text_tab()
        time.sleep(1)
        main_page.click_add_comment_button()
        main_page.comment_input = "Hello World!"
        main_page.click_save_comment_button()
        main_page.click_add_comment_button()
        main_page.comment_input = "Testing!"
        main_page.click_save_comment_button()
        time.sleep(2)
        comments = self.driver.find_element(*MainPageLocators.TEXT_COMMENTS_CONTAINER)
        comment_cards = comments.find_elements(By.CLASS_NAME, "card")
        self.assertEqual(len(comment_cards), 2)
        self.assertEqual(self.find_card_text(comment_cards[0]), "Hello World!\n")
        self.assertEqual(self.find_card_text(comment_cards[1]), "Testing!\n")
        main_page.click_delete_mark_button()  # Delete the mark

    def test_insert_voice_comments_correctly(self):
        """
        Tests that voice comments should be inserted correctly into marked text
        # Select Text, click mark, click marked section, record first, record second, click save
        """
        main_page = MainPageComment(self.driver)
        main_page.select_text_voice()
        time.sleep(1)
        main_page.click_mark_button()
        time.sleep(1)
        marked_section = self.driver.find_element(*MainPageLocators.MARKED_SECTION)
        marked_section.click()
        main_page.click_record_button()  # Recording twice
        time.sleep(3)
        main_page.click_record_button()
        time.sleep(1)
        main_page.click_record_button()
        time.sleep(3)
        main_page.click_record_button()
        time.sleep(1)
        main_page.click_record_save_button()
        time.sleep(2)
        main_page.click_voice_comment_label()
        saved_recordings = self.driver.find_element(*MainPageLocators.SAVED_RECORDINGS)
        voice_comment_cards = saved_recordings.find_elements(By.CLASS_NAME, "card")
        self.assertEqual(len(voice_comment_cards), 2)
        main_page.click_delete_mark_button()  # Delete the mark

    def find_card_text(self, card):
        return card.find_element(By.CLASS_NAME, "card-body").find_element(By.CLASS_NAME, "card-text").find_element(
            By.TAG_NAME, "textarea").get_attribute("value")

    def tearDown(self):
        self.driver.close()
