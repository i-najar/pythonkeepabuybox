import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def check_buybox_stock(asin):
    """
    Checks the Buy Box stock for a given ASIN.

    Args:
        asin (str): The ASIN of the product to check.

    Returns:
        int: The Buy Box stock quantity, or None if the request fails.
    """

    url = f"https://api.keepa.com/product?key={API_KEY}&domain=1&asin={asin}&stock=1&stats=1"

    try:
        response = requests.get(url)
        response.raise_for_status()
        product = response.json().get("products", [])[0]

        buybox_stock = product["stats"].get("stockBuyBox")
        # amazon_stock = product["stats"].get("stockAmazon") <-- Optional, not needed.

        return buybox_stock

    except requests.exceptions.RequestException as err:
        print(f"Error fetching product data: {err}")
        return None


# Uncomment for testing purposes

# if __name__ == "__main__":
#     asin = os.getenv("ASIN")
#     buybox_stock = check_buybox_stock(asin)
#     print(f"Buy Box Stock for {asin}: {buybox_stock}")
