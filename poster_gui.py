# Holly Lotor Montalvo 2020
# Cross - a cross-poster between Mastodon and Hubzilla accounts.
# The intent of this file is to provide a GUI to the console-based posting app.

# I'm importing the functions I made in the poster app. Doesn't make sense to reinvent the wheel.
from poster import post_hubzilla, post_mastodon
import PySimpleGUIQt as sg
import os
import jsonlines
# We don't need pprint and time.
# We don't even need requests or Mastodon.py, since it's in the other file.
# We do, however, need PySimpleGUIQt. Y'know, for the GUI.


def main():
    # Define theme for the GUI
    sg.theme('Light Grey 1')
    # Define the location for the userdata file.
    dirname = os.path.dirname(__file__)
    userdata_file = os.path.join(dirname, 'userdata.jl')
    # Create a list of all of the accounts in the userdata file.
    account_names = []
    try:
        with jsonlines.open(userdata_file) as reader:
            for account in reader:
                account_names.append(account['account_name'])
    except FileNotFoundError:
        # If the file doesn't exist, error out and let the user know why.
        sg.popup_ok("The data file doesn't appear to exist!\n"
                    "You'll need to create it and add your account(s) to it\n"
                    "by running one of the scripts in the auth_handlers\n"
                    "folder!", )
        exit(1)
    if account_names == []:
        # If there are no entries in the file, error out and let the user know why.
        sg.popup_ok("No accounts seem to exist in the data file!\n"
                    "You'll need to add your account(s) to the data file\n"
                    "by running one of the scripts in the auth_handlers\n"
                    "folder!")
        exit(1)
    # Create a column for the account list and the post GUI.
    acct_col = [[sg.Text('Select accounts to post to:')],
                [sg.Listbox(values=account_names, size=(20, 10))]]
    post_col = [[sg.Input(default_text="Subject/Content Warning (leave blank for none)", size=(50, 1))],
                [sg.Multiline(default_text="What's on your mind?", size=(50, 15))],
                [sg.Text(justification='right', key='-CHARS-', margins=(10, 10, 10, 10)),
                 sg.Button("Post!", size=(10, 1))]]
    # Combine both columns in one layout, and define the layout in the main window.
    layout = [[sg.Column(acct_col), sg.Column(post_col)]]
    window = sg.Window('Cross - A Mastodon/Hubzilla cross-poster', layout)

    # Start an loop that watches for window events and post length.
    while True:
        # This will update the post length counter every 20 milliseconds if I'm understanding correctly.
        # And, of course, will also do the event listening and monitor the values of the different items.
        event, values = window.read(timeout=20)
        if event is None:
            # If we get here, the user closed the window. Break the loop without posting.
            break
        elif event == 'Post!':
            # If we get here, the user pressed the post button.
            # Let's do a few sanity checks - first, let's make sure an account was selected to post to.
            if values[0] == []:
                # If we're here, no accounts were selected.
                sg.popup_ok("You didn't select any accounts!\n"
                            "Try selecting an account before posting.\n", title="Error making post")
            # Next, let's make sure they actually wrote a post.
            elif values[2] in ("", "What's on your mind?"):
                # They didn't actually write a post. Error out and let them know why.
                sg.popup_ok("You didn't actually write a post, silly!\n"
                            "Try writing one first.", title="Error making post")
            # We /should/ be good to continue at this point.
            else:
                # Check if the subject is the default. If so, just make it blank.
                subject = values[1]
                if subject == "Subject/Content Warning (leave blank for none)":
                    subject = ""
                # Iterate over every account in the user data file.
                with jsonlines.open(userdata_file) as reader:
                    for account in reader:
                        # Check if the account was selected. If so, continue to make the post.
                        if account['account_name'] in values[0]:
                            # Use the Mastodon post function if it's a Mastodon account.
                            if account['account_type'] == 0:
                                if post_mastodon(account, subject, values[2]) is False:
                                    print("Account " + account['account_name'] +
                                          " ran into an issue during execution, skipping...")
                            # Use the Hubzilla post function if it's a Hubzilla account.
                            elif account['account_type'] == 1:
                                if post_hubzilla(account, subject, values[2]) is False:
                                    print("Account " + account['account_name'] +
                                          " ran into an issue during execution, skipping...")
                            # If we get to the "else", the entry has either been messed with, or is with a newer version
                            # of this program made in the future where I've added more apps to cross-post between.
                            # Either way, skip the account in this case.
                            else:
                                print("Account " + account['account_name'] + " has an invalid type, skipping...")
                # And once we get here, we're done! Print a thank-you message in the console, break, and exit.
                print()
                print("Done! Thank you for using Cross.")
                break
        else:
            # We're not breaking or posting, so update the post length counter with the combined length of the
            # subject/content warning and the post.
            window['-CHARS-'].update(str(len(values[1]) + len(values[2])))
    window.close()


if __name__ == '__main__':
    main()
