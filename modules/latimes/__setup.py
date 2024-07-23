import re

def amount_checker(texts: list[str]) -> bool:
    """Checks if any of the texts contain a dollar amount in specified formats."""
    patterns = [
        r'\$\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?',  # Matches $11.1, $111,111.11
        r'\d+(?:\.\d+)? dollars',               # Matches 11 dollars, 11.1 dollars
        r'\d+(?:\.\d+)? USD'                    # Matches 11 USD, 11.1 USD
    ]

    for text in texts:
        for pattern in patterns:
            if re.search(pattern, text):
                return True

    return False

__all__ = [
    "amount_checker"
]