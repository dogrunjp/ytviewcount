# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime, timedelta
import httplib2
import os
import urllib2
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.readonly",
  "https://www.googleapis.com/auth/yt-analytics.readonly"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_ANALYTICS_API_SERVICE_NAME = "youtubeAnalytics"
YOUTUBE_ANALYTICS_API_VERSION = "v1"

##  your own parameters
# Native aplication client JSON
CLIENT_SECRETS_FILE = "client_secret.json"
# API_KEY is Public API acess key
API_KEY = ""
JSON_NAME = datetime.now().strftime('%Y-%m-%d') + "_viewcount.json"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the Developers Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=" ".join(YOUTUBE_SCOPES),
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)
    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    http = credentials.authorize(httplib2.Http())

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                   http=http)
    youtube_analytics = build(YOUTUBE_ANALYTICS_API_SERVICE_NAME,
                              YOUTUBE_ANALYTICS_API_VERSION, http=http)

    return (youtube, youtube_analytics)

def get_channel_id(youtube):
    channels_list_response = youtube.channels().list(
        mine = True,
        part = "id"
    ).execute()

    return channels_list_response["items"][0]["id"]

def run_analytics_report(youtube_analytics, channel_id, options):
    # call analytics API to retrieve a report.
    analytics_query_response = youtube_analytics.reports().query(
        ids = "channel==%s" %channel_id,
        metrics = options.metrics,
        dimensions = options.dimensions,
        start_date = options.start_date,
        end_date = options.end_date,
        max_results = options.max_results,
        sort = options.sort
    ).execute()

    print "Analytics Data for Channel %s" % channel_id

    for column_header in analytics_query_response.get("columnHeaders", []):
        print "%-20s" % column_header["name"],
    print

    for row in analytics_query_response.get("rows", []):
        # row[0]がvideo id
        id = row[0]
        url = "https://www.googleapis.com/youtube/v3/videos?part=id%2Csnippet&id=" + id + "&key=" + API_KEY
        response = urllib2.urlopen(url)
        item = json.load(response)
        title = item["items"][0]["snippet"]["title"]

        for value in row:
            print "%-20s" % value,
        print title

def get_analytics_json(youtube_analytics, channel_id, options):
    analytics_query_response = youtube_analytics.reports().query(
        ids = "channel==%s" %channel_id,
        metrics = options.metrics,
        dimensions = options.dimensions,
        start_date = options.start_date,
        end_date = options.end_date,
        max_results = options.max_results,
        sort = options.sort
    ).execute()

    print "Analytics Data for Channel %s" % channel_id

    viewcount = []

    for row in analytics_query_response.get("rows", []):
        # query_responseの行数くりかえす
        dct = {}
        for i, column_header in enumerate(analytics_query_response.get("columnHeaders", [])):
            # columnHeadersの長さ繰り返す
            dct[column_header["name"]] = row[i]
        # YT DATA APIよりidからvideoのタイトルを取得する。
        id = row[0]
        url = "https://www.googleapis.com/youtube/v3/videos?part=id%2Csnippet&id=" + id + "&key=" + API_KEY
        response = urllib2.urlopen(url)
        item = json.load(response)
        title = item["items"][0]["snippet"]["title"]
        dct["title"] = title
        viewcount.append(dct)

    with open(JSON_NAME, 'w') as f:
            json.dump(viewcount, f, ensure_ascii=False)


if __name__ == "__main__":
    now = datetime.now()
    one_day_ago = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    one_week_ago = (now - timedelta(days=7)).strftime("%Y-%m-%d")

    argparser.add_argument("--metrics", help="Report metrics",
                           default="views,comments,favoritesAdded,favoritesRemoved,likes,dislikes,shares")
    argparser.add_argument("--dimensions", help="Report dimensions",
                           default="video")
    argparser.add_argument("--start-date", default=one_week_ago,
                           help="Start date, in YYYY-MM-DD format")
    argparser.add_argument("--end-date", default=one_day_ago,
                           help="End date, in YYYY-MM-DD format")
    argparser.add_argument("--max-results", help="Max results", default=10)
    argparser.add_argument("--sort", help="Sort order", default="-views")
    args = argparser.parse_args()

    (youtube, youtube_analytics) = get_authenticated_service(args)
    try:
        channel_id = get_channel_id(youtube)
        # channel_idは取得できている模様
        # run_analytics_report(youtube_analytics, channel_id, args)
        get_analytics_json(youtube_analytics, channel_id, args)
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" %(e.resp.status, e.content)

