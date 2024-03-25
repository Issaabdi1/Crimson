from selenium.webdriver.common.by import By


class MainPageLocators(object):
    NUM_PAGE = (By.ID, "numberPages")
    PAGE_INPUT = (By.ID, "pageInput")

    THUMBNAIL_BTN = (By.ID, "viewThumbnails")
    OUTLINE_BTN = (By.ID, "viewOutline")
    COMMENT_BTN = (By.ID, "viewComments")
    BOOKMARK_BTN = (By.ID, "viewBookmarks")

    THUMBNAIL_1 = (By.XPATH, '//*[@id="thumbnailsContainer"]/div[1]')
    THUMBNAIL_2 = (By.XPATH, '//*[@id="thumbnailsContainer"]/div[2]')
    THUMBNAIL_3 = (By.XPATH, '//*[@id="thumbnailsContainer"]/div[3]')
    THUMBNAIL_4 = (By.XPATH, '//*[@id="thumbnailsContainer"]/div[4]')
    THUMBNAIL_5 = (By.XPATH, '//*[@id="thumbnailsContainer"]/div[5]')
    THUMBNAIL_6 = (By.XPATH, '//*[@id="thumbnailsContainer"]/div[6]')

    FIRST_PAGE_FIRST_SPAN = (By.XPATH, '')

    MARK_BTN = (By.ID, "markButton")
    MARKED_SECTION = (By.ID, "markedSection")