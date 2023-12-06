import base64

import requests


def download_article(baseurl):
    """
    Downloads an article given its articleid

    Parameters
    ----------
    baseurl: baseurl for web service

    Returns
    -------
    nothing
    """
    print("Enter a user id:")
    userid = input()
    print("Enter an article id:")
    articleid = input()
    url = baseurl + "/download/" + articleid + "/" + userid
    res = requests.get(url)
    if res.status_code != 200:
        # failed:
        print("Failed with status code:", res.status_code)
        if res.status_code == 400:
            # we'll have an error message
            body = res.json()
            print("Error message:", body["message"])
        #
        return
    else:
        body = res.json()
        print(body["message"])
        bytes = base64.b64decode(body["data"])
        filename = articleid + ".txt"
        with open(filename, "wb") as f:
            f.write(bytes)
        print("Downloaded to", filename)
