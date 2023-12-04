import logging

import requests


def delete_article(baseurl):
    print("Enter a userid:")
    wanted_userid = input()

    print("Enter the articleid you want to delete:")
    wanted_articleid = input()

    try:
        api = "/delete"
        url = baseurl + api
        data = {"userid": wanted_userid, "articleid": wanted_articleid}

        res = requests.delete(url, json=data)

        if res.status_code != 200:
            # failed:
            print("Failed with status code:", res.status_code)
            if res.status_code == 400:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            #
            return

        print("Article successfully deleted!")
        return

    except Exception as e:
        logging.error("delete_article() failed:")
        logging.error(f"url: {url}")
        logging.error(e)
        return

        return
