from requests_oauthlib import OAuth1Session


class PlatformOAuth1(Platform):

    request_token_path = '/oauth/request_token'
    authorize_path = '/oauth/authorize'
    access_token_path = '/oauth/access_token'

    def get_auth_session(self, token=None, token_secret=None):
        return OAuth1Session(self.api_key, self.api_secret, token, token_secret,
                             callback_uri=self.callback_url)

    def get_auth_url(self, **kw):
        sess = self.get_auth_session()
        r = sess.fetch_request_token(self.auth_url+self.request_token_path)
        url = sess.authorization_url(self.auth_url+self.authorize_path)
        return url, r['oauth_token'], r['oauth_token_secret']

    def get_query_id(self, querystring):
        return querystring['oauth_token']

    def handle_auth_callback(self, url, token, token_secret):
        sess = self.get_auth_session(token=token, token_secret=token_secret)
        sess.parse_authorization_response(url)
        sess.fetch_access_token(self.auth_url+self.access_token_path)
        return sess
