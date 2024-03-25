from selenium.webdriver.common.by import By


class MainPageLocators(object):
    # BUTTONS
    PREV_BTN = (By.ID, "previousPage")
    NEXT_BTN = (By.ID, "nextPage")
    FIND_BTN = (By.ID, "viewFindbar")
    THUMBNAIL_BTN = (By.ID, "viewThumbnails")
    OUTLINE_BTN = (By.ID, "viewOutline")
    COMMENT_BTN = (By.ID, "viewComments")
    BOOKMARK_BTN = (By.ID, "viewBookmarks")
    MARK_BTN = (By.ID, "markButton")
    DELETE_MARK = (By.ID, "deleteMarkButton")
    ADD_COMMENT = (By.ID, "addCommentBtn")
    SAVE_COMMENT = (By.XPATH, '//*[@id="inputText"]/button')
    RECORD_BTN = (By.ID, 'recordButton')
    SAVE_RECORD = (By.ID, 'save')
    # INPUTS
    PAGE_INPUT = (By.ID, "pageInput")
    SCALE_INPUT = (By.ID, "selectScale")
    COMMENT_TEXT = (By.ID, "textArea")
    FIND_TEXT = (By.ID, "searchTermInput")
    # THUMBS
    THUMBNAIL_1 = (By.XPATH, '//*[@id="thumbnailsContainer"]/div[1]')
    THUMBNAIL_2 = (By.XPATH, '//*[@id="thumbnailsContainer"]/div[2]')
    THUMBNAIL_3 = (By.XPATH, '//*[@id="thumbnailsContainer"]/div[3]')
    THUMBNAIL_4 = (By.XPATH, '//*[@id="thumbnailsContainer"]/div[4]')
    THUMBNAIL_5 = (By.XPATH, '//*[@id="thumbnailsContainer"]/div[5]')
    THUMBNAIL_6 = (By.XPATH, '//*[@id="thumbnailsContainer"]/div[6]')
    # Text Span
    FIRST_PAGE_SECOND_SPAN = (By.XPATH, '//*[@id="textlayer-1"]/span[2]')
    MARKED_SECTION = (By.ID, "markedSection")
    # Tabs
    VOICE_TAB = (By.ID, "voice-pill-tab")
    TEXT_TAB = (By.ID, "text-pill-tab")
    # Indicator
    NUM_PAGE = (By.ID, "numberPages")
    # PDF Page
    FIRST_PAGE = (By.ID, "page1")
    # Views
    VIEWER = (By.ID, "viewer")
    THUMBNAIL_VIEW = (By.ID, "thumbnailView")
    OUTLINE_VIEW = (By.ID, "outlineView")
    COMMENT_VIEW = (By.ID, "commentView")
    BOOKMARK_VIEW = (By.ID, "bookmarksView")
    # Recording
    RECORDINGS = (By.ID, "recordings")


class OutlinePageLocator(object):
    OUTLINE_BTN = (By.ID, "viewOutline")
    OUTLINE_VIEW = (By.ID, "outlineView")
    VIEWER = (By.ID, "viewer")
    NUM_PAGE = (By.ID, "numberPages")
