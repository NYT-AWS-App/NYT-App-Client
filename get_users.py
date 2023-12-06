import logging

import requests


def get_users(baseurl):
    try:
        url = baseurl + "/users"
        res = requests.get(url)

        if res.status_code != 200:
            # failed:
            print("Failed with status code:", res.status_code)
            if res.status_code == 400:
                # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            return
        else:
            body = res.json()
            for user in body["users"]:
                print(user["userid"])
                print(f"  {user['username']}")
                print(f"  {user['pwdhash']}")
                print(f"  {user['bucketfolder']}\n")

    except Exception as e:
        logging.error("delete_article() failed:")
        logging.error(f"url: {url}")
        logging.error(e)
        return
