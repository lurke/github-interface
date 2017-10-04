import os
import requests
import pickle
import urllib.parse as urlparse

def get_pull_requests() :
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
    cache_filename = os.path.abspath(os.path.join(os.path.realpath(__file__), '../cache.pkl'))
    # with open(cache_filename, 'wb') as cache_file:
    #     pickle.dump(pulls, cache_file)
    pulls = None
    with open(cache_filename, 'rb') as cache_file:
        pulls = pickle.load(cache_file)

    # compute metrics on pulls, if desired
    # TODO

if __name__ == '__main__':
    get_pull_requests()