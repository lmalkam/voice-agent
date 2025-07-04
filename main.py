# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import load_dotenv
import subprocess
import logging
import re

# Set environment variables for your credentials
# Read more at http://twil.io/secure

load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
phone_number = os.getenv("TWILIO_PHONE_NUMBER")
livekit_url = os.getenv("LIVEKIT_URL")
livekit_api_key = os.getenv("LIVEKIT_API_KEY")
livekit_api_secret = os.getenv("LIVEKIT_API_SECRET")

def create_inbound_trunk():
    trunk_data = {
        "trunk": {
            "name": "Inbound LiveKit Trunk",
            "numbers": [phone_number]
        }
    }

    # 🔧 Write inbound_trunk.json
    with open('inbound_trunk.json', 'w') as f:
        import json
        json.dump(trunk_data, f, indent=4)

    # ✅ Run the command after JSON is ready
    result = subprocess.run(
        ['lk', 'sip', 'inbound', 'create', 'inbound_trunk.json',
         '--url', livekit_url.replace("wss", "https"),
         '--api-key', livekit_api_key,
         '--api-secret', livekit_api_secret],
        capture_output=True,
        text=True,
        cwd=os.getcwd(),
    )

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    # ✅ Extract SID
    match = re.search(r'ST_\w+', result.stdout)
    if match:
        inbound_trunk_sid = match.group(0)
        return inbound_trunk_sid
    else:
        return None

    
def create_dispatch_rule(trunk_sid):
    dispatch_rule_data = {
        "name": "Inbound Dispatch Rule",
        "trunk_ids": [trunk_sid],
        "rule": {
            "dispatchRuleIndividual": {
                "roomPrefix": "call-"
            }
        }
    }

    result = subprocess.run(
        ['lk', 'sip', 'dispatch-rule', 'create', 'dispatch_rule.json', '--url', livekit_url.replace("wss", "https"), '--api-key', livekit_api_key, '--api-secret', livekit_api_secret],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return

    logging.info(f"Dispatch rule created: {result.stdout}")

def main():

    client = Client(account_sid,auth_token)
    
    trunks_list = client.trunking.v1.trunks.list()

    riverline_trunk = next(
        (trunk for trunk in trunks_list if trunk.friendly_name == "riverline"),
        None
    )

    if not riverline_trunk:
        print("There is no riverline trunk in the twilio")
        return

    result = subprocess.run(
        ['lk', 'sip', 'inbound', 'create', 'inbound_trunk.json', '--url', livekit_url.replace("wss", "https"), '--api-key', livekit_api_key, '--api-secret', livekit_api_secret],
        capture_output=True,
        text=True,
        cwd=os.getcwd(),
    )

    #inbound_sid = create_inbound_trunk()
    inbound_sid = "ST_PKP83xmX8aUf"
    print(inbound_sid)
    if inbound_sid:
        print("Sadfsadf")
        create_dispatch_rule(inbound_sid)


if __name__ == "__main__":
    main()