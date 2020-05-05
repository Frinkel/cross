# Holly Lotor Montalvo 2020
# Cross - a cross-poster between Mastodon and Hubzilla accounts.
# The intent of this file is to compose and publish a post across multiple accounts.

# Here's a ton of dependencies we're gonna need.
import mastodon
from mastodon import Mastodon
import os
import requests
import jsonlines
import pprint
import time

# mastodon for, well, Mastodon support.
# os to access the userdata file.
# requests for sending API calls for Hubzilla.
# And jsonlines for handling the jl file.
# I also add pprint for the sake of printing the different accounts,
# and time for the sake of pausing before posting.
# Let's get to work!


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
    else:
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
    dirname = os.path.dirname(__file__)
    userdata_file = os.path.join(dirname, 'userdata.jl')
    pp = pprint.PrettyPrinter()

    # Print the header, as per usual...
    print("Cross - a Mastodon/Hubzilla cross-poster")
    print("       Holly Lotor Montalvo  2020       ")
    print("----------------------------------------", end="\n\n")

    # Read the file. Gather the account names.
    account_names = []
    try:
        with jsonlines.open(userdata_file) as reader:
            for account in reader:
                account_names.append(account['account_name'])
    except FileNotFoundError:
        # If the file doesn't exist, error out and let the user know why.
        print("Error: User data file doesn't exist.")
        print("Please add an account via one of the scripts in the auth_handlers directory. Bailing...")
        exit(1)
    if account_names == []:
        # If there are no entries in the file, error out and let the user know why.
        print("Error: No accounts on file.")
        print("Please add an account via one of the scripts in the auth_handlers directory. Bailing...")
        exit(1)
    # Print all the accounts we've got.
    print("Accounts on file:")
    pp.pprint(account_names)
    print()
    # Accept input for a content warning.
    subject = input("Please type a content warning for your post. If you have none, just hit Enter.\n")
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
    # Send a system command to clear the console screen.
    clear_screen = lambda: os.system('cls')
    clear_screen()
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
    with jsonlines.open(userdata_file) as reader:
        for account in reader:
            if account['account_type'] == 0:
                if post_mastodon(account, subject, post) is False:
                    print("Account " + account['account_name'] + " ran into an issue during execution, skipping...")
            elif account['account_type'] == 1:
                if post_hubzilla(account, subject, post) is False:
                    print("Account " + account['account_name'] + " ran into an issue during execution, skipping...")
            else:
                print("Account " + account['account_name'] + " has an invalid type, skipping...")
    print()
    print("Done! Thank you for using Cross.")

if __name__ == '__main__':
    main()
