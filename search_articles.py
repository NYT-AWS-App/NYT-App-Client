import requests


def search_articles(baseurl):
    options = ["headline", "author", "date", "keyword"]
    found_filter = False
    search_filter = ""

    print("Enter the user_id of the user you would like to search through >")
    user_id = input()
    if not user_id.isnumeric():
        print("Invalid user id. Exiting...")
        return

    for _ in range(5):
        print(
            "What do you want to search by? [Options: headline, author, date, keyword] >"
        )
        search_filter = input()
        search_filter = search_filter.lower()

        if search_filter in options:
            found_filter = True
            break
        else:
            print("Invalid search term. Try again.")
    if not found_filter:
        print("Too many attempts. Exiting...")
        return

    if search_filter == "date":
        search_filter = "pubdate"

    print("Enter your search term >")
    search_term = input()

    data = {"userid": user_id, "filter": search_filter, "term": search_term}
    api = "/search"
    search_url = baseurl + api

    res = requests.get(search_url, json=data)

    if res.status_code != 200:
        # failed:
        print("Failed with status code:", res.status_code)
        if res.status_code == 400:
            # we'll have an error message
            body = res.json()
            print("Error message:", body)
        #
        return

    body = res.json()
    print("Here are your saved articles:\n")
    for key, art_data in body["data"].items():
        print(key)
        print("  " + art_data["headline"])
        print("  " + art_data["author"])
        print("  " + art_data["pubdate"])
        print()
    return
