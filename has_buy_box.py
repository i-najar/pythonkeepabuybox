import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def has_buy_box(asin):
    """
    Checks if a product has a buybox on Amazon.

    Args:
        asin (str): ASIN of the product.

    Returns:
        bool: Returns True if the product has a buybox; False if no buybox.
    """
    url = f"https://api.keepa.com/product?key={API_KEY}&domain=1&asin={asin}&stats=1"  # Checks stats for last # of days (ex. 1)

    try:
        response = requests.get(url)
        response.raise_for_status()
        product = response.json().get("products", [])[0]

        if product and "stats" in product:
            buy_box_id = product["stats"].get("buyBoxSellerId")
            return buy_box_id not in [-1, -2, None]

        else:
            print("Product data or stats not found.")
            return False

    except requests.exceptions.RequestException as err:
        print(f"Error fetching product data: {err}")
        return False


# Uncomment for testing purposes

# if __name__ == "__main__":
#     asin = os.getenv("ASIN")
#     has_box = has_buy_box(asin)
#     print(f"Has Buy Box: {has_box}")
