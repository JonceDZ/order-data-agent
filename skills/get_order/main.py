from weni import Skill
from weni.context import Context
from weni.responses import TextResponse
import requests

class GetOrder(Skill):
    def execute(self, context: Context) -> TextResponse:
        order_id = context.parameters.get("order_id", "")

        account = context.credentials.get("VTEX_ACCOUNT")
        app_key = context.credentials.get("VTEX_APP_KEY")
        app_token = context.credentials.get("VTEX_APP_TOKEN")

        order_info = self.get_order_by_id(order_id, account, app_key, app_token)
        return TextResponse(data=order_info)

    def get_order_by_id(self, order_id, account, app_key, app_token):
        url = f"https://{account}.vtexcommercestable.com.br/api/oms/pvt/orders/{order_id}"

        headers = {
            "X-VTEX-API-AppKey": app_key,
            "X-VTEX-API-AppToken": app_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            preferences = data.get("storePreferencesData", {})
            currency_symbol = preferences.get("currencySymbol", "")
            currency_code = preferences.get("currencyCode", "")
            
            raw_total_value = data.get("value", 0)
            total_value = raw_total_value / 100.0
            formatted_total_value = f"{currency_symbol}{total_value:,.2f} {currency_code}"

            shipping_value = 0
            for t in data.get("totals", []):
                if t.get("id") == "Shipping":
                    shipping_value = t.get("value", 0)
                    break

            shipping_cost = shipping_value / 100.0
            formatted_shipping_cost = f"{currency_symbol}{shipping_cost:,.2f} {currency_code}"

            items = data.get("items", [])
            items_details = []
            for item in items:
                name = item.get("name", "Unknown product")
                item_id = item.get("id", "Unknown ID")
                raw_price = item.get("sellingPrice", 0)
                price = raw_price / 100.0
                formatted_price = f"{currency_symbol}{price:,.2f} {currency_code}"
                items_details.append(f"{name} at {formatted_price}")

            items_string = "; ".join(items_details) if items_details else "No items found."

            message = (
                f"Aha! 🕵️ I've found it. Order #{data['orderId']} is currently *{data['status']}* "
                f"and was placed by {data['clientProfileData']['firstName']}. "
                f"The order total is {formatted_total_value}. "
                f"Shipping cost: {formatted_shipping_cost}. "
                f"Products: {items_string}. Mystery solved ✅"
                f"The ID of the item is {item_id}"
            )
            return {"message": message}

        elif response.status_code == 404:
            return {
                "message": "Hmm... even Sherlock José couldn't find that order 🧐. Mind checking the ID one more time?"
            }
        else:
            return {
                "message": "Elementary, my dear user — something went wrong while reaching VTEX 🔎. Try again shortly, I'll be ready."
            }
