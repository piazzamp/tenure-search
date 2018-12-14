import requests

base_url = 'https://api.linkedin.com'
org_search_url = base_url+'/v2/search?q=companiesV2'
auth_url = base_url+'/oauth/v2/accessToken'

client_id = # TODO: get from env
secret = # TODO: get from env

# TODO: make an API client object with its token and stuff
def org_search(keyword, token):
	params = {"baseSearchParams.keywords":keyword}
	headers = {
		'Authorization':'Bearer '+token,
		'Accept': "application/json"
	}

	print("making http call to ", org_search_url, "with token", token)
	headers = {'Authorization': 'Bearer ' + token}
	resp = requests.get(org_search_url, params=params, headers=headers)
	if resp.status_code != 200:
		print("request failed with code: "+str(resp.status_code))
		raise Exception(resp.json())
		# exit()
	
	return resp.json()


def code_to_token(code):
	access_url = 'https://www.linkedin.com/oauth/v2/accessToken'
	headers = { "Content-Type": 'application/x-www-form-urlencoded' }
	params = {
		'grant_type': 'authorization_code',
		'code': code,
		'redirect_uri': 'http://localhost:5000/done',
		'client_id': client_id,
		'client_secret': secret
	}
	resp = requests.post(access_url, headers=headers, params=params)
	if resp.status_code != 200:
		print("request failed with code: "+str(resp.status_code))
		raise Exception(resp.json())
	
	return resp.json()['access_token']

def get_current_user(token):
	me_url = 'https://api.linkedin.com/v2/me'
	headers = {
		'Authorization':'Bearer '+token,
		'Accept': "application/json"
	}
	resp = requests.get(me_url, headers=headers)
	if resp.status_code != 200:
		print("request failed with code: "+str(resp.status_code))
		raise Exception(resp.json())
		# exit()
	return resp.json()

# returns the token
def new_auth_token():
	params = {
		'grant_type':'client_credentials',
		'client_id': client_id,
		'client_secret': secret
	}
	resp = requests.get(auth_url, params=params)
	if resp.status_code != 200:
		print('auth request failed with status', resp.status_code)
		print(resp.json())
		exit()
	
	json = resp.json()
	print('token expires in: '+str(int(json['expires_in'])/60))
	return ['access_token']
	
if __name__ == '__main__':
	cli()
