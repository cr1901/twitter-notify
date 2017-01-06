import tweepy
import webbrowser
import json
import time
import sys
import os
from colorama import init, Fore, Back, Style

from tnotify.source import *


def init_credentials(filename="auth.json"):
    with open(filename, "r") as fp:
        creds = json.load(fp)
    return creds

def write_credentials(auth, creds, filename="auth.json"):
    with open(filename, "w") as fp:
        creds["authorization_token"] = auth.access_token
        creds["authorization_secret"] = auth.access_token_secret
        json.dump(auths, fp, indent=4, separators=(',', ': '))

def get_auth_credentials(auth):
    redirect_url = auth.get_authorization_url()
    webbrowser.open(redirect_url)
    verifier = input("Enter PIN (will write credentials to file): ")
    auth.get_access_token(verifier)

auth_path = None
for fn in [os.path.join(os.path.expanduser("~"), ".tnotify", "auth.json")]:
    try:
        creds = init_credentials(filename=fn)
    except FileNotFoundError:
        continue
    else:
        auth_path = fn
        break

if not auth_path:
    raise FileNotFoundError("Could not find auth.json.")

auth = tweepy.OAuthHandler(creds["consumer_token"], creds["consumer_secret"])

try:
    auth.set_access_token(creds["authorization_token"], creds["authorization_secret"])
except:
    get_auth_credentials(auth)
    write_auth_credentials(auth, creds, filename=auth_path)

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
