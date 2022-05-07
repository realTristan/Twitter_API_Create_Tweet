from requests_oauthlib import OAuth1Session

class TwitAuth:
    def __init__(self, key: str, secret: str):
        self.session = OAuth1Session(key, client_secret=secret)
        self.secret = secret
        self.key = key

    # Get the tokens
    def fetch_oauth_tokens(self):
        r = self.session.fetch_request_token(
            "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
        )
        print(f"Authoization Required: ", 
           self.session.authorization_url("https://api.twitter.com/oauth/authorize")
        )
        return OAuth1Session(self.key,
            client_secret=self.secret,
            resource_owner_key=r.get('oauth_token'),
            resource_owner_secret=r.get("oauth_token_secret"),
            verifier=input("Enter Authorization PIN: "),
        ).fetch_access_token("https://api.twitter.com/oauth/access_token")


    # Get final post session
    def fetch_auth_session(self):
        tokens = self.fetch_oauth_tokens()
        return OAuth1Session(self.key,
            client_secret=self.secret,
            resource_owner_key=tokens["oauth_token"],
            resource_owner_secret=tokens["oauth_token_secret"],
        )
    
    # Create a new tweet
    def create_tweet(self, session: OAuth1Session, message: str):
        return session.post("https://api.twitter.com/2/tweets", json={"text": message})



if __name__ == "__main__":
    twit_auth = TwitAuth(
        key="YOUR TWITTER API KEY",
        secret="YOUR TWITTER API SECRET"
    )
    session = twit_auth.fetch_auth_session()

    # Create new tweets
    r = twit_auth.create_tweet(session, "Message 1")
    print(f"{r.status_code}: {r.json()}")

    r2 = twit_auth.create_tweet(session, "Message 2")
    print(f"{r2.status_code}: {r2.json()}")
