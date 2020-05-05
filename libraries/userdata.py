import jsonlines
from libraries import common

# I'm going to be using a JSON Lines file (http://jsonlines.org/) for storing details. (I just like JSON okay)

# TODO: Remove the dependent functions from poster
import poster


def get_names():
    # Read the file. Gather the account names.
    account_names = []
    try:
        with jsonlines.open(common.userdata_file) as reader:
            for account in reader:
                account_names.append(account['account_name'])
    except FileNotFoundError:
        # If the file doesn't exist, error out and let the user know why.
        print("Error: User data file doesn't exist.")
        print("Please add an account via one of the scripts in the auth_handlers directory. Bailing...")
        exit(1)
    if not account_names:
        # If there are no entries in the file, error out and let the user know why.
        print("Error: No accounts on file.")
        print("Please add an account via one of the scripts in the auth_handlers directory. Bailing...")
        exit(1)
    return account_names


def post_all_accts(subject, post):
    with jsonlines.open(common.userdata_file) as reader:
        for account in reader:
            if account['account_type'] == 0:
                if poster.post_mastodon(account, subject, post) is False:
                    print("Account " + account['account_name'] + " ran into an issue during execution, skipping...")
            elif account['account_type'] == 1:
                if poster.post_hubzilla(account, subject, post) is False:
                    print("Account " + account['account_name'] + " ran into an issue during execution, skipping...")
            else:
                print("Account " + account['account_name'] + " has an invalid type, skipping...")


def post_sel_accts(selected_accounts, subject, post):
    # Iterate over every account in the user data file.
    with jsonlines.open(common.userdata_file) as reader:
        for account in reader:
            # Check if the account was selected. If so, continue to make the post.
            if account['account_name'] in selected_accounts:
                # Use the Mastodon post function if it's a Mastodon account.
                if account['account_type'] == 0:
                    if poster.post_mastodon(account, subject, post) is False:
                        print("Account " + account['account_name'] + " ran into an issue during execution, skipping...")
                # Use the Hubzilla post function if it's a Hubzilla account.
                elif account['account_type'] == 1:
                    if poster.post_hubzilla(account, subject, post) is False:
                        print("Account " + account['account_name'] + " ran into an issue during execution, skipping...")
                # If we get to the "else", the entry has either been messed with, or is with a newer
                # version of this program made in the future where I've added more apps to cross-post
                # between. Either way, skip the account in this case.
                else:
                    print("Account " + account['account_name'] + " has an invalid type, skipping...")


def append_account(account):
    account_list = []
    acct_already_exists = False
    try:
        with jsonlines.open(common.userdata_file) as reader:
            for obj in reader:
                if obj['account_name'] == account['account_name']:
                    acct_already_exists = True
    except FileNotFoundError:
        # If we get here, the account definitely isn't in the userfile yet.
        acct_already_exists = False
    if acct_already_exists:
        # TODO: Figure out how to delete the specific line automatically.
        print("The account already exists in the user data file.")
        print("Please delete the line with your account and run this script again.")
    else:
        with jsonlines.open(common.userdata_file, mode='a', flush=True) as writer:
            writer.write(account)
        print("Account saved to file!")
