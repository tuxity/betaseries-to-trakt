#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import re
import json
import requests


trakt_api = 'https://api.trakt.tv'
auth_get_token_route = '%s/oauth/token' % (trakt_api)
sync_history_route = '%s/sync/history' % (trakt_api)
sync_watchlist_route = '%s/sync/watchlist' % (trakt_api)


session = requests.Session()

def login_to_trakt():

    print('')
    print('Open the link in a browser and paste the pin')
    print('https://trakt.tv/oauth/authorize?response_type=code&client_id=%s&redirect_uri=urn:ietf:wg:oauth:2.0:oob' % (os.environ.get('CLIENT_ID')))
    print('')

    pin = str(input('Pin: '))

    session.headers.update({
        'Accept':     'application/json',
        'User-Agent': 'Betaseries to Trakt',
        'Connection': 'Keep-Alive'
    })

    post_data = {
        'code':          pin,
        'client_id':     os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET'),
        'redirect_uri':  'urn:ietf:wg:oauth:2.0:oob',
        'grant_type':    'authorization_code'
    }

    request = session.post(auth_get_token_route, data=post_data)
    response = request.json()

    session.headers.update({
        'Content-Type':      'application/json',
        'trakt-api-version': '2',
        'trakt-api-key':     os.environ.get('CLIENT_ID'),
        'Authorization':     'Bearer ' + response["access_token"]
    })

def create_show_history(obj):
    id = obj[1]
    name = obj[2]
    status_pct = obj[6]

    output = re.search('S([0-9]+)E([0-9]+)', obj[4])
    last_seen_season = output.group(1)
    last_seen_episode = output.group(2)

    show = {
        'name': name,
        'ids': {
            'tvdb': id
        },
        'watched_at': 'released'
    }

    if status_pct != '100':
        show['seasons'] = []

        for s in range(0, int(last_seen_season)):
            show['seasons'].append({
                'number': s + 1,
                'watched_at': 'released'
            })

            if (s + 1) == int(last_seen_season):
                show['seasons'][s]['episodes'] = []

                for e in range(0, int(last_seen_episode)):
                    show['seasons'][s]['episodes'].append({
                        'number': e + 1,
                        'watched_at': 'released'
                    })

    return show

def create_show_watchlist(obj):
    id = obj[1]
    name = obj[2]

    show = {
        'name': name,
        'ids': {
            'tvdb': id
        }
    }

    return show

def create_movie_history(obj):
    id = obj[1]
    name = obj[2]

    movie = {
        'name': name,
        'ids': {
            'tmdb': id
        },
        'watched_at': 'released'
    }

    return movie

def create_movie_watchlist(obj):
    id = obj[1]
    name = obj[2]

    movie = {
        'name': name,
        'ids': {
            'tmdb': id
        }
    }

    return movie


def main():
    login_to_trakt()

    post_history_data = {
        'shows': [],
        'movies': []
    }

    post_watchlist_data = {
        'shows': [],
        'movies': []
    }

    for file_path in sys.argv[1::]:
        file = open(file_path, "r")
        type = None

        for row in csv.reader(file):
            if row[1] == 'thetvdb_id':
                type = 'show'
                continue

            if row[1] == 'tmdb_id':
                type = 'movie'
                continue

            if type == 'show':
                status_pct = row[6]
                if status_pct == '0':
                    post_watchlist_data['shows'].append(create_show_watchlist(row))
                else:
                    post_history_data['shows'].append(create_show_history(row))

            if type == 'movie':
                status = row[3] # '2' = je ne veux pas voir, '1' = j'ai vu, '0' = je veux voir
                if status == '0':
                    post_watchlist_data['movies'].append(create_movie_watchlist(row))
                elif status == '1':
                    post_history_data['movies'].append(create_movie_history(row))


        file.close()

    # Post 'history' data

    request_history = session.post(sync_history_route, data=json.dumps(post_history_data))
    response_history = request_history.json()

    # Post 'watchlist' data

    request_watchlist = session.post(sync_watchlist_route, data=json.dumps(post_watchlist_data))
    response_watchlist = request_watchlist.json()

    # Print summary

    print('\r\nMigration from Betaseries CSV files Done!')

    print('\r\n-----------------------------------------')
    print('HISTORY')

    print('\r\nAdded:')
    # print('\t %s shows' % response_history['added']['shows'])
    print('\t %s episodes' % response_history['added']['episodes'])
    print('\t %s movies' % response_history['added']['movies'])

    if response_history['not_found']['shows'] or response_history['not_found']['episodes'] or response_history['not_found']['movies']:
        print('Not found:')

        if len(response_history['not_found']['shows']):
            print('\t shows:')
            print(response_history['not_found']['shows'])

        if len(response_history['not_found']['episodes']):
            print('\t episodes:')
            print(response_history['not_found']['episodes'])

        if len(response_history['not_found']['movies']):
            print('\t movies:')
            print(response_history['not_found']['movies'])

    print('\r\n-----------------------------------------')
    print('WATCHLIST')

    print('\r\nAdded:')
    print('\t %s shows' % response_watchlist['added']['shows'])
    print('\t %s movies' % response_watchlist['added']['movies'])

    if response_watchlist['existing']['shows'] or response_watchlist['existing']['movies']:
        print('Existing:')
        if response_watchlist['existing']['shows']:
            print('\t %s shows' % response_watchlist['existing']['shows'])

        if response_watchlist['existing']['movies']:
            print('\t %s movies (the play count was incremented)' % response_watchlist['existing']['movies'])

    if response_watchlist['not_found']['shows'] or response_watchlist['not_found']['movies']:
        print('Not found:')

        if len(response_watchlist['not_found']['shows']):
            print('\t shows:')
            print(response_watchlist['not_found']['shows'])

        if len(response_watchlist['not_found']['movies']):
            print('\t movies:')
            print(response_watchlist['not_found']['movies'])


if __name__ == "__main__":
    main()
