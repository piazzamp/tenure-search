import flask
from flask_oauthlib.provider import OAuth2Provider
import main
from urllib.parse import urlencode

app = flask.Flask(__name__)
oauth_provider = OAuth2Provider(app)

@app.route('/')
def home():
    login_url = 'https://www.linkedin.com/oauth/v2/authorization'
    params = {
        'response_type': 'code',
        'client_id': main.client_id,
        'redirect_uri': 'http://localhost:5000/done',
        'state': 'TODO',
        'scope': 'r_basicprofile'
    }
    login_url = login_url+'?'+urlencode(params)
    return flask.redirect(login_url)

@app.route("/done")
def done():
    code = flask.request.args.get('code', '')
    # make the code a token
    token = main.code_to_token(code)

    # make the api call
    try:
        resp = main.get_current_user(token)
        # resp = main.org_search('PhishLabs', token)
        print(resp)
        return resp
    except Exception as e:
        return str(e)