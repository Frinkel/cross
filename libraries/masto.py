import mastodon


def attempt_authenticate(masto_auth, login_code, scopes):
    try:
        return masto_auth.log_in(code=login_code, scopes=scopes)
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


def get_session_and_login_url(instance, client_id, client_secret, scopes):
    try:
        masto_auth = mastodon.Mastodon(client_id=client_id, client_secret=client_secret,
                                       api_base_url='https://' + instance)
        login_url = masto_auth.auth_request_url(client_id=client_id, scopes=scopes, force_login=True)
        return masto_auth, login_url
    except mastodon.MastodonNetworkError:
        print("Couldn't connect to the instance for some reason, bailing...")
        exit(1)
    except mastodon.MastodonError:
        print("Something happened! (Something happened!)")
        exit(2)


def get_username(client_id, client_secret, access_token, instance):
    try:
        masto_session = mastodon.Mastodon(client_id=client_id, client_secret=client_secret,
                                          access_token=access_token, api_base_url='https://' + instance)
        masto_acct_info = masto_session.account_verify_credentials()
        username = masto_acct_info['username']
        return username
    except mastodon.MastodonError:
        print("Something happened! (Something happened!)")
        exit(2)