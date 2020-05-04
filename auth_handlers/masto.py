# Holly Lotor Montalvo 2020
# Cross - a cross-poster between Mastodon and Hubzilla accounts. (yeah, I know, original name)
# This file processes accounts for Mastodon API-compatible instances and appends credentials to the userdata file.
# This one's about a million times easier since an API wrapper already exists *and* it doesn't involve storing
# passwords in plaintext! The wrapper name is super slick, too: it's called Mastodon.py.

import json
import jsonlines
import os
import re
from mastodon import Mastodon
import mastodon


def main():
    # Here's some settings.
    mapp_name = "Cross"
    mapp_scopes = ['read', 'write']
    mapp_site = "https://github.com/Frinkel/cross"

    # Putting all of the variables I'll be writing into the json file ahead of time...
    account = {}
    account['account_name'] = ""
    account['account_type'] = 0  # Mastodon accounts are 0, Hubzilla accounts 1.
    account['instance'] = ""
    account['masto_client_id'] = ""
    account['masto_client_secret'] = ""
    account['access_token'] = ""

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
    account['instance'] = re.sub("^https?://", "", account['instance'])  # Removes http(s) from the beginning.
    account['instance'] = re.sub("/.*$", "", account['instance'])

    # Create the OAuth app.
    account['masto_client_id'], account['masto_client_secret'] = Mastodon.create_app(mapp_name, scopes=mapp_scopes,
                                                                         api_base_url='https://' + account['instance'],
                                                                         website=mapp_site)

    # Generate a login URL.
    try:
        masto_auth = Mastodon(client_id=account['masto_client_id'], client_secret=account['masto_client_secret'],
                                api_base_url='https://' + account['instance'])
        login_url = masto_auth.auth_request_url(client_id=account['masto_client_id'], scopes=mapp_scopes,
                                                force_login=True)
    except mastodon.MastodonNetworkError:
        print("Couldn't connect to the instance for some reason, bailing...")
        exit(1)
    except mastodon.MastodonError:
        print("Something happened! (Something happened!)")
        exit(2)

    # Prompt user to authenticate with the URL.
    print("Please log into the Mastodon instance with the following URL:")
    print(login_url, end="\n\n")
    print("After doing so, copy and paste the code it gives you below...")

    # Obtain the login code via user prompt.
    login_code = input("Auth Code: ")

    # Attempt to authenticate, obtain access code if successful.
    try:
        account['access_token'] = masto_auth.log_in(code=login_code, scopes=mapp_scopes)
    except mastodon.MastodonIllegalArgumentError:
        # Documentation states we go here if the credentials are incorrect.
        print("The code provided appears to be incorrect. Bailing...")
        exit(1)
    except mastodon.MastodonAPIError:
        # Documentation states we go here if not all the requested scopes were granted.
        print("Something went wrong with the API scopes. Bailing...")
        exit(1)
    except mastodon.MastodonError:
        print("Something happened! (Something happened!)")
        exit(2)

    # Now we just need to nab the username...
    try:
        masto_session = Mastodon(client_id=account['masto_client_id'], client_secret=account['masto_client_secret'],
                                 access_token=account['access_token'], api_base_url='https://' + account['instance'])
        masto_acct_info = masto_session.account_verify_credentials()
        username = masto_acct_info['username']
    except mastodon.MastodonError:
        print("Something happened! (Something happened!)")
        exit(2)

    # create the account name...
    account['account_name'] = "@" + username + "@" + account['instance']

    # and now, we write!
    json_account = json.dumps(account)
    acct_already_exists = False
    with jsonlines.open(userdata_file) as reader:
        for obj in reader:
            if obj['account_name'] == account['account_name']:
                acct_already_exists = True
    if acct_already_exists:
        # TODO: Figure out how to delete the specific line automatically.
        # I know how I'd do it in Linux, but this needs to be OS-agnostic.
        print("The account already exists in the user data file.")
        print("Please delete the line with your account and run this script again.")
    else:
        with jsonlines.open(userdata_file, mode='a+', flush=True) as writer:
            writer.write(account)
        print("Account saved to file!")


if __name__ == '__main__':
    main()