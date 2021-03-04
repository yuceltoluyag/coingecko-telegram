import time, os, requests
from os import environ
from pycoingecko import CoinGeckoAPI

# global variables
bot_token = environ['YOUR_BOT_TOKEN']
chat_id = environ['YOUR_CHAT_ID']
time_interval = 30  # in seconds


def get_crypto_price(sfppricelist, juldpricelist, leadpricelist, pundixpricelist):

    geckoAPI = CoinGeckoAPI()
    response = geckoAPI.get_price(
        ids=['safepal', 'julswap', 'lead-token', 'pundi-x'],
        vs_currencies="usd",
    )
    sfppricelist.append(response["safepal"]["usd"])
    leadpricelist.append(response["julswap"]["usd"])
    juldpricelist.append(response["lead-token"]["usd"])
    pundixpricelist.append(response["pundi-x"]["usd"])

    return sfppricelist, leadpricelist, juldpricelist


# fn to send_message through telegram
def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"

    # send the msg
    requests.get(url)


def format_msg(pricelisting):
    difflisting = []
    for i in range(len(pricelisting)):
        diff = round(pricelisting[i][1] - pricelisting[i][0], 2)
        difflisting.append(diff)

    msg = (
        f'Son Fiyatlar Dolar Cinsinden:'
        f'\nSFP: {pricelisting[0][0]}$ -> {pricelisting[0][1]}$ = {difflisting[0]}$!'
        f'\nJULD: {pricelisting[1][0]}$ -> {pricelisting[1][1]}$ = {difflisting[1]}$!'
        f'\nLEAD: {pricelisting[2][0]}$ -> {pricelisting[2][1]}$ = {difflisting[2]}$!'
        f'\nNPXS: {pricelisting[3][0]}$ -> {pricelisting[3][1]}$ = {difflisting[3]}$!'
    )

    return msg


def main():
    sfppricelist = []
    juldpricelist = []
    leadpricelist = []
    pundixpricelist = []

    # infinite loop
    while True:
        pricelistings = get_crypto_price(
            sfppricelist, juldpricelist, leadpricelist, pundixpricelist
        )

        # send last 6 btc price
        if len(pricelistings[0]) >= 2:
            msg = format_msg(pricelistings)
            send_message(chat_id=chat_id, msg=msg)
            # empty the price_list
            for i in range(len(pricelistings)):
                del pricelistings[i][0]

        # fetch the price for every dash minutes
        time.sleep(time_interval)


if __name__ == '__main__':
    main()
