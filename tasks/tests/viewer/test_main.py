import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from .locator import MainPageLocators
from .page import MainPage


class TestViewer(unittest.TestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        """
        If you are not storing the path to the chromedriver to the system's PATH,
        Uncomment code below, replace with the path to the driver 
        and import this 'from selenium.webdriver.common.service import Service'
        """
        # service = Service(f"{path to driver}")
        # self.driver = webdriver.Chrome(service=service,options=chrome_options)
        self.driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(self.driver, 5)
        self.driver.get("http://localhost:8000/log_in/")
        wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys("@admin")
        wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys("Password123")
        wait.until(EC.element_to_be_clickable((By.ID, "btn-submit"))).click()
        self.driver.get("http://localhost:8000/test_viewer_1/")

    def test_title_must_correct(self):
        """
        Tests that page title is correct
        """
        main_page = MainPage(self.driver)
        self.assertTrue(main_page.is_title_matches())

    def test_num_pages_must_correct(self):
        """
        Tests that total page number is correctly displayed
        """
        main_page = MainPage(self.driver)
        time.sleep(2)
        self.assertTrue(main_page.is_num_pages_matches())

    def test_num_pages_input_must_navigate_to_corresponding_page(self):
        """
        Tests that type in page input field should correct navigate to correct page
        # input 4 to navigate to fourth page, input 3 to navigate to third page
        """
        main_page = MainPage(self.driver)
        main_page.page_input = "4"
        time.sleep(1)
        self.assertTrue(main_page.is_thumbnail_selected(4))
        main_page.page_input = "3"
        time.sleep(1)
        self.assertTrue(main_page.is_thumbnail_selected(3))

    def test_page_navigation_button_should_work_correctly(self):
        """
        Tests that the next & previous page button is working correctly
        # click next, click next twice, click previous three times
        """
        main_page = MainPage(self.driver)
        main_page.click_next_page_button()
        time.sleep(1)
        self.assertTrue(main_page.is_thumbnail_selected(2))
        self.assertEqual(main_page.page_input, '2')
        main_page.click_next_page_button()
        main_page.click_next_page_button()
        time.sleep(1)
        self.assertTrue(main_page.is_thumbnail_selected(4))
        self.assertEqual(main_page.page_input, '4')
        main_page.click_prev_page_button()
        main_page.click_prev_page_button()
        main_page.click_prev_page_button()
        time.sleep(1)
        self.assertTrue(main_page.is_thumbnail_selected(1))
        self.assertEqual(main_page.page_input, '1')

    def test_scale_input_should_zoom_the_PDF_correctly(self):
        """
        Tests that zoom functionality is correctly applied to the PDF
        # Zoom to 125% , 200% then back to original
        """
        main_page = MainPage(self.driver)
        first_page = self.driver.find_element(*MainPageLocators.FIRST_PAGE)
        original_height = first_page.size["height"]
        main_page.select_scale_input("125%")
        time.sleep(1)
        self.assertEqual(original_height * 1.25, self.driver.find_element(*MainPageLocators.FIRST_PAGE).size["height"])
        main_page.select_scale_input("200%")
        time.sleep(1)
        self.assertEqual(original_height * 2, self.driver.find_element(*MainPageLocators.FIRST_PAGE).size["height"])
        main_page.select_scale_input("100%")
        time.sleep(1)
        self.assertEqual(original_height, self.driver.find_element(*MainPageLocators.FIRST_PAGE).size["height"])

    def test_must_correctly_mark_text_and_click(self):
        """
        Tests that select a text and click on the mark button should mark the text correctly,
        and the marked text should selectable
        # select the text, click on the mark button, click on the marked text
        """
        main_page = MainPage(self.driver)
        main_page.select_text()
        time.sleep(1)
        main_page.click_mark_button()
        marked_section = self.driver.find_element(*MainPageLocators.MARKED_SECTION)
        self.assertEqual(marked_section.text, 'of the printing and typesetting ')
        marked_section.click()
        time.sleep(1)
        self.assertEqual(marked_section.value_of_css_property("background-color"), 'rgba(255, 165, 0, 1)')
        main_page.click_text_tab()
        main_page.click_delete_mark_button()

    def test_must_correctly_delete_mark_on_text(self):
        """
        Tests that select a marked text and click on the delete mark button, should delete the mark correctly
        # select the text, click on the mark button, click on the marked text, click on the delete mark button
        """
        main_page = MainPage(self.driver)
        main_page.select_text()
        time.sleep(1)
        main_page.click_mark_button()
        marked_section = self.driver.find_element(*MainPageLocators.MARKED_SECTION)
        marked_section.click()
        main_page.click_delete_mark_button()
        try:
            self.driver.find_element(*MainPageLocators.MARKED_SECTION)
        except NoSuchElementException:
            return
        else:
            raise AssertionError("Mark is not correctly deleted")

    def test_recording_functionality_works_correctly(self):
        """
        Tests that recording functionality should generate the audio file correctly
        """
        main_page = MainPage(self.driver)
        main_page.select_text()
        time.sleep(1)
        main_page.click_mark_button()
        marked_section = self.driver.find_element(*MainPageLocators.MARKED_SECTION)
        marked_section.click()
        main_page.click_record_button()
        time.sleep(3)
        main_page.click_record_button()
        time.sleep(1)
        recordings = self.driver.find_element(*MainPageLocators.RECORDINGS)
        self.assertEqual(len(recordings.find_elements(By.TAG_NAME, "audio")), 1)
        main_page.click_record_button()
        time.sleep(3)
        main_page.click_record_button()
        time.sleep(1)
        self.assertEqual(len(recordings.find_elements(By.TAG_NAME, "audio")), 2)

    def test_find_in_page_should_work_correctly(self):
        """
        Test that the find_in_page function correct find the term in the page
        # click the find button, input text
        """
        main_page = MainPage(self.driver)
        main_page.click_find_button()
        main_page.find_term_input = "PDF"
        time.sleep(1)
        class_check_script = f"return arguments[0].classList.contains('highlight');"
        first_term_found = main_page.driver.find_element(By.XPATH, '//*[@id="textlayer-1"]/span[2]/span[1]')
        self.assertTrue(main_page.driver.execute_script(class_check_script, first_term_found))
        self.assertEqual(first_term_found.text, "PDF")
        second_term_found = main_page.driver.find_element(By.XPATH, '//*[@id="textlayer-2"]/span[2]/span[1]')
        self.assertTrue(main_page.driver.execute_script(class_check_script, second_term_found))
        self.assertEqual(first_term_found.text, "PDF")
        third_term_found = main_page.driver.find_element(By.XPATH, '//*[@id="textlayer-3"]/span[2]/span[1]')
        self.assertTrue(main_page.driver.execute_script(class_check_script, third_term_found))
        self.assertEqual(first_term_found.text, "PDF")

    def test_must_scrolling_effect(self):
        """
        Tests that scrolling through viewer should change the page input and thumbnail
        # scrolling to second page, third page, then back to top (first page)
        """
        main_page = MainPage(self.driver)
        first_page = self.driver.find_element(*MainPageLocators.FIRST_PAGE)
        main_page.scroll_y(first_page.size["height"])
        time.sleep(1)
        self.assertTrue(main_page.is_thumbnail_selected(2))
        self.assertEqual(main_page.page_input, '2')
        main_page.scroll_y(first_page.size["height"])
        time.sleep(1)
        self.assertTrue(main_page.is_thumbnail_selected(3))
        self.assertEqual(main_page.page_input, '3')
        main_page.scroll_y_back()
        time.sleep(1)
        self.assertTrue(main_page.is_thumbnail_selected(1))
        self.assertEqual(main_page.page_input, '1')

    def test_side_bar_button_should_display_the_view_accordingly(self):
        """
        Tests that
        """
        main_page = MainPage(self.driver)
        thumbnail_view = self.driver.find_element(*MainPageLocators.THUMBNAIL_VIEW)
        outline_view = self.driver.find_element(*MainPageLocators.OUTLINE_VIEW)
        comment_view = self.driver.find_element(*MainPageLocators.COMMENT_VIEW)
        self.assertEqual(thumbnail_view.value_of_css_property("display"), 'block')
        self.assertEqual(outline_view.value_of_css_property("display"), 'none')
        self.assertEqual(comment_view.value_of_css_property("display"), 'none')
        main_page.click_outline_button()
        time.sleep(1)
        self.assertEqual(thumbnail_view.value_of_css_property("display"), 'none')
        self.assertEqual(outline_view.value_of_css_property("display"), 'block')
        self.assertEqual(comment_view.value_of_css_property("display"), 'none')
        main_page.click_comment_button()
        time.sleep(1)
        self.assertEqual(thumbnail_view.value_of_css_property("display"), 'none')
        self.assertEqual(outline_view.value_of_css_property("display"), 'none')
        self.assertEqual(comment_view.value_of_css_property("display"), 'block')
        main_page.click_bookmark_button()
        time.sleep(1)
        self.assertEqual(thumbnail_view.value_of_css_property("display"), 'none')
        self.assertEqual(outline_view.value_of_css_property("display"), 'none')
        self.assertEqual(comment_view.value_of_css_property("display"), 'none')
        main_page.click_thumbnail_button()
        time.sleep(1)
        self.assertEqual(thumbnail_view.value_of_css_property("display"), 'block')
        self.assertEqual(outline_view.value_of_css_property("display"), 'none')
        self.assertEqual(comment_view.value_of_css_property("display"), 'none')

    def tearDown(self):
        self.driver.close()
