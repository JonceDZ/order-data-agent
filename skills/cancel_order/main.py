from weni import Skill
from weni.context import Context
from weni.responses import TextResponse
import requests

class CancelOrder(Skill):
    def execute(self, context: Context) -> TextResponse:
        
        order_id = context.parameters.get("order_id", "")
        reason = context.parameters.get("reason", "No reason provided.")

        account = context.credentials.get("VTEX_ACCOUNT")
        app_key = context.credentials.get("VTEX_APP_KEY")
        app_token = context.credentials.get("VTEX_APP_TOKEN")


        cancel_info = self.cancel_order(order_id, account, app_key, app_token, reason)
        return TextResponse(data=cancel_info)

    def cancel_order(self, order_id, account, app_key, app_token, reason):

        url = f"https://{account}.vtexcommercestable.com.br/api/oms/pvt/orders/{order_id}/cancel"

        payload = {"reason": reason}

        headers = {
            "X-VTEX-API-AppKey": app_key,
            "X-VTEX-API-AppToken": app_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            
            data = response.json()
            return {
                "message": (
                    f"🕵️‍♂️ Case closed! Order #{order_id} has been successfully cancelled.\n"
                    f"Cancellation reason: \"{reason}\".\n"
                    "Another mystery solved by Sherlock José ✅"
                )
            }
        elif response.status_code == 403:
            
            return {
                "message": "Access denied: Unable to cancel the order due to insufficient permissions."
            }
        elif response.status_code == 404:
            return {
                "message": (
                    "Hmm... 🧐 It seems my badge doesn’t open that door — I wasn’t authorized to cancel this order. "
                "Please double-check if I’ve got the right credentials 🪪"
                )
            }
        else:
            return {
                "message": "Elementary, my dear user — something went wrong while attempting to cancel the order. Try again shortly."
            }
