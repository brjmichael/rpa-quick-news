import bot
import pandas as pd
from enum import Enum
from time import sleep
from modules import latimes
from selenium.webdriver.common.by import By

from robocorp.tasks import task
from RPA.Robocorp.WorkItems import WorkItems

class Locators(Enum):
    """Class of the main element locators usd on the website"""
    SEARCH_BTN = "//*[@data-element='search-button']"
    SEARCH_INPUT = "//*[@data-element='search-form-input']"
    SUBMIT_SEARCH = "//*[@data-element='search-submit-button']"
    SORT_BY_SELECT = "select.select-input"
    SEARCH_FILTER_TOPIC = "ul.search-filter-menu"
    UL_NEWS = "ul.search-results-module-results-menu"

@task
def main():
    """Main flow
    
    Performs the necessary steps to automate the collection of news from the LaTimes site
    """
    # Get work item variable
    wi = WorkItems()
    wi.get_input_work_item()
    input_wi = wi.get_work_item_variables()
    search_phrase = input_wi.get("search_phrase", "Economic")
    topic_search = input_wi.get("topic_search", "Business")

    # Starts the browser and accesses the website
    browser = bot.browser.Chrome()
    browser.searchBrowser("https://www.latimes.com")
    pageTitle = browser.title

    bot.logger.info(f"Current Page Title: '{ pageTitle }'")
    
    # Click on the search button
    element = browser.find_element("xpath", Locators.SEARCH_BTN)
    assert element, f"Element '{ element }' not found"
    element.click()

    # Focuses on the search field and typing phrase
    element = browser.find_element("xpath", Locators.SEARCH_INPUT)
    assert element, f"Element '{ element }' not found"
    element.send_keys(search_phrase)    
    
    # Click on the submit search button
    element = browser.find_element("xpath", Locators.SUBMIT_SEARCH)
    assert element, f"Element '{ element }' not found"
    element.click()

    # Waits for the page to redirect to the search page
    bot.utils.wait_condition(
        condition = lambda: browser.title != pageTitle,
        timeout = 15,
        error = TimeoutError
    )

    # Search page
    searchPageUrl = browser.url
    
    # Filtering by topic
    element = browser.find_element("css selector", Locators.SEARCH_FILTER_TOPIC)
    assert element, f"Element '{ element }' not found"

    topics = element.find_elements(By.TAG_NAME, "li")
    filtered = False

    for item in topics:
        topic = item.find_element(By.CSS_SELECTOR, "label span").text

        if topic_search in topic:
            checkbox = item.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
            if not checkbox.is_selected():
                checkbox.click()
                filtered = True
            break

    if not filtered: bot.logger.info(f"No topic matches the term '{ topic_search }'")

    # Filters the 'Sort By' field to display the latest news
    element = browser.awaits_visibility_element("css selector", Locators.SORT_BY_SELECT, "Visible")
    assert element, f"Element '{ element }' not found"
    browser.select_option(element, "Newest")
    sleep(2)

    bot.utils.wait_condition(
        condition = lambda: browser.url != searchPageUrl,
        timeout = 10,
        error = TimeoutError
    )

    # Get data from the news list
    element = browser.awaits_visibility_element("css selector", Locators.UL_NEWS, "Visible")
    assert element, f"Element '{ element }' not found"
    sleep(2)

    try:
        news_data = []
        news = element.find_elements(By.TAG_NAME, "li")
        for item in news:
            # Get title, date, description and picture filename
            title = item.find_element(By.CSS_SELECTOR, "h3.promo-title").text
            date = item.find_element(By.CSS_SELECTOR, "p.promo-timestamp").get_attribute("data-timestamp")
            description = item.find_element(By.CSS_SELECTOR, "p.promo-description").text
            
            try:
                picture_url = item.find_element(By.CSS_SELECTOR, "img.image").get_attribute("src")
                picture_filename = bot.utils.filename_from_url(picture_url, ".jpg")
            except Exception as error:
                bot.logger.error(f"Unable to download news image ('{ title }') . It probably doesn't have an image")
                picture_filename = "No image"

            news_data.append ({
                "Title": title,
                "Date": bot.utils.timestamp_to_date(float(date)),
                "Description": description,
                "Picture filename": picture_filename,
                "Count search phrase": bot.utils.count_phrase_in_context(search_phrase, [title, description]),
                "Contains Amount": latimes.amount_checker([title, description])
            })

            browser.download_file(picture_url, alt_extension=".jpg")

        df = pd.DataFrame(news_data)
        df.to_excel("./output/news.xlsx", index=False)

    except Exception as error:
       bot.logger.error(f"Error while obtaining the news data: { error }")

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        bot.logger.error(f"Unexpected error in the flow: { error }")
