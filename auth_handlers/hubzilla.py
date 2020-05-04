# Holly Lotor Montalvo 2020
# Cross - a cross-poster between Mastodon and Hubzilla accounts. (yeah, I know, original name)
# The purpose of this file is to accept credentials for Hubzilla accounts, verify their validity, and save
# the credentials to the userdata file.

# *** BEGIN HOLLY RANT TIME ***
# So the Hubzilla documentation for the OAuth workflow is essentially non-existent. The documentation examples
# for its API essentially have you pass the channel name and the password to the endpoint, and provide no detail as to
# how to go through an OAuth workflow, or how they've even implemented it. I spent a good few hours sifting through
# server source code, trying to figure out how OAuth was implemented and how to get it working. But, no matter what I
# do, it... just won't, and I can't tell if it's a failing on my part, or if their OAuth implementation is just hot
# garbage. But, seeing as though I've never actually seen an application like this that works with the Hubzilla API...
# I'm inclined to believe the latter. Needless to say, I'm definitely not going to implement this into a webapp. I'd
# rather be caught dead than having a webapp that stores its passwords in plaintext (not gonna pull a Sony), and
# forcing me to enter my password to this app every time I want to post feels like it defeats the convenience I was
# hoping for it to have.

# Although, what I might consider is doing something like the good password managers of current do, where information is
# encrypted two-way and is done so such a large number of times that attempting to brute force would be computationally
# expensive beyond reason, but only takes, like, 2-3 seconds if you have the correct password. Maybe down the line...

# ***  END HOLLY RANT TIME  ***

import os
import base64
import getpass
import re
import requests
import json
import jsonlines
# We need a whole slew of things. There's no API wrapper for Hubzilla, so we kinda have to roll our own.
# requests will be used to actually send web requests to the instance for validation.
# re will be used to perform a tad bit of sanitation on some of the user input.
# getpass will be used to avoid having the password echoed to the screen when typed.
# base64 will be used to encode the userdata sent to the instance.


# Function to check if the instance has a host-meta page in the /.well-known/ directory.
# The base Hubzilla install has this up, and it's kinda necessary for federation to work.
# That being said, this IS a heuristic - there are plugins for Hubzilla that explicitly disable federation.
# Might be worth looking down the line to see if there's a configuration that makes a valid instance fail this check.
def basic_check(instance):
    host_meta_url = "https://" + instance + "/.well-known/host-meta"
    # Sends a web request to the host-meta page on the instance given.
    host_meta = requests.request("GET", host_meta_url)
    # Check to see if the request returned with a 200 OK status code and return T/F based on that.
    if host_meta.status_code == 200:
        return True
    else:
        return False


# Check if the instance has a node_info page. If so, we can 100% confirm or deny it's a Hubzilla instance.
def check_nodeinfo(instance):
    nodeinfo_url = "https://" + instance + "/nodeinfo/2.0"
    nodeinfo_req = requests.request("GET", nodeinfo_url)
    if nodeinfo_req.status_code == 404:
        # The nodeinfo check failed completely, but this is inconclusive.
        # The Diaspora Statistics plugin has to be enabled for this check to work on a Hubzilla instance.
        # So, we're just gonna return True.
        return True
    # Obtain a JSON-formatted version of the returned data.
    nodeinfo = nodeinfo_req.json()
    # Check the key under software.name. /nodeinfo/2.0 on my instances returns hubzilla, and /1.0 returns redmatrix.
    # I'm including them both for sanity's sake.
    if nodeinfo["software"]["name"] in ("hubzilla", "redmatrix"):
        return True
    else:
        # If we get here, this key doesn't exist or includes something other than those two names.
        # We're going to assume this is not a Hubzilla instance.
        return False


# Smash the username and password into a base64-encoded string suitable for webauth.
def base64_creds(channel_name, password):
    # Yep, this is the format. Hope your password doesn't have a colon in it! 8D
    creds = channel_name + ":" + password
    # I have to admit, I don't understand why I have to encode the base64 like this, it seems redundant.
    # It's what the samples I found on the net claim is how to do it, though, and it Works(tm), so...
    creds64 = str(base64.b64encode(creds.encode("utf-8")), "utf-8")
    return creds64


# Attempts to authenticate and pull info using the credentials given using the Hubzilla API.
def check_usercred(instance, b64creds):
    # And then we put this into the authorization header.
    usercheck_header = {'authorization': "Basic " + b64creds}

    # Any API call that requires authentication should do here. I'm just using the basic channel export API function.
    usercheck_url = "https://" + instance + "/api/z/1.0/channel/export/basic"
    # Specifying the absolute basics, I only care about the status code.
    usercheck_params = {"sections": "channel", "posts": "0"}
    # Actually put forth the request.
    usercheck = requests.request("POST", usercheck_url, data="", headers=usercheck_header, params=usercheck_params)

    # If the request came out OK, return True. If not, return False.
    if usercheck.status_code == 200:
        return True
    else:
        return False



def main():
    # Information we're going to put into the json file.
    account = {}
    account['account_name'] = ""
    account['account_type'] = 1  # Mastodon accounts are 0, Hubzilla accounts 1. May add support for more accounts down the line.
    account['instance'] = ""
    account['credentials'] = ""

    # Information we're going to be playing with and not writing directly to the file.
    channel_name = ""
    password = ""

    # Location of the userdata file.
    dirname = os.path.dirname(__file__)
    userdata_file = os.path.join(dirname, '../userdata.jl')

    # Make a pretty intro screen.
    print("Cross - a Mastodon/Hubzilla cross-poster")
    print("       Holly Lotor Montalvo  2020       ")
    print("----------------------------------------", end="\n\n")

    # Ask for the instance name.
    account['instance'] = input("Please enter your instance's domain (i.e. example.com): ")
    # Strip information that might exist out of the URL, if it does.
    account['instance'] = re.sub("^https?://", "", account['instance'])   # Removes http(s) from the beginning.
    account['instance'] = re.sub("/.*$", "", account['instance'])         # This *should* remove everything after the domain name.

    # Apply a few checks to ensure the instance given is (likely) a valid Hubzilla instance.
    # Neither are a perfect science, unfortunately.
    if basic_check(account['instance']) is False:
        # If we get here, the host-meta page failed to return properly, a page that exists by default on Hubzilla.
        # We're going to assume, therefore, that this instance is not working properly, if it's even an instance.
        # Either that, or someone made an error that even regex can't fix.
        print("Instance returned error upon validation. Something's amiss with the instance. Bailing...")
        # I know it might not necessarily be the cleanest thing on Earth to bail in the middle of the code, but
        # it honestly makes sense to me in this situation to bail at this point, and it makes less sense to drag
        # out the execution all the way to the end with a bunch of else blocks.
        exit(1)
    if check_nodeinfo(account['instance']) is False:
        # If we get here, the nodeinfo page returned, but it appears to have software that isn't Hubzilla.
        # We're going to assume that they typed in the URL of an instance running other software - i.e. Mastodon
        print("Nodeinfo claims this isn't a Hubzilla instance. Bailing...")
        exit(1)

    # Now, we can ask for the user information.
    channel_name = input("Please enter your channel name (this is what goes before @" + account['instance'] + "): ")
    channel_name = re.sub("^@", "", channel_name)   # Remove leading @, should they add it for some reason.
    # Prompt for the password using getpass, which makes it so the output is not printed to the screen.
    account['credentials'] = getpass.getpass(prompt='Enter your password: ')

    # Immediately overwrite the raw password in memory with the base64-encoded user credentials.
    # Which... still has the password in it, but at least the password won't be staring right at you in the face.
    # Ugh, I REALLY wish the documentation for Hubzilla weren't hot garbage...
    account['credentials'] = base64_creds(channel_name, account['credentials'])

    # Attempt to use the credentials. Bail if fails.
    if check_usercred(account['instance'], account['credentials']) is False:
        print("Authorization attempt failed. Bailing...")
        exit(1)

    # Make the name of the account the full channel name (including the instance name.)
    account['account_name'] = channel_name + "@" + account['instance']

    # I'm going to be using a JSON Lines file (http://jsonlines.org/) for storing details. (I just like JSON okay)
    json_account = json.dumps(account)
    with jsonlines.open(userdata_file, mode='a', flush=True) as writer:
        writer.write(account)
    print("Account saved to file!")

if __name__ == '__main__':
    main()