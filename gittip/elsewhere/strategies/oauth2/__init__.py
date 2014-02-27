from requests_oauthlib import OAuth2Session


class PlatformOAuth2(Platform):

    oauth_default_scope = None
    oauth_email_scope = None
    oauth_payment_scope = None

    def get_auth_session(self, state=None, token=None):
        return OAuth2Session(self.api_key, state=state, token=token,
                             redirect_uri=self.callback_url,
                             scope=self.oauth_default_scope)

    def get_auth_url(self, **kw):
        sess = self.get_auth_session()
        url, state = sess.authorization_url(self.auth_url+'/authorize')
        return url, state, ''

    def get_query_id(self, querystring):
        return querystring['state']

    def handle_auth_callback(self, url, state, unused_arg):
        sess = self.get_auth_session(state=state)
        sess.fetch_token(self.auth_url+'/access_token',
                         client_secret=self.api_secret,
                         authorization_response=url)
        return sess
