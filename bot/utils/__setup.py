import os
import re
from urllib.parse import unquote, urlparse
from datetime import datetime
from typing import Callable, Literal
from time import sleep, perf_counter

ALTERNATIVE_EXTENSIONS = Literal['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
"""Alternative extension options for referencing parameters"""

def wait_condition(condition: Callable[[], bool], timeout: int, delay=0.1, error: Exception = None) -> bool:
    """Repeat the `condition` function for `timeout` seconds until it results in `True`
    - Returns a `bool` indicating whether the `condition` has been met
    - Exceptions are ignored """

    timer = countdown()

    while timer() < timeout:
        try:
            if condition(): return True
        except: pass
        sleep(delay)

    if error != None: raise error("The condition did not have the expected return")
    return False

def filename_from_url(url: str, alt_extension: ALTERNATIVE_EXTENSIONS = None) -> str:
    """Returns only the file name of the URL if it has a valid extension
    - `alt_extension` defines an alternative extension for the file that does not have an extension defined"""
    filename = unquote(url).split('/')[-1]

    # Extract the extension
    extension = os.path.splitext(filename)[1]
    if extension == '' and alt_extension: return f"{ filename }{ alt_extension }"

    return filename

def timestamp_to_date(timestamp: float) -> str:
    """Converts a timestamp value to the format `F j, Y`"""
    # Validate whether the timestamp is in milliseconds or seconds
    if len(str(timestamp)) > 10:
        # Divide the timestamp by 1000 to convert from milliseconds to seconds
        timestamp_seconds = timestamp / 1000

    date = datetime.fromtimestamp(timestamp_seconds)
    return date.strftime(f"%B %d, %Y")

def count_phrase_in_context(phrase: str, contexts: list[str]) -> int:
    """Counts how many times `phrase` appears in a list of `contexts`"""
    count = 0
    for context in contexts:
        # Using re.escape to escape any special characters in the phrase
        # Using word boundaries (\b) to ensure exact phrase matches
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        matches = pattern.findall(context)
        count += len(matches)

    return count

def countdown () -> Callable[[], float]:
    """Starts a timer that reuturns the passed to each call in the function
    - Rounded to 3 decimal places"""
    startTime = perf_counter()
    return lambda: round(perf_counter() - startTime, 3) 

__all__ = [
    "wait_condition",
    "filename_from_url",
    "timestamp_to_date",
    "count_phrase_in_context",
    "ALTERNATIVE_EXTENSIONS"
]