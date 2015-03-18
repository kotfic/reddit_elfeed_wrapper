from config import USER_AGENT, CLIENT_ID, CODE
from config import CLIENT_SECRET, AUTH_REDIRECT_URI
import praw
import os

r = praw.Reddit(user_agent=USER_AGENT)

r.set_oauth_app_info(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     redirect_uri=AUTH_REDIRECT_URI)


url = r.get_authorize_url("uniqueKey_{}".format(os.getpid()),
                          "identity",
                          True)

# Get Code Here from url

access_info = r.get_access_information(CODE)
r.set_access_credentials(**access_info)


