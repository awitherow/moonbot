setup:
	pip2 install -r requirements.txt

tail:
	heroku logs --app crypto-moon-bot --tail