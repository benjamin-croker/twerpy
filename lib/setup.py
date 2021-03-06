import argparse
import logging
import os

import database as db


def gen_parser():
    parser = argparse.ArgumentParser(add_help=False)

    # add common arguments
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--debug", action="store_true", help="Show debug information")
    common.add_argument("-d", "--database")

    subparsers = parser.add_subparsers()
    # set up arguments for the setup command
    setup_p = subparsers.add_parser("setup", parents=[common],
            help="""Set up the authentication, database and sentiment classifier.
            If a database is specified with the --database option, only the database is set up""")
    setup_p.set_defaults(which="setup")

    # set up arguments for the search-tweets command
    search_tweets_p = subparsers.add_parser("search-tweets", parents=[common],
            help="Search for tweets about specific topics")
    search_tweets_p.add_argument("filename")
    search_tweets_p.add_argument("--no_RT",
            help="do not include retweets in the search", action="store_true")
    search_tweets_p.set_defaults(which="search-tweets")

    # set up arguments for the search-users command
    search_users_p = subparsers.add_parser("search-users", parents=[common],
            help="Search users who recently tweeted about specific topics")
    search_users_p.add_argument("filename")
    search_users_p.set_defaults(which="search-users")

    # set up arguments for the get-home-timeline command
    search_home_timeline_p = subparsers.add_parser("get-home-timeline", parents=[common],
            help="Get tweets from your home timeline")
    search_home_timeline_p.add_argument("-g", "--group",
            help="Specify a group")
    search_home_timeline_p.set_defaults(which="get-home-timeline")

    # set up arguments for the search-top-users command
    search_top_user_p = subparsers.add_parser("search-top-users", parents=[common],
            help="Search for the top users on specific topics")
    search_top_user_p.add_argument("term")
    search_top_user_p.add_argument("-g", "--group",
            help="Specify a group")
    search_top_user_p.set_defaults(which="search-top-users")

    # set up arguments for the search-user-tweets command
    search_user_tweets_p = subparsers.add_parser("search-user-tweets", parents=[common],
            help="Search for tweets from specific users")
    search_user_tweets_p.add_argument("filename")
    search_user_tweets_p.set_defaults(which="search-user-tweets")

    # set up arguments for the search-suggested-users command
    search_suggested_users_p = subparsers.add_parser("search-suggested-users", parents=[common],
            help="Search for suggested users. Outputs the user and category")
    search_suggested_users_p.set_defaults(which="search-suggested-users")

    # set up arguments for the search-trends command
    search_trends_p = subparsers.add_parser("search-trends", parents=[common],
            help="Search trending terms for the given WOEID")
    search_trends_p.add_argument("WOEID")
    search_trends_p.add_argument("-g", "--group",
            help="Specify a group")
    search_trends_p.set_defaults(which="search-trends")

    # set up arguments for the dump-tweets command
    dump_tweets_p = subparsers.add_parser("dump-tweets", parents=[common],
            help="Dumps all the tweet data to tweets.csv in the 'reports' directory, or in a location specified by the -o option")
    dump_tweets_p.add_argument("-g", "--group",
            help="Specify a group")
    dump_tweets_p.add_argument("-o", "--output",
            help="Output filename")
    dump_tweets_p.add_argument("--json", help="Report data in JSON format")
    dump_tweets_p.set_defaults(which="dump-tweets")

    # set up arguments for the dump-users command
    dump_users_p = subparsers.add_parser("dump-users", parents=[common],
            help="Dumps all the user data to users.csv in the 'reports' directory, or in a location specified by the -o option")
    dump_users_p.add_argument("-g", "--group",
            help="Specify a group")
    dump_users_p.add_argument("-o", "--output",
            help="Output filename")
    dump_users_p.add_argument("--json", help="Report data in JSON format")
    dump_users_p.set_defaults(which="dump-users")

    return parser


def setup_db(db_filename):
    logging.info("Creating new database file {0} in data directory".format(db_filename))
    db.reset(db_filename)


def setup_all():
    def _join_to_data_dir(filename):
        # this file is  twerpy/lib/setup.py, so navigate to twerpy/
        # the join with data/ to get twerpy/data/
        return os.path.join(
                os.path.dirname(os.path.dirname(
                        os.path.abspath(__file__))),
                "data", filename)

    access_token_key = raw_input("Enter access token key: ")
    access_token_secret = raw_input("Enter access token secret: ")
    consumer_key = raw_input("Enter consumer key: ")
    consumer_secret = raw_input("Enter consumer secret: ")

    default_db_filename = raw_input("Enter default database file name\n" +
                                  "Leave blank to use 'tweets.db'")
    if len(default_db_filename) == 0:
        default_db_filename = "tweets.db"

    with open(_join_to_data_dir("user_settings.py"), "w") as settings_file:
        settings_file.write("access_token_key = \"{0}\"\n".format(access_token_key))
        settings_file.write("access_token_secret = \"{0}\"\n".format(access_token_secret))
        settings_file.write("consumer_key = \"{0}\"\n".format(consumer_key))
        settings_file.write("consumer_secret = \"{0}\"\n".format(consumer_secret))
        settings_file.write("default_db_filename = \"{0}\"\n".format(default_db_filename))

    db.reset(_join_to_data_dir(default_db_filename))
