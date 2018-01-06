import bot
from time import sleep

res = bot.build_info_template()
ad = bot.build_ad_template()
bot.send_message(res, "info")
sleep(3)
bot.send_message(ad, "ad")
