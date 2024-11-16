import requests
import time
SLACK_BOT_TOKEN = "xoxb-8020284472341-8037138158309-04OdXZEahqbNxDOdcHQQhvbO"
CHANNEL_ID = "C080P6M4DKL"  # Replace with the ID of the channel you want to monitor
TARGET_USER_ID = "U080GCRATP1"  # Replace with Joe Arrowsmith's user ID
TARGET_MESSAGE = "Data has just been released"  # Replace with the target message content
def get_channel_messages(channel_id, latest_ts=None):
    """Fetch messages from a Slack channel."""
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    params = {
        "channel": channel_id,
        "limit": 10,  # Fetch the last 10 messages
    }
    if latest_ts:
        params["oldest"] = latest_ts  # Only fetch messages after the last checked timestamp
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["ok"]:
            return data["messages"]
        else:
            print(f"Error: {data['error']}")
    else:
        print(f"HTTP Error: {response.status_code}")
    return []
def monitor_channel():
    """Continuously poll the channel for new messages."""
    latest_ts = None  # Tracks the last processed message timestamp
    while True:
        messages = get_channel_messages(CHANNEL_ID, latest_ts)
        for message in reversed(messages):  # Process messages in chronological order
            user_id = message.get("user")
            text = message.get("text")
            ts = message.get("ts")
            # Check if the message matches the target conditions
            if user_id == TARGET_USER_ID and TARGET_MESSAGE.lower() in str(text).lower():
                print("Target message detected!")
                execute_custom_code(text, ts)
            # Update the latest timestamp
            latest_ts = ts
        time.sleep(5)  # Poll every 5 seconds
def execute_custom_code(message, ts):
    """Custom logic triggered by a specific message."""
    print(f'Custom code executed for message: "{message}" - {ts} - please mention me to recruiters if you use my work thanks lmao')
    # Add your logic here: API calls, database updates, etc.
if __name__ == "__main__":
    monitor_channel() (edited)


##// ==UserScript==
##// @name         New Userscript
##// @namespace    http://tampermonkey.net/
##// @version      2024-11-16
##// @description  try to take over the world!
##// @author       You
##// @match        https://docs.google.com/forms/d/e/1FAIpQLSeUYMkI5ce18RL2aF5C8I7mPxF7haH23VEVz7PQrvz0Do0NrQ/viewform
##// @icon         https://www.google.com/s2/favicons?sz=64&domain=google.com
##// @grant        GM_xmlhttpRequest
##// ==/UserScript==
##(function () {
##    'use strict';
##    // Wait for the page to fully load
##    window.addEventListener('load', () => {
##        console.log('Page loaded, starting automation...');
##        // Select and click the checkbox
##        const checkboxXPath = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div[1]/label/div/div[1]';
##        const checkbox = document.evaluate(
##            checkboxXPath,
##            document,
##            null,
##            XPathResult.FIRST_ORDERED_NODE_TYPE,
##            null
##        ).singleNodeValue;
##        if (checkbox) {
##            checkbox.click();
##            console.log('Checkbox clicked.');
##        } else {
##            console.error('Checkbox not found.');
##        }
##        // Fetch data from an API
##        GM_xmlhttpRequest({
##            method: 'GET',
##            url: 'REPLACE FOR THE URL OF YOUR OWN API THAT HAS THE MOST RECENT ANSWER HERE',
##            onload: (response) => {
##                const responseText = response.responseText; // if your response is simply the text. youll need to add extra handling if your api response is JSON
##                // Enter the response into the textarea
##                const textareaXPath =
##                    '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/textarea';
##                const textarea = document.evaluate(
##                    textareaXPath,
##                    document,
##                    null,
##                    XPathResult.FIRST_ORDERED_NODE_TYPE,
##                    null
##                ).singleNodeValue;
##                if (textarea) {
##                    textarea.value = responseText;
##                    textarea.dispatchEvent(new Event('input', { bubbles: true }));
##                    console.log('Response entered.');
##                } else {
##                    console.error('Textarea not found.');
##                }
##                // Wait 30 seconds before submitting the form (for testing)
##                console.log('Waiting 30 seconds before submitting...');
##                setTimeout(() => {
##                    // Click the submit button
##                    const submitXPath = '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div';
##                    const submitButton = document.evaluate(
##                        submitXPath,
##                        document,
##                        null,
##                        XPathResult.FIRST_ORDERED_NODE_TYPE,
##                        null
##                    ).singleNodeValue;
##                    if (submitButton) {
##                        submitButton.click();
##                        console.log('Form submitted.');
##                    } else {
##                        console.error('Submit button not found.');
##                    }
##                }, 30000);
##            },
##            onerror: () => {
##                console.error('Failed to fetch data from the API.');
##            },
##        });
##    });
##})();
