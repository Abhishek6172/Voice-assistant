import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MARTE_API_URL = "https://marte.app/api/v1/chat/completions"
MARTE_API_KEY = "Enter_yourAPI_key_here"
        headers = {
            "Authorization": f"Bearer {MARTE_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
    "model": "marte-v1",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.3,
    "max_tokens": 150,
    "privacy_level": "high"
}

        response = requests.post(MARTE_API_URL, json=payload, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()

        #
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        return reply or "I'm not sure how to respond."

    except Exception as e:
        print("Error while connecting to Marte API:", e)
        return "An error occurred while connecting to Marte."
