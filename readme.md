<!-- PROJECT LOGO -->
<br />
<p align="center">

  <a href="https://github.com/Frinkel/cross">
    <img src="../assets/img/arrows-alt.svg?raw=true" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Cross</h3>

  <p align="center">
    A Python-based cross poster for Hubzilla and Mastodon social media accounts
    <br />
    <a href="https://github.com/Frinkel/cross"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Frinkel/cross/issues">Report Bug</a>
    ·
    <a href="https://github.com/Frinkel/cross/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Roadmap](#roadmap)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot][product-screenshot]

So I use lesser-known social media websites - mainly because I'm not much a fan of Twitter, Facebook, and
other centralized platforms. I've noticed a problem, though - it's kinda difficult for me to manage posting across
multiple accounts, which I like doing so I can be personal with close friends on one account, but also have a "safe"
account that I show people I'm not quite as comfortable around. 

This problem then increased further when I started 
moving from one platform - Mastodon - to another - Hubzilla. They both use different federating protocols, and Hubzilla 
doesn't even have a phone app available for it like Mastodon does. So, I figured I would kill two birds with one stone,
by bringing all of my accounts to one place, where I can post to as many or as little of them at the same time whenever
I'd like.


### Built With

* [Python](https://www.python.org/)
* [requests](https://2.python-requests.org/en/master/)
* [Mastodon.py](https://mastodonpy.readthedocs.io/en/stable/)
* [jsonlines](https://jsonlines.readthedocs.io/en/latest/)
* [PySimpleGUIQt](https://github.com/PySimpleGUI/PySimpleGUI/tree/master/PySimpleGUIQt)



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
You'll need to have Python 3 as well as `pip` and `virtualenv` installed. On Linux, you may or may not already have
these installed. If you don't, they should be available as packages on your distro's package manager. On Windows,
you'll need to install Python 3 from the [Python website](https://www.python.org/downloads/).

If you have Python3 and `pip` installed but not virtualenv, you should be able to install it with a simple command:
```sh
pip3 install virtualenv
```

*Note: If you have Python pre-installed, make sure you're using Python 3 and the corresponding pip version! Some Linux
distributions, for example, ship with Python 2.7 for backwards compatibility reasons, or both Python versions with 2.7
set to the default.*

Also, while not mandatory, it's highly recommended that you install Git. Many Linux distros come with it preinstalled, 
and if it's not, installation is typically as simple as installing `git` through your package manager. For Windows, 
you'll want to install [Git for Windows](https://git-scm.com/download/win). Don't worry about all of the options the
installer gives you: the defaults should be fine.

### Installation
 First, you're going to want to download the repository, then navigate into the directory. You can do this through
 Github, but if you're doing this via `git` (which, again, I recommend), you can just run the following command:
 ```sh
git clone https://github.com/Frinkel/cross.git cross
cd cross
```

From here, it's highly recommended you create a virtual environment. This will allow the app to install its own
dependencies without messing with the packages installed on your main system.
```sh 
python3 -m venv venv
```

Then, run the following to activate the virtual environment on Windows:
```sh 
venv\Scripts\activate.bat
```
If you're on Linux or Mac OS, the command would be:
```sh 
source venv/bin/activate
```
 
Now, install the package dependencies.
```sh 
pip3 install -r requirements.txt
```

### Configuration
If you attempt to launch the program right away, you'll be shooed away as you haven't set up any accounts to cross-post
over. To set this up, go to the `auth_handlers/` folder and run the corresponding script once for each account you
wish to set up with the cross-poster. The script will tell you what to do from there. Note - for `masto.py`, you will
need access to a browser.

When all's said and done, you will have a file in the root application directory, `userdata.jl`, that contains a Json
Lines-formatted list of your accounts and their credentials. Do NOT share this file with ANYONE! Doing so is the
equivalent of sharing your account details.

Note that if you need to change one of the accounts in the list, you'll need to open this file up and delete the line
corresponding to that account first. I'm hoping to add a way for the scripts to do this programmatically.

### Usage
There are two versions of the cross-poster: `poster.py` and `poster_gui.py`. It's highly recommended to use
`poster_gui.py`, as it's easier to use and has more functionality than `poster.py`, and `poster.py` has had its fair
share of weird quirks. It works if you're, say, in a console-only environment, though.

#### poster_gui.py
The window is split into two columns - on the left, you'll see all the accounts that exist in the userdata file. Hold
Shift and select the accounts you wish to post to. Then, type your post out in the message boxes to the right, then
hit "Post!" once done writing the post. (Also, FYI - please watch your character count, as the app currently can't
detect if you're going over, and posts will be rejected by your instance if it exceeds the character limit.) The window
should close after a moment of hesitation. Check the console - it will tell you if it failed to post to any one of the
instances. That's it!

#### poster.py (Not Recommended)
Upon launching, you will be greeted with a list of the different accounts that are in the userdata file. This script
will attempt to post to all of the accounts in the file.

It will ask you for a subject/content warning: either type one or leave it blank, then hit Enter. Then, it will ask you
to type the actual post out. When you're done typing, start a new line by hitting Enter, then hit Ctrl-Z or Ctrl-D to
end the post.

A preview of your post will be shown with a character count, and after 10 seconds, the post will automatically be
submitted. Please watch your character count - the app currently can't detect if you're going over, and posts will
be rejected by your instance if it exceeds the character limit.


## Troubleshooting
**Help! The app claims that my instance isn't working, but it's up and works completely!**

Please submit a bug request with your instance domain.


**I'm trying to launch the application, but it says a file doesn't exist or something?**

Make sure you've run one of the scripts in the `auth_handlers/` folder to completion.



<!-- ROADMAP -->
## Roadmap

The following are plans I have for the possible future for this application:
* Automate overwriting account entries
* Add auto-detect of character count restraints on Mastodon-based instances that support it
* Add command line arguments for the different scripts
* Add IFTTT support via Maker Webhooks (possibly?)
* Figure out/fix OAuth2 integration with Hubzilla so I can stop using basic web auth
* Attempt to plea with Twitter for a developer account and add Twitter support
* Make GUIs for the authentication handlers?
* Port this to Android and maybe even iOS if doable
* Add image attachment support
* Add support for Mastodon-specific and Hubzilla-specific post capabilities
* Make this a webapp, store account entries in relational database instead of flat file



<!-- LICENSE -->
## License
Currently not decided on a license at this exact moment, mainly because I haven't quite done the research on it just
yet! Will get that fixed soon, however!


<!-- CONTACT -->
## Contact

Holly Lotor - [hollylotor@the.chirr.space](https://the.chirr.space/profile/hollylotor) - iam@hollylotor.online

Project Link: [https://github.com/Frinkel/cross](https://github.com/Frinkel/cross)



<!-- ACKNOWLEDGEMENTS -->
## Thanks to...

* My teachers and mentors, for being patient with me
* My friends on the Fediverse for keeping me sane
* [Insomnia REST Client](https://insomnia.rest/) for saving me from a dozen headaches

[product-screenshot]: ../assets/img/CrossGUI.png?raw=true
