# CLI Basecamp Time Entry

Tired of udpating your hours through the Basecamp site? Well sir, this might help.

## Install
1. New virtual environment `mkvirtualenv basecamp`
2. Clone it `git clone git@github.com:drewisme/basecamp-cli.git` and enter the directory `cd basecamp-cli`
3. Install dependencies `pip install -r requirements.txt`
4. Copy default settings file `cp settings.default settings.py`
5. Log into Basecamp, click "My Info" and then under Authentication tokens click "Show your tokens". Copy the token under "Token for feed readers or the Basecamp API" and update `BASECAMP_API_KEY` in settings.py

## Usage
To see a list of available commands and arguments
```bash
python main.py --help
```

Get a list of projects
```bash
python main.py projects
#...
#id: Name
#...
```

Maybe you have an idea of the project name and want to filter the list
```bash
python main.py projects | grep Side
```

Once you found your project id run the following to add a time entry
```bash
python main.py time -p 12345 -m "Gettin' work done" -t 3.0
```
or if you want a date other than today
```bash
python main.py time -p 12345 -m "Gettin' work done" -t 3.0 -d 2014-01-30
```

## !!Notice!!
There is no updating a time stamp right now. So if you muck it up, log into Basecamp to fix it.
