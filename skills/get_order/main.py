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

        # Define los headers con autenticación y tipo de contenido
        headers = {
            "X-VTEX-API-AppKey": app_key,
            "X-VTEX-API-AppToken": app_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return {
                "message": (
                    f"Aha! 🕵️ I've found it. Order #{data['orderId']} is currently *{data['status']}* "
                    f"and was placed by {data['clientProfileData']['firstName']}. Mystery solved ✅"
                )
            }
        elif response.status_code == 404:
            return {
                "message": "Hmm... even Sherlock José couldn't find that order 🧐. Mind checking the ID one more time?"
            }
        else:
            return {
                "message": "Elementary, my dear user — something went wrong while reaching VTEX 🔎. Try again shortly, I'll be ready."
            }
