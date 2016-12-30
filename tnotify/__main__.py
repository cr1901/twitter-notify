import tweepy
import webbrowser
import json
import time
import sys
from colorama import init, Fore, Back, Style


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


creds = init_credentials()
auth = tweepy.OAuthHandler(creds["consumer_token"], creds["consumer_secret"])

try:
    auth.set_access_token(creds["authorization_token"], creds["authorization_secret"])
except:
    get_auth_credentials(auth)
    write_auth_credentials(auth, creds)

api = tweepy.API(auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=False)
replies = dict()
dms = dict()
init(wrap=False)

fore_colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
back_colors = [Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE]
i = 0

# Potential tweepy.error.TweepError for timeout... retry?
while True:
    mentions = api.mentions_timeline(20)
    messages = api.direct_messages(20)
    new_replies = False
    new_dms = False
    for m in reversed(mentions):
        if not m.id in replies:
            try:
                print(fore_colors[i] + "New reply from " + m.user.screen_name + ": " + m.text)
            except UnicodeEncodeError:
                print(fore_colors[i] + "New reply from " + m.user.screen_name + ": " + "UnicodeEncodeError")
            replies[m.id] = m
            new_replies = True

    for d in reversed(messages):
        if not d.id in dms:
            try:
                print(fore_colors[i] + "New DM from " + d.sender.screen_name + ": " + d.text)
            except UnicodeEncodeError:
                print(fore_colors[i] + "New DM from " + d.sender.screen_name + ": " + "UnicodeEncodeError")
            dms[d.id] = d
            new_dms = True
    # for mentions in tweepy.Cursor(api.mentions_timeline).items(20):
    #     if not mentions.id in replies:
    #         print("New reply from ".encode("utf-8") + mentions.user.screen_name.encode("utf-8") + ": ".encode("utf-8") + mentions.text.encode("utf-8"))
    #         replies[mentions.id] = mentions
    sys.stdout.flush()
    time.sleep(90)
    if new_replies:
        i = (i + 1) % 7
