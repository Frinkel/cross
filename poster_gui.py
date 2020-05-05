# Holly Lotor Montalvo 2020
# Cross - a cross-poster between Mastodon and Hubzilla accounts.
# The intent of this file is to provide a GUI to the console-based posting app.

# I'm importing the functions I made in the poster app. Doesn't make sense to reinvent the wheel.
import PySimpleGUIQt as sg
import libraries.userdata as userdata
from libraries import common


# We don't need pprint and time.
# We don't even need requests or Mastodon.py, since it's in the other file.
# We do, however, need PySimpleGUIQt. Y'know, for the GUI.


def main():
    # Define theme for the GUI
    sg.theme('Light Grey 1')
    # Create a list of all of the accounts in the userdata file.
    account_names = userdata.get_names()
    # Define the icon in base64 format - this is the FontAwesome arrows-alt icon.
    # Create a column for the account list and the post GUI.
    acct_col = [[sg.Text('Select accounts to post to:')],
                [sg.Listbox(values=account_names, size=(20, 12))]]
    post_col = [[sg.Text('Subject/Content Warning (leave blank for none)')],
                [sg.Input(size=(50, 1))],
                [sg.Text("What's on your mind?")],
                [sg.Multiline(size=(50, 15))],
                [sg.Text(justification='right', key='-CHARS-', margins=(10, 10, 10, 10)),
                 sg.Button("Post!", size=(10, 1))]]
    # Combine both columns in one layout, and define the layout in the main window.
    layout = [[sg.Column(acct_col), sg.Column(post_col)]]
    window = sg.Window('Cross - A Mastodon/Hubzilla cross-poster', layout, icon=common.fa_arrows)

    # Start an loop that watches for window events and post length.
    while True:
        # This will update the post length counter every 20 milliseconds if I'm understanding correctly.
        # And, of course, will also do the event listening and monitor the values of the different items.
        event, values = window.read(timeout=20)
        if event in (None, 'Post!'):
            if event == 'Post!':
                # If we get here, the user pressed the post button.
                # Let's do a few sanity checks - first, let's make sure an account was selected to post to.
                if not values[0]:
                    # If we're here, no accounts were selected.
                    sg.popup_ok("You didn't select any accounts!\n"
                                "Try selecting an account before posting.\n",
                                title="Error making post", icon=common.fa_arrows)
                # Next, let's make sure they actually wrote a post.
                elif values[2] == "":
                    # They didn't actually write a post. Error out and let them know why.
                    sg.popup_ok("You didn't actually write a post, silly!\n"
                                "Try writing one first.", title="Error making post", icon=common.fa_arrows)
                # We /should/ be good to continue at this point.
                else:
                    userdata.post_sel_accts(values[0], values[1], values[2])
                    # And once we get here, we're done! Print a thank-you message in the console, break, and exit.
                    print()
                    print("Done! Thank you for using Cross.")
            # We've either finished posting or the user closed the window. Either way, let's break.
            break
        # If we get here, we're not breaking or posting, so update the post length counter with
        # the combined length of the subject/content warning and the post.
        window['-CHARS-'].update(str(len(values[1]) + len(values[2])))
    window.close()


if __name__ == '__main__':
    main()
