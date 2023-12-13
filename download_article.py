import base64

import requests


def download_article(baseurl):
    """
    Downloads a given article to the local filesystem

    :param baseurl: Core server url
    :type baseurl: string
    """

    print("Enter a user id:")
    userid = input()
    print("Enter an article id:")
    articleid = input()
    url = baseurl + "/download/" + articleid + "/" + userid
    res = requests.get(url, timeout=30)
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
        file_bytes = base64.b64decode(body["data"])
        filename = articleid + ".txt"
        with open(filename, "wb") as f:
            f.write(file_bytes)
        print("Downloaded to", filename)
