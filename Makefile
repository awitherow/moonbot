setup:
	pip2 install -r requirements.txt

test_coin_market_cap_call:
	ENV=test python2 ./src/cmc.py

tail:
	heroku logs --app crypto-moon-bot --tail