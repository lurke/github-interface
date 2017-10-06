import os
import requests
import pickle
import urllib.parse as urlparse
from flask import Flask, json, abort
from flask import request as flask_request

import time

# initiate flask application
app = Flask(__name__)

# global constants and variables
CACHE_FILENAME = os.path.abspath(os.path.join(os.path.realpath(__file__), '../cache.pkl'))
GITHUB_REPO_URL = 'https://api.github.com/repos/lodash/lodash/pulls'
PULLS_PER_PAGE = 30
params = {'state': 'all'}
headers = {'User-Agent': 'Lauren Urke'}
pull_requests = []

def load_pull_requests():
    # load cache
    with open(CACHE_FILENAME, 'rb') as cache_file:
        global pull_requests
        pull_requests = pickle.load(cache_file)
    time_since_modified = time.time() - os.path.getmtime(CACHE_FILENAME)

    # check how many pull requests exist
    first_response = requests.head(GITHUB_REPO_URL, params=params, headers=headers)
    if first_response.status_code == 403:
        print("Github rate limit exceeded. Using cached file instead.")
        return
    last_page_url = first_response.links['last']['url']
    last_page = int(urlparse.parse_qs(last_page_url)['page'][0])
    params['page'] = last_page
    last_response = requests.get(GITHUB_REPO_URL, params=params, headers=headers)
    num_pulls = (last_page-1) * PULLS_PER_PAGE + len(last_response.json())

    # if there are new pull requests or if cache is more than a day old, query for pull requests and update cache
    if num_pulls > len(pull_requests) or time_since_modified > 86400:
        # TODO do we need global here?
        pull_requests = query_pull_requests(last_page)
        with open(CACHE_FILENAME, 'wb') as cache_file:
            pickle.dump(pull_requests, cache_file)

def query_pull_requests(last_page):
    pulls = []
    page = 1   # pages are 1 indexed
    while page <= last_page:
        params['page'] = page
        response = requests.get(GITHUB_REPO_URL, params=params, headers=headers)
        pulls.extend(response.json())
        page += 1
    return pulls

@app.route("/pulls/")
def get_pull_requests() :
    start_index = flask_request.args.get('start')
    end_index = flask_request.args.get('end')

    # handle start and end params
    if not start_index: start_index = 0
    if not end_index: end_index = 30
    if not start_index >= 0:
        abort(400, "Start param must be positive.")
    if not end_index >= 0:
        abort(400, "End param must be positive.")
    if end_index < start_index:
        abort(400, "End param must be greater than start param.")
    if end_index - start_index > 30:
        abort(400, "You may only request a maximum of 30 requests at a time.")

    return json.jsonify(pull_requests[start_index:end_index])

# initiate app by loading pull requests
load_pull_requests()

if __name__ == '__main__':
    app.run()