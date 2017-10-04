import os
import requests
import pickle
import urllib.parse as urlparse
from flask import Flask, json, abort
from flask import request as flask_request

app = Flask(__name__)
CACHE_FILENAME = os.path.abspath(os.path.join(os.path.realpath(__file__), '../cache.pkl'))


def cache_pull_requests():
    # set up query
    url = 'https://api.github.com/repos/lodash/lodash/pulls'
    params = {'state': 'all'}
    headers = {'User-Agent': 'Lauren Urke'}

    # request the first page of pull requests to get the number of requests needed
    response = requests.get(url, params = params, headers = headers)
    last_url = response.links['last']['url']
    query_params = urlparse.parse_qs(last_url)
    last_page = int(query_params['page'][0])

    # collect all requests as pulls
    # pulls = response.json()
    # page = 2   # pages are 1 indexed and we already requested the first one
    # while page <= last_page:
    #     params['page'] = page
    #     response = requests.get(url, params = params, headers = headers)
    #     pulls.extend(response.json())
    #     page += 1

    # cache in case we exceed github's rate limit
    # with open(CACHE_FILENAME, 'wb') as cache_file:
    #     pickle.dump(pulls, cache_file)


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

    pulls = None
    with open(CACHE_FILENAME, 'rb') as cache_file:
        pulls = pickle.load(cache_file)

    return json.jsonify(pulls[start_index:end_index])

if __name__ == '__main__':
    cache_pull_requests()
    app.run()