import os
import webbrowser
import json
import tweepy

def init_credentials(filename="auth.json"):
    with open(filename, "r") as fp:
        creds = json.load(fp)
    return creds

def write_credentials(auth, creds, filename="auth.json"):
    with open(filename, "w") as fp:
        creds["authorization_token"] = auth.access_token
        creds["authorization_secret"] = auth.access_token_secret
        json.dump(auths, fp, indent=4, separators=(',', ': '))

def get_credentials(auth):
    redirect_url = auth.get_authorization_url()
    webbrowser.open(redirect_url)
    verifier = input("Enter PIN (will write credentials to file): ")
    auth.get_access_token(verifier)

def auth_init(invoke_browser=True):
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
        if invoke_browser:
            get_credentials(auth)
            write_credentials(auth, creds, filename=auth_path)
        else:
            pass # FIXME: Reraise original exception?

    return auth
