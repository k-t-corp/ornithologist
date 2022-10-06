# ornithologist
CLI to crawl relevant Twitter accounts from your Twitter notifications

## Setup

### Install dependencies
```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

### Get Twitter credentials
This CLI uses unofficial Twitter API (e.g. the one used on their desktop webapp),
so you need to gather the credentials from a web browser that it logged into your Twitter account

1. `cp header.example.json header.json`
2. Make sure you are logged into your Twitter account on a web browser
3. Go to https://twitter.com/notifications
4. Open developer tab and inspect on the "Network" tab
   1. From the `https://twitter.com/i/api/2/notifications/all.json?...` AJAX call...
   2. Copy the `authorization` value in Request header into `headers.json`
   3. Store the `cookie` value in Request header into `cookie.txt`
   4. Store the `x-csrf-token` value in Request header into `headers.json`

## Run
```bash
./venv/bin/python main.py
```
