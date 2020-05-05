# Holly Lotor Montalvo 2020
# Cross - a cross-poster between Mastodon and Hubzilla accounts. (yeah, I know, original name)
# This file processes accounts for Mastodon API-compatible instances and appends credentials to the userdata file.
# This one's about a million times easier since an API wrapper already exists *and* it doesn't involve storing
# passwords in plaintext! The wrapper name is super slick, too: it's called Mastodon.py.

from mastodon import Mastodon

from libraries import common
import libraries.userdata as userdata
import libraries.masto as mcross


def main():
    # Here's some settings.
    mapp_name = "Cross"
    mapp_scopes = ['read', 'write']
    mapp_site = "https://github.com/Frinkel/cross"

    account = {}
    account['account_type'] = 0  # Mastodon accounts are 0, Hubzilla accounts 1.

    # Make a pretty intro screen.
    common.post_header()

    # Ask for the instance name.
    account['instance'] = common.get_instance_domain()

    # Create the OAuth app.
    account['masto_client_id'], \
    account['masto_client_secret'] = Mastodon.create_app(mapp_name, scopes=mapp_scopes,
                                                         api_base_url='https://' + account['instance'],
                                                         website=mapp_site)
    # Generate a login URL and a Mastodon session.
    masto_auth, login_url = mcross.get_session_and_login_url(account['instance'], account['masto_client_id'],
                                             account['masto_client_secret'], mapp_scopes)

    # Prompt user to authenticate with the URL.
    print("Please log into the Mastodon instance with the following URL:")
    print(login_url, end="\n\n")
    print("After doing so, copy and paste the code it gives you below...")

    # Obtain the login code via user prompt.
    login_code = input("Auth Code: ")

    # Attempt to authenticate, obtain access code if successful.
    account['access_token'] = mcross.attempt_authenticate(masto_auth, login_code, mapp_scopes)

    # Now we just need to nab the username...
    username = mcross.get_username(account['masto_client_id'], account['masto_client_secret'],
                                   account['access_token'], account['instance'])

    # create the account name...
    account['account_name'] = "@" + username + "@" + account['instance']

    # and now, we write!
    userdata.append_account(account)


if __name__ == '__main__':
    main()