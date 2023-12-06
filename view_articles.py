import logging

import requests


def view_articles(baseurl):
    """
    Prints out a user's saved articles

    Parameters
    ----------
    baseurl: baseurl for web service

    Returns
    -------
    nothing
    """

    print("Enter a userid:")
    userid = input()

    try:
        #
        # call the web service:
        #

        data = {"userid": userid}
        api = "/articles"
        url = baseurl + api

        res = requests.get(url, json=data)

        #
        # let's look at what we got back:
        #
        if res.status_code != 200:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code == 400:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            #
            return

        #
        # deserialize and extract articles:
        #
        body = res.json()

        for a in body["articles"]:
            print(a["articleid"])
            print(" ", a["headline"])
            print(" ", a["url"])
            print(f"  {a['authorfirst']} {a['authorlast']}")
            print(f"  {a['pubdate']}\n")

    except Exception as e:
        logging.error("articles() failed:")
        logging.error(f"url: {url}")
        logging.error(e)
        return
