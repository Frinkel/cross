<!-- PROJECT LOGO -->
<br />
<p align="center">
<!--
  <a href="https://github.com/Frinkel/cross">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
-->
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



### Installation
 


<!-- ROADMAP -->
## Roadmap

The following are plans I have for the possible future for this application:
* Automate overwriting account entries
* Add IFTTT support via Maker Webhooks (possibly? Character limits may make that difficult)
* Figure out/fix OAuth2 integration with Hubzilla so I can stop using basic web auth
* Attempt to plea with Twitter for a developer account and add Twitter support
* Make GUIs for the authentication handlers?
* Port this to Android and maybe even iOS if doable - either would be a challenge
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
