import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("API_KEY")


def check_offers_stock(asin):
    """
    Fetches stock information using an ASIN to identify sellers and
    their latest stock quantities of that product.

    Parameters:
        asin (str): The ASIN of the product.

    Returns:
        list: A list of dictionaries with the following keys:
            - 'sellerId' (str): The ID of the seller.
            - 'latest_stock' (int): The latest stock quantity of that seller.

    """

    url = f"https://api.keepa.com/product?key={API_KEY}&domain=1&asin={asin}&stock=1&offers=20"

    try:
        response = requests.get(url)
        response.raise_for_status()
        product = response.json().get("products", [])[0]

        with open(f"{asin}_product_data.json", "w") as json_file:
            json.dump(product, json_file, indent=4)

        if not product:
            print(f"No product data available for ASIN: {asin}")
            return []

        if product.get("offers"):
            offer_data = []
            for offer in product["offers"]:
                seller_id = offer.get("sellerId")
                stock_data = offer.get("stockCSV")

                if stock_data:
                    latest_stock = stock_data[-1]
                    offer_data.append(
                        {"sellerId": seller_id, "latest_stock": latest_stock}
                    )

                else:
                    print(f"No stock data available for seller {seller_id}")

            return offer_data

        else:
            print("No offers available for this product.")
            return []

    except requests.exceptions.RequestException as err:
        print(f"Error fetching product data: {err}")
        return []


check_offers_stock(asin=os.getenv("ASIN"))

# Uncomment for testing purposes

if __name__ == "__main__":
    asin = os.getenv("ASIN")
    product_stock = check_offers_stock(asin)

    if product_stock:
        print(f"Offer stock information for ASIN: {asin}")
        for offer in product_stock:
            seller_id = offer["sellerId"]
            latest_stock = offer["latest_stock"]
            print(f"Seller ID: {seller_id}, Latest Stock: {latest_stock}")
    else:
        print(f"No offers available for ASIN: {asin}")
