import re
import time
import requests
import pyshorteners
from pyshorteners.shorteners import chilpit





response = requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates').json()
if response['ok']:
    update_id = response['result'][-1]['update_id']
else:
    update_id = None

while True:
    if update_id:
        response = requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates?offset={update_id + 1}').json()
    else:
        response = requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates').json()

    if response['ok'] and response['result']:
        for result in response['result']:
            message = result.get('message', {})
            text_message = message.get('text', '')
            photo_caption = message.get('caption','')
            text_message += ' ' + photo_caption
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text_message)

            if urls:
                r = requests.head(urls[0], allow_redirects=True)
                long_link = r.url

                if "amazon" in long_link or "amzn" in long_link:
                    split = long_link.split('tag')
                    modified_link = split[0] + "&tag=jagan319-21"
                    s = pyshorteners.Shortener()
                    shortened_link = s.chilpit.short(modified_link)
                    modified_message = text_message.replace(urls[0], shortened_link)
                    requests.post(
                        f'https://api.telegram.org/bot{bot_token}/sendMessage',
                        json={'chat_id': chat_id, 'text': modified_message}
                    )
                elif "flipkart" in long_link or "flkrt" in long_link:
                    split = long_link.split('affid=')
                    modified_link = split[0] + "affid=jagan319"
                    s = pyshorteners.Shortener()
                    shortened_link = s.chilpit.short(modified_link)
                    modified_message = text_message.replace(urls[0], shortened_link)
                    
                    requests.post(
                        f'https://api.telegram.org/bot{bot_token}/sendMessage',
                        json={'chat_id': chat_id, 'text': modified_message}
                    )
                else:
                    pass
            update_id = result['update_id']
    time.sleep(10)
