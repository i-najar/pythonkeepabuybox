import os
import requests
from dotenv import load_dotenv

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
                This is based on the most recent timestamp in the stock data.

    """

    url = f"https://api.keepa.com/product?key={API_KEY}&domain=1&asin={asin}&stock=1&offers=20"

    try:
        response = requests.get(url)
        response.raise_for_status()
        product = response.json().get("products", [])[0]

        if not product:
            print(f"No product data available for ASIN: {asin}")
            return []

        if product.get("offers"):
            seller_latest_info = {}

            for offer in product["offers"]:
                seller_id = offer.get("sellerId")
                stock_data = offer.get("stockCSV")

                if stock_data:
                    for i in range(0, len(stock_data), 2):
                        timestamp = stock_data[i]
                        stock_count = stock_data[i + 1]

                        if (
                            seller_id not in seller_latest_info
                            or timestamp > seller_latest_info[seller_id]["timestamp"]
                        ):
                            seller_latest_info[seller_id] = {
                                "latest_stock": stock_count,
                                "timestamp": timestamp,
                            }

                else:
                    print(f"No stock data available for seller {seller_id}")

            offer_data = [
                {"sellerId": seller_id, "latest_stock": info["latest_stock"]}
                for seller_id, info in seller_latest_info.items()
            ]

            return offer_data

        else:
            print("No offers available for this product.")
            return []

    except requests.exceptions.RequestException as err:
        print(f"Error fetching product data: {err}")
        return []


# Uncomment for testing purposes

# if __name__ == "__main__":
#     asin = os.getenv("ASIN")
#     product_stock = check_offers_stock(asin)

#     if product_stock:
#         print(f"Offer stock information for ASIN: {asin}")
#         for offer in product_stock:
#             seller_id = offer["sellerId"]
#             latest_stock = offer["latest_stock"]
#             print(f"Seller ID: {seller_id}, Latest Stock: {latest_stock}")
#     else:
#         print(f"No offers available for ASIN: {asin}")
