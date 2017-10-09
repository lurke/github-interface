import os
import requests
import pickle
import math
import time
import arrow
import urllib.parse as urlparse
from flask import Flask, json, abort
from flask import request as flask_request
from flask_cors import CORS


# initiate flask application, with CORS for local deployments because of cross origin requests between localhosts
app = Flask(__name__)
CORS(app)

# global constants and variables
CACHE_FILENAME = os.path.abspath(os.path.join(os.path.realpath(__file__), '../cache.pkl'))
GITHUB_REPO_URL = 'https://api.github.com/repos/lodash/lodash/pulls'
PULLS_PER_PAGE = 30
params = {'state': 'all'}
headers = {'User-Agent': 'Lauren Urke'}
pull_requests = []

def load_pull_requests():
    """
    Function that determines whether to use cached pull requests of query github.
    Currently uses cache if the number of pull requests is unchanged and the cache is less than a day old.
    :return: None, saves pull requests in globals instead
    """

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
        pull_requests = query_pull_requests(last_page)
        # if we reached the rate limit while asking for pulls, abort and use cache instead
        if not pull_requests:
            print("Github rate limit exceeded while querying for new set of pull requests. Using cached file instead.")
            return
        with open(CACHE_FILENAME, 'wb') as cache_file:
            pickle.dump(pull_requests, cache_file)
    return

def query_pull_requests(last_page):
    """
    Function that queries github for all pull requests

    :param last_page: the total number of pages to ask for
    :return: the list pull requests
    """
    pulls = []
    page = 1   # pages are 1 indexed
    reached_rate_limit = False
    while page <= last_page:
        params['page'] = page
        response = requests.get(GITHUB_REPO_URL, params=params, headers=headers)
        # if we reached the rate limit, lets use the cache instead
        if response.status_code == 403:
            reached_rate_limit = True
            break
        pulls.extend(response.json())
        page += 1
    if reached_rate_limit: return None
    return pulls

def week_over_week():
    """
    Example query for looking at pull requests week over week as in email
    :return: A list of list of pull requests, where each top level list represents a week
    """
    # weeks will be a list of lists, with each list containing the pull requests for that week
    # week 0 will be this past week, with week 1 the week before, etc
    weeks = []
    define_week_since = time.time()      # can change to sunday at midnight if you wish
    for pull in pull_requests:
        week_created = int((define_week_since - arrow.get(pull['created_at']).float_timestamp) // 604800)     # 604800 seconds in a week
        # add empty lists for each week up to this one, if we are seeing a week for the first time
        if len(weeks) <= week_created: weeks.extend([[] for x in range(week_created + 1 - len(weeks))])
        weeks[week_created].append(pull)
    return weeks


def test_pull_requests_loaded():
    assert len(pull_requests)

@app.route("/pulls/pages/", methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_pulls_pages():
    """
    An api call that returns the total number of pages the ui will need to request.
    :return: A number of pages
    """
    return str(math.ceil(len(pull_requests)/PULLS_PER_PAGE))

@app.route("/pulls/", methods=['GET', 'OPTIONS'], strict_slashes=False)
def get_pull_requests() :
    """
    An api call that returns the pull requests for the page requested.
    :return: A list of pull request json objects
    """
    page = int(flask_request.args.get('page'))
    if not page >= 1:
        abort(400, "Page param must be 1 or greater.")

    max_page = math.ceil(len(pull_requests)/PULLS_PER_PAGE)
    if page > max_page:
        abort(400, "Page param must be less than " + max_page + ".")

    start = (page-1)*PULLS_PER_PAGE
    end = min(len(pull_requests), start+PULLS_PER_PAGE)
    return json.jsonify(pull_requests[start:end])


# initiate app by loading pull requests
load_pull_requests()

if __name__ == '__main__':
    # call desired metrics functions
    # week_over_week()

    # run simple tests
    test_pull_requests_loaded()

    # run the flask app
    app.run()