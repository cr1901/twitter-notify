import tweepy
import sys
from colorama import init, Fore, Back, Style

from tnotify.source import *
from tnotify.auth import auth_init


auth = auth_init()
api = tweepy.API(auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=False)

init(wrap=False)
fore_colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
back_colors = [Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE]
i = 0

# Potential tweepy.error.TweepError for timeout... retry?
conn = Source(api)
for nots in conn:
    for n in nots:
        msg_str = "reply " if n.msg_type == Notification.Timeline else "DM "
        try:
            print(fore_colors[i] + "New " + msg_str + "from " + n.sender + ": " + n.text)
        except UnicodeEncodeError:
            print(fore_colors[i] +  "New " + msg_str + "from " + n.sender + ": " + "UnicodeEncodeError")
    sys.stdout.flush()
    i = (i + 1) % 7
