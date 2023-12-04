import json
import re

import requests


def nyt_search(baseurl):
    options = ["keyword", "author", "title", "date"]
    found_filter = False
    search_filter = ""

    for _ in range(5):
        print(
            "What do you want to search by? [Options: keyword, author, title, date] >"
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

    ## search filter + search term
    search_term = ""
    valid = False
    for _ in range(5):
        if search_filter == "author":
            print("Enter your search term (Format: FirstName LastName)>")
            search_term = input()
            search_term = search_term.lower()
            if re.match(r"^[a-zA-Z]+ [a-zA-Z]+$", search_term):
                valid = True
                break
            else:
                print(
                    "Reenter your search term in the correct format (Format: FirstName LastName)>"
                )
        elif search_filter == "date":
            print("Enter your search term (Format: YYYY-MM-DD)>")
            search_term = input()
            search_term = search_term.lower()
            if re.match(r"^\d{4}-\d{2}-\d{2}$", search_term):
                valid = True
                break
            else:
                print(
                    "Reenter your search term in the correct format (Format: YYYY-MM-DD)>"
                )
        else:
            print("Enter your search term >")
            search_term = input()
            search_term = search_term.lower()
            valid = True
            break

    if not valid:
        print("Too many attempts. Exiting...")
        return

    ## article search back
    url = (
        baseurl + f"/nyt_search?search_term={search_term}&search_filter={search_filter}"
    )

    res = requests.get(url)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
        # failed:
        print("Failed with status code:", res.status_code)
        print("url: " + url)
        if res.status_code == 400:
            # we'll have an error message
            body = res.json()
            print("Error message:", body)
        #
        return

    #
    # deserialize and extract results:
    #
    body = res.json()

    ## From body: We want the uuid, headline (title), author, date, description, url
    ## Map uuids to numbers from 1 to 10
    number_to_nyt_obj = {}

    wanted_fields = [
        "web_url",
        "lead_paragraph",
        "headline",
        "keywords",
        "pub_date",
        "news_desk",
        "section_name",
        "byline",
        "_id",
    ]
    print(len(body["data"]["response"]["docs"]))
    ## Display headlines w/ mapped to numbers
    for i, article_chunk in enumerate(body["data"]["response"]["docs"]):
        number_to_nyt_obj[i + 1] = {}
        for name, value in article_chunk.items():
            if name in wanted_fields:
                if name == "_id":
                    match = re.search(r"nyt://.*/([^/]+)", value)
                    number_to_nyt_obj[i + 1]["bucketkey"] = match.group(1)
                elif name == "keywords":
                    for key in value:
                        if "keywords" not in number_to_nyt_obj[i + 1]:
                            number_to_nyt_obj[i + 1]["keywords"] = [key["value"]]
                        else:
                            number_to_nyt_obj[i + 1]["keywords"].append(key["value"])
                elif name == "byline":
                    if len(value["person"]) != 0:
                        number_to_nyt_obj[i + 1]["first_name"] = value["person"][0][
                            "firstname"
                        ]
                        number_to_nyt_obj[i + 1]["last_name"] = value["person"][0][
                            "lastname"
                        ]
                    else:
                        number_to_nyt_obj[i + 1]["first_name"] = ""
                        number_to_nyt_obj[i + 1]["last_name"] = ""
                elif name == "headline":
                    number_to_nyt_obj[i + 1]["headline"] = value["main"]
                else:
                    number_to_nyt_obj[i + 1][name] = value
        print(f'{i+1}.) {number_to_nyt_obj[i + 1]["headline"]}')

    ## Prompt the user and ask if they want to save to their saved articles
    print("If you want to save an article, enter the story's ID [1-10] >")
    article_number = input()
    if (
        not article_number.isnumeric()
        or int(article_number) < 1
        or int(article_number) > 10
    ):
        print("Exiting...")
        return

    article_number = int(article_number)

    print("Enter User ID (Format: #####)>")
    user_id = input()
    for _ in range(3):
        if not user_id.isnumeric():
            print("Enter User ID (Format: #####)>")
            user_id = input()
        else:
            break
    if not user_id.isdigit():
        print("Too many attempts. Exiting...")
        return

    nyt_obj = number_to_nyt_obj[article_number]
    save_article(baseurl, nyt_obj, user_id)
    return


def save_article(baseurl, nyt_obj, user_id):
    save_url = baseurl + f"/save?userid={user_id}"
    data = json.dumps(nyt_obj)
    res = requests.put(save_url, json=data)
    if res.status_code == 200:
        print("Article saved successfully!")
        return
    elif res.status_code == 203:
        print("Article already saved.")
        return
    else:
        print("Failed with status code:", res.status_code)
        print("url: " + save_url)
        if res.status_code == 400:
            # we'll have an error message
            body = res.json()
            print("Error message:", body)
        return

    ## Send save api call to server, with data in the body of request
    ## Send save api call to server, with data in the body of request        ## Send save api call to server, with data in the body of request
    ## Send save api call to server, with data in the body of request
