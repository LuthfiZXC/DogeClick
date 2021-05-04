#Script masih beta, jangan dipake kalo gamau kenapa2


import os
import re
import sys
import asyncio
import requests
import undetected_chromedriver.v2 as uc

from time import sleep
from bs4 import BeautifulSoup
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest, ImportChatInviteRequest, GetHistoryRequest

#----- Kode Warna -----#
R = '\033[31m' #Red
G = '\033[32m' #Green
Y = '\033[33m' #Yellow
B = '\033[34m' #Blue
M = '\033[35m' #Magenta
C = '\033[36m' #Brown
W = '\033[37m' #White
BR= '\033[91m' #Bright Red
BG= '\033[92m'
BY= '\033[93m'
BB= '\033[94m'
BM= '\033[95m'
BC= '\033[96m'
BW= '\033[97m'

#----- Telegram Information -----#
api_id = 1126719
api_hash = "3389b2abb4a96a82ed0f9efa744faa25"
phone_number1 = str(input("Phone number"))
doge = "Dogecoin_click_bot"
ltc = "Litecoin_click_bot"
bch = "BCH_clickbot"

#print("[1] Doge\n[2] LTC\n[3] BCH")
#ask = int(input("Masukkan pilihan :"))
ask = 1
if ask == 1:
    channel_username = doge
elif ask == 2:
    channel_username = ltc
elif ask == 3:
    channel_username = bch
else :
    print("input salah")
    exit()

#print(f"Current Bot : {channel_username}")

mode = 0
balance = 0.0

ua = {
    'user-agent' : 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'
}

if not os.path.exists("session"):
    os.mkdir("session")

sys.stdout.write(f"{R}-- Starting Chrome --")
driver = uc.Chrome("C:\Windows\System32\chromedriver.exe")
sys.stdout.write(f"\r{G}-- Chrome Started --{W}")
client = TelegramClient("session/"+ phone_number, api_id, api_hash)
client.start(phone_number)
c = requests.session()

def hitung(timer):
    for sisa in range(int(timer), -1, -1):
        sys.stdout.write(f'\r{Y}Tunggu dalam {sisa} detik')
        sleep(1)

async def main():

    try:
        me = await client.get_me()
        print("~Welcome "+me.username +"~\n")
    except TypeError:
        pass
    await client.send_message(channel_username, "🏠 Menu")
    sleep(1)

    @client.on(events.NewMessage(chats=channel_username, incoming=True))
    async def cek(event):
        global balance
        pesan = event.raw_text
        channel_id = event.id

        if "By using this bot, you agree" in pesan:
            print(f"\n\n{M}-----Visit Sites-----")
            await client.send_message(channel_username, "🖥 Visit sites")
        elif "Alerts for new click task" in pesan:
            print(f"\n\n{M}-----Message Bots-----")
            await client.send_message(channel_username, "🤖 Message bots")
        elif "Alerts for new bot task" in pesan:
            print(f"\n\n{M}-----Join Chats-----")
            await client.send_message(channel_username, "📣 Join chats")

#----- Visiting Ads -----#
        elif "Visit website" in pesan:
            url = event.reply_markup.rows[0].buttons[0].url
            sys.stdout.write(f"\n{BG}Visiting URL : {url}")
            if "doge.click/vc" in url:
                sys.stdout.write(f"\r{R}CloudFlare detected.{Y} Please wait...{W}")
                with driver:
                    driver.get(url)
                    driver.close()
                    driver.exit()

            r = c.get(url, headers=ua)
            soup = BeautifulSoup(r.text, "html.parser")

            if soup.find('div', class_='g-recaptcha') is None and soup.find('div', id='headbar') is None:
                pass
            elif soup.find('div', id='headbar') is not None:
                for data in soup.find_all('div', class_='container-fluid'):
                    code = data.get('data-code')
                    timer = data.get('data-timer')
                    token = data.get('data-token')
                    hitung(timer)
                    c.post('https://doge.click/reward', data={'code': code, 'token': token}, headers=ua)

#----- Reward -----#
        elif "You earned" in pesan:

            koin = re.search(r"You earned (.*?) DOGE", pesan).group(1)
            balance = balance + float(koin)
            bal = "{:.4f}".format(balance)
            sys.stdout.write(f"\r{BG}You earned {koin} DOGE | Collected : {bal} DOGE{W}")

#----- Message Bot -----#
        elif "Forward a message" in pesan :
            url = event.reply_markup.rows[0].buttons[0].url
            if "doge.click/bc" in url:
                sys.stdout.write(f"\r{R}CloudFlare detected.{Y} Please wait...{W}")
                with driver:
                    driver.get(url)
                    url = driver.current_url
                    print(url)
            r = c.get(url, headers=ua)
            target = re.search(r'content=\"https://t\.me/(.*?)\">', r.text).group(1)
            sys.stdout.write(f"\n{BG}Forwarding  message from @{target}{W}")
            await client.send_message(target, "/start")
            hitung(5)

            @client.on(events.NewMessage(chats=target, incoming=True))
            async def forward(event):
                await client.forward_messages(channel_username, event.id, target)
                sleep(1)

        elif "After joining, press the" in pesan:
            url = event.reply_markup.rows[0].buttons[0].url
            if "doge.click/jc" in url:
                sys.stdout.write(f"\r{R}CloudFlare detected.{Y} Please wait...{W}")
                with driver:
                    driver.get(url)
                    url = driver.current_url
            r = c.get(url, headers=ua)
            target = re.search(r'content=\"https://t\.me/(.*?)\">', r.text).group(1)
            sys.stdout.write(f"\n{BG}Joining Chats : @{target}{W}")
            await client(JoinChannelRequest(target))
            await client(GetBotCallbackAnswerRequest(
                         channel_username,
                         channel_id,
                         data= event.reply_markup.rows[0].buttons[1].data
                         ))
#----- Countdown -----#
        elif "Please stay on the site" in pesan:
            waktu = int(re.search(r"least (.*?) sec", pesan).group(1))
            hitung(waktu)
        elif "Success! 👍" in pesan:
            sys.stdout.write("\rSuccess!")

    await client.run_until_disconnected()
asyncio.get_event_loop().run_until_complete(main())
