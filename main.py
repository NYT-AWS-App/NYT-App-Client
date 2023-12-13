import pathlib
import sys
from configparser import ConfigParser

from add_user import add_user
from delete_article import delete_article
from download_article import download_article
from get_users import get_users
from nyt_search import nyt_search
from search_articles import search_articles
from view_articles import view_articles

# Authors:
# Patrick Hoey, Macy Bosnich, Griffin Minster, Will Hoffmann
# Prof. Joe Hummel (initial template)
# Northwestern University
# CS 310


###################################################################
#
# prompt
#
def prompt():
    """
    Prompts the user for client options

    :return: Command to perform
    :rtype: int
    """

    print()
    print(">> Enter a command:")
    print("   0 => end")
    print("   1 => get users")
    print("   2 => add user")  # Write RDS
    print("   3 => view your saved articles")  # Read RDS
    print("   4 => delete a saved article")  # Write S3 and RDS
    print("   5 => NYT search")  # pt1: NYT API, pt2 (if save): Write RDS and S3
    print("   6 => search your saved articles")  # read RDS
    print("   7 => download a saved article")  # Write S3, read RDS

    cmd = int(input())
    return cmd


#########################################################################
# main
#
print("** Welcome to your NYT article hub **")
print()

# eliminate traceback so we just get error message:
sys.tracebacklimit = 0

#
# what config file should we use for this session?
#
CONFIG_FILE = "client-config.ini"

print("What config file to use for this session?")
print("Press ENTER to use default (client-config.ini),")
print("otherwise enter name of config file>")
s = input()

if s == "":  # use default
    pass  # already set
else:
    CONFIG_FILE = s

#
# does config file exist?
#
if not pathlib.Path(CONFIG_FILE).is_file():
    print("**ERROR: config file '", CONFIG_FILE, "' does not exist, exiting")
    sys.exit(0)

#
# setup base URL to web service:
#
configur = ConfigParser()
configur.read(CONFIG_FILE)
baseurl = configur.get("client", "webservice")

#
# main processing loop:
#
cmd = prompt()

while cmd != 0:
    if cmd == 1:
        get_users(baseurl)
    elif cmd == 2:
        add_user(baseurl)
    elif cmd == 3:
        view_articles(baseurl)
    elif cmd == 4:
        delete_article(baseurl)
    elif cmd == 5:
        nyt_search(baseurl)
    elif cmd == 6:
        search_articles(baseurl)
    elif cmd == 7:
        download_article(baseurl)
    else:
        print("** Unknown command, try again...")
    cmd = prompt()

#
# done
#
print()
print("** done **")
