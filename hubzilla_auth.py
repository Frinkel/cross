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

import getpass
import re
import libraries.userdata as userdata
import libraries.hubzilla as hubzilla
from libraries import common


# We need a whole slew of things. There's no API wrapper for Hubzilla, so we kinda have to roll our own.
# requests will be used to actually send web requests to the instance for validation.
# re will be used to perform a tad bit of sanitation on some of the user input.
# getpass will be used to avoid having the password echoed to the screen when typed.
# base64 will be used to encode the userdata sent to the instance.



def main():
    # Information we're going to put into the json file.
    account = {}
    account['account_type'] = 1  # Mastodon accounts are 0, Hubzilla accounts 1.

    # Make a pretty intro screen.
    common.post_header()

    # Ask for the instance name.
    account['instance'] = common.get_instance_domain()

    # Apply a few checks to ensure the instance given is (likely) a valid Hubzilla instance.
    # Neither are a perfect science, unfortunately.
    if hubzilla.basic_check(account['instance']) is False:
        # If we get here, the host-meta page failed to return properly, a page that exists by default on Hubzilla.
        # We're going to assume, therefore, that this instance is not working properly, if it's even an instance.
        # Either that, or someone made an error that even regex can't fix.
        print("Instance returned error upon validation. Something's amiss with the instance. Bailing...")
        # I know it might not necessarily be the cleanest thing on Earth to bail in the middle of the code, but
        # it honestly makes sense to me in this situation to bail at this point, and it makes less sense to drag
        # out the execution all the way to the end with a bunch of else blocks.
        exit(1)
    if hubzilla.check_nodeinfo(account['instance']) is False:
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
    account['credentials'] = hubzilla.base64_creds(channel_name, account['credentials'])

    # Attempt to use the credentials. Bail if fails.
    if hubzilla.check_usercred(account['instance'], account['credentials']) is False:
        print("Authorization attempt failed. Bailing...")
        exit(1)

    # Make the name of the account the full channel name (including the instance name.)
    account['account_name'] = channel_name + "@" + account['instance']

    # and write data to the data file!
    userdata.append_account(account)


if __name__ == '__main__':
    main()