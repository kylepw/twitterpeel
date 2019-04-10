from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
import logging


logging.basicConfig(level=logging.DEBUG)

session = requests.Session()


def get_tweets(user, pages=20):
    '''Get `user` tweets via Twitter frontend API.

    Note:
        Based on Kenneth Reitz's twitter_scraper.
        https://github.com/kennethreitz/twitter-scraper/blob/master/twitter_scraper.py

    '''

    url = f'https://twitter.com/i/profiles/show/{user}/timeline/tweets?include_available_features=1&include_entities=1&include_new_items_bar=true'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': f'https://twitter.com/{user}',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'X-Twitter-Active-User': 'yes',
        'X-Twitter-Active-User': 'yes',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'en-us',
    }

    def gen_tweets(pages):
        r = session.get(url, headers=headers)

        while pages > 0:
            try:
                soup = BeautifulSoup(r.json()['items_html'], features='lxml')
            except KeyError:
                raise ValueError(f'User {user} does not exist or is private.')

            comma = ','
            dot = '.'
            tweets = []
            for tweet in soup.find_all(class_='stream-item'):
                text = tweet.find(class_='tweet-text').text

                tweet_id = tweet['data-item-id']

                time = datetime.fromtimestamp(int(tweet.find(class_='_timestamp')['data-time']))

                actions = [
                    a.text.strip() for a in tweet.find_all(class_='ProfileTweet-actionCount')
                ]

                replies = int(actions[0].split(' ')[0].replace(comma, '').replace(dot, ''))

                retweets = int(actions[1].split(' ')[0].replace(comma, '').replace(dot, ''))

                likes = int(actions[2].split(' ')[0].replace(comma, '').replace(dot, ''))

                hashtags = [
                    hashtag.text
                    for hashtag in tweet.find_all(class_='twitter-hashtag')
                ]

                urls = [
                    url_node['data-expanded-url']
                    for url_node in tweet.find_all('a', class_='twitter-timeline-link')
                    if 'u-hidden' not in url_node['class']
                ]

                photos = [
                    photo_node['data-image-url']
                    for photo_node in tweet.find_all(class_='AdaptiveMedia-photoContainer')
                ]

                videos = []
                video_nodes = tweet.find_all(class_='PlayableMedia-player')
                for node in video_nodes:
                    styles = node['style'].split()
                    for style in styles:
                        if style.startswith('background'):
                            video_id = style.split('/')[-1].split('.')[0]
                            videos.append({'id': video_id})

                tweets.append({
                    'tweetid': tweet_id,
                    'time': time,
                    'text': text,
                    'replies': replies,
                    'retweets': retweets,
                    'likes': likes,
                    'entries': {
                        'hashtags': hashtags, 'urls': urls,
                        'photos': photos, 'videos': videos
                    }
                })

            last_tweetid = tweets[-1]['tweetid']

            for tweet in tweets:
                if tweet:
                    tweet['text'] = re.sub(r'\Shttp', ' http', tweet['text'], 1)
                    tweet['text'] = re.sub(r'\Spic\.twitter', ' pic.twitter', tweet['text'], 1)
                yield tweet

            r = session.get(url, params={'max_position': last_tweetid}, headers=headers)
            pages -= 1

    return gen_tweets(pages)
