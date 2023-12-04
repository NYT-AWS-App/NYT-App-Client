import pathlib
import sys
from configparser import ConfigParser

from add_user import add_user
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
# classes
#
class User:
    userid: int
    username: str
    pwhash: str
    bucketfolder: str


class Article:
    articleid: int
    userid: int
    url: str
    headline: str
    pubdate: str
    newsdesk: str
    sectionname: str
    authorfirst: str
    authorlast: str
    bucketkey: str


###################################################################
#
# prompt
#
def prompt():
    """
    Prompts the user and returns the command number

    Parameters
    ----------
    None

    Returns
    -------
    Command number entered by user (0, 1, 2, ...)
    """
    print()
    print(">> Enter a command:")
    print("   0 => end")
    print("   1 => add user")  # Write RDS
    print("   2 => view your saved articles")  # Read RDS
    print("   3 => delete a saved article")  # Write S3 and RDS
    print("   4 => NYT search")  # pt1: NYT API, pt2 (if save): Write RDS and S3
    print("   5 => search your saved articles")  # read RDS
    print("   6 => download a saved article")  # Write S3, read RDS

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
config_file = "client-config.ini"

print("What config file to use for this session?")
print("Press ENTER to use default (client-config.ini),")
print("otherwise enter name of config file>")
s = input()

if s == "":  # use default
    pass  # already set
else:
    config_file = s

#
# does config file exist?
#
if not pathlib.Path(config_file).is_file():
    print("**ERROR: config file '", config_file, "' does not exist, exiting")
    sys.exit(0)

#
# setup base URL to web service:
#
configur = ConfigParser()
configur.read(config_file)
baseurl = configur.get("client", "webservice")

#
# main processing loop:
#
cmd = prompt()

while cmd != 0:
    #
    if cmd == 1:
        add_user(baseurl)
    elif cmd == 2:
        view_articles(baseurl)
    elif cmd == 4:
        nyt_search(baseurl)
    elif cmd == 5:
        search_articles(baseurl)
    else:
        print("** Unknown command, try again...")
    cmd = prompt()

#
# done
#
print()
print("** done **")
