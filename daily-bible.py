from slack_sdk.webhook import WebhookClient
from urllib import request
import xml.etree.ElementTree as ET
import re


def reg_brs(text):
    return re.sub(r'\n+', '\n\n', text)


req = request.urlopen('https://feed43.com/7044075533483011.xml')
src = req.read().decode('utf-8')

root = ET.fromstring(src)
item = root.find('./channel/item')

title = item.find('./title').text
desc = reg_brs(item.find('./description').text.replace('<br>', '\n\n'))
items = [*map(lambda item: item.strip(), desc.split('<delim>'))]
subtitle, address, verses, comment = items


li_verses = re.sub(r'<div.+?>', '', verses).replace('</div>', '')
md_verses = re.sub(r' ?<\/li> ?', '\n', re.sub(r'<li>', '*', li_verses))
md_comment = reg_brs(re.sub(r' ?<\/div> ?', '',
                            re.sub(r' ?<div.+?> ?', '\n\n', comment)))


message = f'*{title}*\n\n'
message += f'*{subtitle}*\n\n'
message += f'*{address}*\n\n'
message += f'{md_verses}\n\n'
message += '*해설*\n\n'
message += f'{md_comment}\n\n'

url = "https://hooks.slack.com/services/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"
webhook = WebhookClient(url)

response = webhook.send(text=message)
assert response.status_code == 200
assert response.body == "ok"
