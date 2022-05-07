from requests_oauthlib import OAuth1Session

class TwitAuth:
    def __init__(self, key: str, secret: str):
        self.oauth = OAuth1Session(key, client_secret=secret)
        self.secret = secret
        self.key = key

    # Get the tokens
    def fetch_oauth_tokens(self):
        r = self.oauth.fetch_request_token(
            "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
        )
        print(f"Authoization Required: ", 
            self.oauth.authorization_url("https://api.twitter.com/oauth/authorize")
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
    
    # Createa new tweet
    def create_tweet(self, oauth: OAuth1Session, message: str):
        return oauth.post("https://api.twitter.com/2/tweets", json={"text": message})



if __name__ == "__main__":
    twit_auth = TwitAuth(
        key="YOUR TWITTER API KEY",
        secret="YOUR TWITTER API SECRET"
    )
    oauth = twit_auth.fetch_auth_session()

    # Create new tweets
    r = twit_auth.create_tweet(oauth, "New Claim! Pine")
    print(f"{r.status_code}: {r.json()}")

    r2 = twit_auth.create_tweet(oauth, "New Claim! Dan")
    print(f"{r2.status_code}: {r2.json()}")


# For the name claimer
# if claim:
#   twit_auth.create_tweet(oauth, f"New Claim! {name}")