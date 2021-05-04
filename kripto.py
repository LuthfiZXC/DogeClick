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

api_id = 1126719
api_hash = "3389b2abb4a96a82ed0f9efa744faa25"
phone_number = "+6281336434313"
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
balance = 0

ua = {
    'user-agent' : 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'
}

if not os.path.exists("session"):
    os.mkdir("session")

driver = uc.Chrome("C:\Windows\System32\chromedriver.exe")
client = TelegramClient("session/"+ phone_number, api_id, api_hash)
client.start(phone_number)
c = requests.session()

def hitung(timer):
    for sisa in range(int(timer), -1, -1):
        sys.stdout.write(f'\rTunggu dalam {sisa} detik')
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
            print("-----Visit Sites-----")
            await client.send_message(channel_username, "🖥 Visit sites")
        elif "Alerts for new click task" in pesan:
            print("\n-----Message Bots-----")
            await client.send_message(channel_username, "🤖 Message bots")
        elif "Alerts for new bot task" in pesan:
            print("\n-----Join Chats-----")
            await client.send_message(channel_username, "📣 Join chats")

        elif "Visit website" in pesan:
            url = event.reply_markup.rows[0].buttons[0].url
            sys.stdout.write(f"\nVisiting URL : {url}")
            if "doge.click/vc" in url:
                sys.stdout.write(f"\rCloudflare detected. Please wait...")
                with driver:
                    r = driver.get(url)
                    driver.close()
                    driver.exit()
            r = c.get(url, headers=ua)

            soup = BeautifulSoup(r.text, "html.parser")

            if soup.find('div', class_='g-recaptcha') is None and soup.find('div', id='headbar') is None:
                #sys.stdout.write("Done")
                pass
            elif soup.find('div', id='headbar') is not None:
                for data in soup.find_all('div', class_='container-fluid'):
                    code = data.get('data-code')
                    timer = data.get('data-timer')
                    token = data.get('data-token')
                    hitung(timer)
                    up = c.post('https://doge.click/reward', data={'code': code, 'token': token}, headers=ua)
        #-----Reward
        elif "You earned" in pesan:

            koin = re.search(r"You earned (.*?) DOGE", pesan).group(1)
            balance = balance + float(koin)
            sys.stdout.write(f"\rYou earned {koin} DOGE | Collected : {balance} DOGE\n")

        #-----Message Bot
        elif "Forward a message" in pesan :
            url = event.reply_markup.rows[0].buttons[0].url
            r = c.get(url, headers=ua)
            print(url)
            target = re.search(r'content=\"https://t\.me/(.*?)\">', r.text).group(1)
            sys.stdout.write(f"\nForwarding  message from @{target}")
            await client.send_message(target, "/start")
            sleep(1)
            @client.on(events.NewMessage(chats=target, incoming=True))
            async def forward(event):
                await client.forward_messages(channel_username, event.id, target)
                sleep(1)

        elif "After joining, press the" in pesan:
            url = event.reply_markup.rows[0].buttons[0].url
            r = c.get(url, headers=ua)
            print(url)
            target = re.search(r'content=\"https://t\.me/(.*?)\">', r.text).group(1)
            sys.stdout.write("\nJoining "+target)
            await client(JoinChannelRequest(target))
            await client(GetBotCallbackAnswerRequest(
                         channel_username,
                         channel_id,
                         data= event.reply_markup.rows[0].buttons[1].data
                         ))

        elif "Please stay on the site" in pesan:
            waktu = int(re.search(r"least (.*?) sec", pesan).group(1))
            hitung(waktu)
        elif "Success! 👍" in pesan:
            sys.stdout.write("\rSuccess!")

    await client.run_until_disconnected()
asyncio.get_event_loop().run_until_complete(main())