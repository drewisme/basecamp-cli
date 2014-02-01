# CLI Basecamp Time Entry

Tired of udpating your hours through the Basecamp site? Well sir, this might help.

## Install

1. New virtual environment `mkvirtualenv basecamp`
2. Clone it `git clone git@github.com:drewisme/basecamp-cli.git` and enter the directory `cd basecamp-cli`
3. Install dependencies `pip install -r requirements.txt`
4. Copy default settings file `cp settings.default settings.py`
5. Log into Basecamp, click "My Info" and then under Authentication tokens click "Show your tokens". Copy the token under "Token for feed readers or the Basecamp API" and update `BASECAMP_API_KEY` in settings.py

### Create Virtual Environment

