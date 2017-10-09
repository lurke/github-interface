# github-interface

A project to grab the pull requests from the Lodash Github repository (https://github.com/lodash) and display them in a simple dashboard. Created using Python 3, Flask, React, and NPM. 

## Table of Contents

- [Installation](#installation)
- [Comments](#comments)

## Installation

To get this project up and running:
1. Download repository from github
2. Make sure you have Python 3 installed
3. cd to `/{installation_path}/github-interface` and run `pip3 install -r requirements.txt` to install all requirements.
4. Start the flask app:
   1. Run `export FLASK_APP=interface.py` to set the correct flask app file name
   2. Run `export FLASK_DEBUG=1` to change to debug mode so the code auto refreshes
   3. Run `flask run` to run the application. This should direct you to a url to hit for the basic api. 
   4. If the url is not `http://127.0.0.1:5000`, go into the `/dashboard/js/constants.js` and update the `FLASK_APP_URL` var to be consistent with the url given to you by the run command.
5. Start the react app, which is located at the `/dashboard` path
  1. Make sure you have npm installed (`brew install npm` if you use homebrew)
  2. cd into the `/github-interface/dashboard` folder
  3. Run `npm install` to install dependencies
  4. Run `npm start` to start the web server and paste the given url into your browser

## Comments

When starting this project, I wanted to make sure I was covering as much of the requested features as I could. I decided to include a very simple react ui as this dashboard, even though it wasn't mentioned in the email, because James Lloyd had mentioned a dashboard for this project on the phone with me. Because I am not primarily a UI developer, I kept this dashboard as simple as possible. It asks for the pull requests from the Flask API and displays them in a list format, with the possibility to ask for more, which then get appended onto the list. I chose not to spend time on a fancy paginator here, but there are many helpful react plugins for doing so if necessary. I do want to highlight that I think of myself as full-stack developer that mostly does back-end development. I have some experience with UIs but its by far not my main focus.

I decided to cache the pull requests in a pickle file, in case we exceeded the github rate limit. Right now, we use the cache if the number of pull requests has stayed the same and it is less than a day old. It would be easy to change these specifications or reduce the time a cache is considered valid if necessary.

Because the project scope was fairly small, I decided to keep everything in the root directory, with the main functionality in the class, interface.py. The directory for the react app is also placed at this root, found in `dashboard`.

To keep the pull requests in memory, I decided to use a global variable. I considered using a class, but thought that for this limited scope, it did not make sense. I wanted to have it in a global so that we could instantiate it on server start and then use it widely throughout for various metrics and other computations. 

Interface.py can be broken down as follows. On server start, it loads the pull requests, first checking the validity of the cache and if necessary, querying github for all the pull requests. These are loaded into a global variable. There are two methods for the Flask api that service my simple ui. These are almost redundant with github's api currently, but I implemented my own api so that could filter or modify the pull request objects to feed to the ui in the future. Interface.py also includes one sample method that sorts the pull requests into lists based on week, which was the example query given in the email instructions. This demonstrates how to use the pull requests in memory to run analytics, and can be commented in in the main function.
