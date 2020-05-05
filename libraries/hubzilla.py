import requests
import base64

# Function to check if the instance has a host-meta page in the /.well-known/ directory.
# The base Hubzilla install has this up, and it's kinda necessary for federation to work.
# That being said, this IS a heuristic - there are plugins for Hubzilla that explicitly disable federation.
# Might be worth looking down the line to see if there's a configuration that makes a valid instance fail this check.
def basic_check(instance):
    host_meta_url = "https://" + instance + "/.well-known/host-meta"
    # Sends a web request to the host-meta page on the instance given.
    host_meta = requests.request("GET", host_meta_url)
    # Check to see if the request returned with a 200 OK status code and return T/F based on that.
    if host_meta.status_code == 200:
        return True
    return False


# Check if the instance has a node_info page. If so, we can 100% confirm or deny it's a Hubzilla instance.
def check_nodeinfo(instance):
    nodeinfo_url = "https://" + instance + "/nodeinfo/2.0"
    nodeinfo_req = requests.request("GET", nodeinfo_url)
    if nodeinfo_req.status_code == 404:
        # The nodeinfo check failed completely, but this is inconclusive.
        # The Diaspora Statistics plugin has to be enabled for this check to work on a Hubzilla instance.
        # So, we're just gonna return True.
        return True
    # Obtain a JSON-formatted version of the returned data.
    nodeinfo = nodeinfo_req.json()
    # Check the key under software.name. /nodeinfo/2.0 on my instances returns hubzilla, and /1.0 returns redmatrix.
    # I'm including them both for sanity's sake.
    if nodeinfo["software"]["name"] in ("hubzilla", "redmatrix"):
        return True
    # If we get here, this key doesn't exist or includes something other than those two names.
    # We're going to assume this is not a Hubzilla instance.
    return False


# Smash the username and password into a base64-encoded string suitable for webauth.
def base64_creds(channel_name, password):
    # Yep, this is the format. Hope your password doesn't have a colon in it! 8D
    creds = channel_name + ":" + password
    # I have to admit, I don't understand why I have to encode the base64 like this, it seems redundant.
    # It's what the samples I found on the net claim is how to do it, though, and it Works(tm), so...
    creds64 = str(base64.b64encode(creds.encode("utf-8")), "utf-8")
    return creds64


# Attempts to authenticate and pull info using the credentials given using the Hubzilla API.
def check_usercred(instance, b64creds):
    # And then we put this into the authorization header.
    usercheck_header = {'authorization': "Basic " + b64creds}

    # Any API call that requires authentication should do here. I'm just using the basic channel export API function.
    usercheck_url = "https://" + instance + "/api/z/1.0/channel/export/basic"
    # Specifying the absolute basics, I only care about the status code.
    usercheck_params = {"sections": "channel", "posts": "0"}
    # Actually put forth the request.
    usercheck = requests.request("POST", usercheck_url, data="", headers=usercheck_header, params=usercheck_params)

    # If the request came out OK, return True. If not, return False.
    if usercheck.status_code == 200:
        return True
    return False