from flask import Flask, jsonify
import feedparser
import requests
import re
import datetime
import os
from google.cloud import secretmanager

app = Flask(__name__)

project_id = os.environ["PROJECT_ID"]

# pull the feed url from google secret manager
client = secretmanager.SecretManagerServiceClient()
name = f"projects/{project_id}/secrets/feed/versions/latest"
response = client.access_secret_version(name=name)
feed = response.payload.data.decode("UTF-8")

# Route to fetch and return the RSS feed as JSON
@app.route('/')
def fetch_feed():
    try:
        # Fetch the RSS feed using the proxy server
        response = requests.get(feed)
        xml_string = response.text
        feed_parsed = feedparser.parse(xml_string)

        if 'entries' in feed_parsed:
            if 'summary' in feed_parsed.entries[0]:
                a=re.findall(r'issue=[0-9]+', feed_parsed.entries[0].summary )
                if len(a)==0:
                    return jsonify({'success': False, 'error': 'cant grep issue number from summary'})
                current_issue=a[0].split('=')[1]
            else:
                return jsonify({'success': False, 'error': 'no summary entry found in rss'})

            if 'published' in feed_parsed.entries[0]:
                published_date=feed_parsed.entries[0].published
            else:
                return jsonify({'success': False, 'error': 'no entries in rss'})
        else:
            return jsonify({'success': False, 'error': 'no entries in rss'})

        return jsonify({'success': True, 'published_date': published_date, 'issue': current_issue, 'asof_utc': int(datetime.datetime.utcnow().timestamp()) })
    except Exception as e:
       return jsonify({'success': False, 'error': str(e)})
