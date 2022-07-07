import os
import re

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import sleep
from pyrogram import Client, filters
from pyrogram.methods.messages import send_message
from bot.helpers.sql_helper import gDriveDB, idsDB
from bot.helpers.utils import CustomFilters, humanbytes
from bot.helpers.downloader import download_file, utube_dl
from bot.helpers.gdrive_utils import GoogleDrive
from bot import DOWNLOAD_DIRECTORY, LOGGER
from bot.config import Messages, BotCommands
from pyrogram.errors import FloodWait, RPCError
from subprocess import call, check_output
import time
from pytz import timezone 
from datetime import datetime
import requests
import validators
import youtube_dl
from pyrogram import Client, filters
from base64 import b64decode


def psarips_sirigan_bypass(url):
    client = requests.Session()
    res = client.get(url)
    url = res.url.split('=', maxsplit=1)[-1]

    while True:
        try: url = b64decode(url).decode('utf-8')
        except: break

    return url.split('url=')[-1]


def droplink_bypass(url):
    client = requests.Session()
    res = client.get(url)

    ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]

    h = {'referer': ref}
    res = client.get(url, headers=h)

    bs4 = BeautifulSoup(res.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest'
    }
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    time.sleep(3.1)
    res = client.post(final_url, data=data, headers=h).json()

    return res



def RecaptchaV3(ANCHOR_URL):
    url_base = 'https://www.google.com/recaptcha/'
    post_data = "v={}&reason=q&c={}&k={}&co={}"
    client = requests.Session()
    client.headers.update({
        'content-type': 'application/x-www-form-urlencoded'
    })
    matches = re.findall('([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
    url_base += matches[0]+'/'
    params = matches[1]
    res = client.get(url_base+'anchor', params=params)
    token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
    params = dict(pair.split('=') for pair in params.split('&'))
    post_data = post_data.format(params["v"], token, params["k"], params["co"])
    res = client.post(url_base+'reload', params=f'k={params["k"]}', data=post_data)
    answer = re.findall(r'"rresp","(.*?)"', res.text)[0]    
    return answer

ANCHOR_URL = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8uaW86NDQz&hl=en&v=1B_yv3CBEV10KtI2HJ6eEXhJ&size=invisible&cb=4xnsug1vufyr'

# -------------------------------------------
# OUO BYPASS

def ouo_bypass(url):
    client = requests.Session()
    tempurl = url.replace("ouo.press", "ouo.io")
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    
    res = client.get(tempurl)
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"

    for _ in range(2):

        if res.headers.get('Location'):
            break

        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.form.findAll("input", {"name": re.compile(r"token$")})
        data = { input.get('name'): input.get('value') for input in inputs }
        
        ans = RecaptchaV3(ANCHOR_URL)
        data['x-token'] = ans
        
        h = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        
        res = client.post(next_url, data=data, headers=h, allow_redirects=False)
        next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"

    return {
        'original_link': url,
        'bypassed_link': res.headers.get('Location')
    }


def gplinks_bypass(url):
    client = requests.Session()
    res = client.get(url)
    
    h = { "referer": res.url }
    res = client.get(url, headers=h)
    
    bs4 = BeautifulSoup(res.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest'
    }
    
    time.sleep(10) # !important
    
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'
    res = client.post(final_url, data=data, headers=h).json()

    return res    


@Client.on_message(filters.private & filters.incoming & filters.text & (filters.command(BotCommands.Bypass) | filters.regex('^(ht|f)tp*')) & CustomFilters.auth_users)
def _download(client, message):
    user_id = message.from_user.id
    if not message.media:
        sent_message = message.reply_text('🕵️**Checking link...**', quote=True)
        if message.command:
            link = message.command[1]
        else:
            link = message.text
        if 'droplink' in link:
            sent_message.edit('**Bypassing...**')
            task = droplink_bypass(link)['url']
            
            sent_message.edit(f'**Ad URL : ** ```{link}```\n**Original URL : ** ```{task}```\n')

        elif 'ouo' in link:
            sent_message.edit('**Bypassing...**')
            task = ouo_bypass(link)['bypassed_link']
            
            sent_message.edit(f'**Ad URL : ** ```{link}```\n**Original URL : ** ```{task}```\n')


        elif 'sirigan' in link:
            sent_message.edit('**Bypassing...**')
            task = psarips_sirigan_bypass(link)
            
            sent_message.edit(f'**Ad URL : ** ```{link}```\n**Original URL : ** ```{task}```\n')

        elif 'gplinks' in link:
            sent_message.edit('**Bypassing...\nHave Patience GPLinks takes little time...**')
            task = gplinks_bypass(link)['url']
            
            sent_message.edit(f'**Ad URL : ** ```{link}```\n**Original URL : ** ```{task}```\n')    
           
