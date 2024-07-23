import os
import bot
import requests
from abc import ABC
from enum import Enum
from typing import Literal, Self

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Edge as WebDriverWedge, EdgeOptions
from selenium.webdriver import Chrome as WebDriverChrome, ChromeOptions

from bot import logger
from bot.utils import ALTERNATIVE_EXTENSIONS

WEBELEMENT_STRETEGIES = Literal["id", "xpath", "name", "css selector", "class name", "link text", "tag name"]
"""Strategies for locating WebElements in `Selenium`"""

WEBELEMENT_VISIBILITY_STATUS = Literal["Visible", "Invisible"]
"""Visibility status of WebElement - used for explicit waits"""

class Browser(ABC):
    """Class of Browser that will must be inherited """

    driver: WebDriverWedge | WebDriverChrome

    def __del__ (self) -> None:
        """Terminate the driver when the browser variable goes out of scope"""
        self.driver.quit()
        logger.info("Browser closed")
    
    @property
    def title (self) -> str:
        """Title of the focused tab"""
        return self.driver.title
    
    @property
    def url (self) -> str:
        """Current Url of the focused tab"""
        return self.driver.current_url
    
    def searchBrowser (self, url: str) ->  Self:
        """Search the Url in the focused tab"""
        logger.info(f"Searching for the URL '{ url }'")
        self.driver.get(url)
        return self

    def find_element(self, strategy: WEBELEMENT_STRETEGIES, locator: str | Enum) -> WebElement | None:
        """Find element in the current tab based on a `locator` for the selected `strategy`"""
        locator = locator if isinstance(locator, str) else str(locator.value)
        logger.info(f"Searching for element ('{ strategy }', '{ locator }')")
        try: return self.driver.find_element(strategy, locator)
        except: return None

    def find_elements(self, strategy: WEBELEMENT_STRETEGIES, locator: str | Enum) -> list[WebElement] | None:
        """Find various elements in the current tab based on a `locator` for the selected `strategy`"""
        locator = locator if isinstance(locator, str) else str(locator.value)
        logger.info(f"Searching for element ('{ strategy }', '{ locator }')")
        elements = self.driver.find_elements(strategy, locator)
        return elements or None
        
    def select_option(self, select: WebElement, option: str) -> None:
        """Select an option from the `select` element
        - `select` select element
        - `option` text of the option you want to select"""
        element = Select(select)
        try: return element.select_by_visible_text(option)
        except: raise Exception(f"Error selecting the '{ option }' option. Check to see if this option exists.")

    def awaits_visibility_element(self, strategy: WEBELEMENT_STRETEGIES, locator: str | Enum, visibility: WEBELEMENT_VISIBILITY_STATUS, timeout: int = 10) -> WebElement | None:
        """Sets an explicit wait until an element is visible or invisible"""
        locator = locator if isinstance(locator, str) else str(locator.value)
        try:
            condition = EC.visibility_of_element_located if visibility == "Visible" else EC.invisibility_of_element_located
            return WebDriverWait(self, timeout).until(condition( ( strategy, locator) ))
        except Exception as error:
            bot.logger.error(f"An error occurred: { error }")

    def download_file(self, url: str, alt_extension: ALTERNATIVE_EXTENSIONS = None, download_dir: str = "./output") -> None:
        """Downloads a file from `url`
        - `alt_extension` defines an alternative extension for the file that does not have an extension defined"""
        try:
            # Ensure the download directory exists
            os.makedirs(download_dir, exist_ok=True)
            
            # Download the file
            download = requests.get(url)
            download.raise_for_status()

            # Create the full path for the file
            file_name = bot.utils.filename_from_url(url, alt_extension)
            file_path = os.path.join(download_dir, file_name)

            # Write the content to the file
            with open(file_path, "wb") as file:
                file.write(download.content)

            bot.logger.info(f"The download of the '{ file_name }' file was completed successfully")
        except Exception as error:
            raise Exception(f"Unable to download the url provided: { error }")

class Edge (Browser):
    """Edge Browser"""

    driver: WebDriverWedge
    """Edge Driver"""

    def __init__ (self, timeout=15, download=rf"./downloads") -> None:
        """Initialize the Edge Browser
        - `timeout` used in waiting for `implicit_wait`
        - `download` used to inform the file download folder"""
        options = EdgeOptions()
        options.add_argument("--start-maximed")
        options.add_argument("--ignore-certificate-errors")
        options.add_experimental_option("prefs", {
            "download.prompt_for_download": False,
            "download.default_directory": os.path.abspath(download)
            })

        self.driver = WebDriverWedge(options)
        self.driver.maximize_window()

        logger.info("Edge browser has been initialized")

class Chrome (Browser):
    """Chrome Browser"""

    driver: WebDriverChrome
    """Chrome Driver"""

    def __init__ (self, timeout=30.0, download=rf"./downloads") -> None:
        """Initialize the Chrome Browser
        - `timeout` used in waiting for `implicit_wait`
        - `download` used to inform the file download folder"""
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("prefs", {
            "download.prompt_for_download": False,
            "download.default_directory": os.path.abspath(download)
        })

        self.driver = WebDriverChrome(options)
        self.driver.implicitly_wait(timeout)
        self.driver.maximize_window()

        logger.info("Chrome browser has been initialized")

__all__ = [
    "Edge",
    "Chrome",
    "Browser",
    "WEBELEMENT_STRETEGIES"
]