from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys


class BasePageElement(object):
    locator = ("", "")

    def __set__(self, instance, value):
        driver = instance.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.locator)
        )
        driver.find_element(*self.locator).clear()
        driver.find_element(*self.locator).send_keys(value)
        driver.find_element(*self.locator).send_keys(Keys.ENTER)

    def __get__(self, instance, owner):
        driver = instance.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.locator)
        )
        element = driver.find_element(*self.locator)
        return element.get_attribute("value")