import hashlib
import logging
import uuid

import requests


def add_user(baseurl):
    """
    Inserts new user into RDS

    Parameters
    ----------
    baseurl: baseurl for web service

    Returns
    -------
    nothing
    """

    print("Enter a username:")
    username = input()
    print("Enter a password:")
    password = input()
    pass_hash = hashlib.sha256(password.encode()).hexdigest()
    # generate unique folder name:
    folder = str(uuid.uuid4())

    try:
        data = {"username": username, "pwdhash": pass_hash, "bucketfolder": folder}

        #
        # call the web service:
        #
        api = "/add_user"
        url = baseurl + api

        res = requests.put(url, json=data)
        #
        # let's look at what we got back:
        #
        if res.status_code != 200:
            # failed:

            if res.status_code == 400:  # username is taken
                body = res.json()
                print(body["message"])
                add_user(baseurl)
                return

            print("Failed with status code:", res.status_code)
            print("url: " + url)
            return

        #
        # deserialize and extract stats:
        #
        body = res.json()
        #
        print(f"{body['message']} with userid: {body['userid']}")

    except Exception as e:
        logging.error("stats() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return logging.error(e)
