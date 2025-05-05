import requests
import time
import random
from requests.exceptions import RequestException

class Middlewares:
    @staticmethod
    def get_random_headers():
        for attempt in range(3):
            try:
                headers_resp = requests.get(
                    url='https://headers.scrapeops.io/v1/browser-headers',
                    params={
                        'api_key': 'c6b36cca-74ea-4c45-9397-af10c76a7d27',
                        'num_results': '2'
                    },
                    timeout=5
                )
                agents_resp = requests.get(
                    url='https://headers.scrapeops.io/v1/user-agents',
                    params={
                        'api_key': 'c6b36cca-74ea-4c45-9397-af10c76a7d27',
                        'num_results': '2'
                    },
                    timeout=5
                )

                headers_list = headers_resp.json().get("result", [])
                agents_list = agents_resp.json().get("result", [])
                selected_headers = random.choice(headers_list) if headers_list else {}
                selected_agent = random.choice(agents_list) if agents_list else selected_headers.get("user-agent", "Mozilla/5.0")
                filtered_headers = {k: v for k, v in selected_headers.items() if k.lower() != "user-agent"}

                print("***** Add Headers & User Agent ******")

                return filtered_headers, selected_agent

            except RequestException as e:
                print(f"⚠️ Attempt {attempt+1}: Failed to fetch headers: {e}")
                time.sleep(2)

        print("❌ Failed to get headers. Using fallback User-Agent.")
        return {}, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"