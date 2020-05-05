# Holly Lotor Montalvo 2020
# Cross - a cross-poster between Mastodon and Hubzilla accounts.
# The intent of this file is to compose and publish a post across multiple accounts.

# Here's a ton of dependencies we're gonna need.
import mastodon
from mastodon import Mastodon
import requests
import pprint
import time
# mastodon for, well, Mastodon support.
# os to access the userdata file.
# requests for sending API calls for Hubzilla.
# And jsonlines for handling the jl file.
# I also add pprint for the sake of printing the different accounts,
# and time for the sake of pausing before posting.
# Let's get to work!

import libraries.userdata as userdata
from libraries import common


# Oh, and I'm starting to try and reduce code block size.


def get_post_contents():
    # Accept continuous input for post contents.
    print("Start typing your post. Press Ctrl-Z (or Ctrl-D if not using Windows) on a blank line to finish typing.\n")
    post = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        post.append(line)
    # Join all the paragraphs typed with a line break.
    post = '\n'.join(post)
    return post


def post_hubzilla(hubzilla_account, subject, post):
    parameters = {
        "title": subject,
        "body": post,
        "app": "Cross"
    }
    headers = {'authorization': "Basic " + hubzilla_account['credentials']}
    url = "https://" + hubzilla_account['instance'] + "/api/z/1.0/item/update"
    response = requests.request("POST", url, data="", headers=headers, params=parameters)
    if response.status_code < 300:
        return True
    return False


def post_mastodon(mastodon_account, subject, post):
    try:
        masto_session = Mastodon(client_id=mastodon_account['masto_client_id'],
                                 client_secret=mastodon_account['masto_client_secret'],
                                 access_token=mastodon_account['access_token'],
                                 api_base_url="https://" + mastodon_account['instance'])
        masto_session.status_post(post, spoiler_text=subject)
    except mastodon.MastodonError:
        print("Something happened! (Something happened!)")
        return False
    return True


def main():
    # Location of the userdata file.
    pp = pprint.PrettyPrinter()

    # Print the header...
    common.post_header()
    account_names = userdata.get_names()
    # Print all the accounts we've got.
    print("Accounts on file:")
    pp.pprint(account_names)
    print()
    # Accept input for a content warning.
    subject = input("Please type a content warning for your post. If you have none, just hit Enter.\n")
    post = get_post_contents()
    # Print out a little post preview, including character count.
    print("Post Preview:")
    print(subject)
    print("-------------------------------------------------------")
    print(post)
    print("-------------------------------------------------------")
    print("Post length: " + str(len(subject) + len(post)) + "chars")
    print("Posting in 10 seconds...")
    time.sleep(10)

    # It's showtime.
    userdata.post_all_accts(subject, post)
    print()
    print("Done! Thank you for using Cross.")

if __name__ == '__main__':
    main()
