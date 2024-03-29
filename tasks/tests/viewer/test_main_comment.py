import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from .locator import MainPageLocators, LogInPageLocator
from .page import MainPageComment
from selenium.webdriver.common.alert import Alert


class TestViewer2(unittest.TestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        self.driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(self.driver, 5)
        self.driver.get("http://localhost:8000/log_in/")
        wait.until(EC.element_to_be_clickable(LogInPageLocator.USERNAME)).send_keys("@admin")
        wait.until(EC.element_to_be_clickable(LogInPageLocator.PASSWORD)).send_keys("Password123")
        wait.until(EC.element_to_be_clickable(LogInPageLocator.LOGIN_SUBMIT)).click()
        self.driver.get("http://localhost:8000/filelist/")
        wait.until(EC.element_to_be_clickable(MainPageLocators.VIEWER_FORM_1)).click()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def test_num_pages_must_correct(self):
        """
        Tests that total page number is correctly displayed
        """
        main_page = MainPageComment(self.driver)
        time.sleep(2)
        self.assertTrue(main_page.is_num_pages_matches())

    def test_insert_and_delete_text_comments_correctly(self):
        """
        Tests that text comments should be inserted correctly into marked text
        # Select Text, click mark, click marked section, click text tab, click add note, write first,
         save first, click add note, write second, save second, delete first, delete second
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
        self.close_card(comment_cards[0])
        time.sleep(1)
        comment_cards = comments.find_elements(By.CLASS_NAME, "card")
        self.assertEqual(len(comment_cards), 1)
        self.close_card(comment_cards[0])
        time.sleep(1)
        comment_cards = comments.find_elements(By.CLASS_NAME, "card")
        self.assertEqual(len(comment_cards), 0)
        main_page.click_delete_mark_button()  # Delete the mark

    def test_insert_and_delete_voice_comments_correctly(self):
        """
        Tests that voice comments should be inserted correctly into marked text
        # Select Text, click mark, click marked section, record first, record second,
        click save, delete first, delete second, delete mark
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
        delete_button = self.get_voice_comment_cards_delete_button()
        delete_button.click()
        time.sleep(1)
        alert = Alert(self.driver)
        alert.accept()
        time.sleep(1)
        voice_comment_cards = saved_recordings.find_elements(By.CLASS_NAME, "card")
        self.assertEqual(len(voice_comment_cards), 1)
        delete_button = self.get_voice_comment_cards_delete_button()
        delete_button.click()
        time.sleep(1)
        alert = Alert(self.driver)
        alert.accept()
        time.sleep(1)
        voice_comment_cards = saved_recordings.find_elements(By.CLASS_NAME, "card")
        self.assertEqual(len(voice_comment_cards), 0)
        main_page.click_delete_mark_button()  # Delete the mark

    def find_card_text(self, card):
        return card.find_element(By.CLASS_NAME, "card-body").find_element(By.CLASS_NAME, "card-text").find_element(
            By.TAG_NAME, "textarea").get_attribute("value")

    def close_card(self, card):
        return card.find_element(By.CLASS_NAME, "button-container").find_element(By.TAG_NAME, "button").click()

    def get_voice_comment_cards_delete_button(self):
        return self.driver.find_element(By.XPATH, '//*[@id="savedRecordings"]/div[1]/div[3]/button[3]')

    def tearDown(self):
        self.driver.close()
