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
sync_route = '%s/sync/history' % (trakt_api)


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

def create_show(obj):
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

def create_movie(obj):
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

def main():
    login_to_trakt()

    post_data = {
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
                post_data['shows'].append(create_show(row))
            if type == 'movie':
                post_data['movies'].append(create_movie(row))


        file.close()

    request = session.post(sync_route, data=json.dumps(post_data))
    response = request.json()

    print('\r\nMigration from Betaseries CSV files Done!')
    print('Added:')
    print('\t %s episodes' % response['added']['episodes'])
    print('\t %s movies' % response['added']['movies'])
    if len(response['not_found']['episodes']) or response['not_found']['movies']:
        print('Not found:')

        if len(response['not_found']['episodes']):
            print('\t episodes:')
            print(response['not_found']['episodes'])

        if len(response['not_found']['movies']):
            print('\t movies:')
            print(response['not_found']['movies'])


if __name__ == "__main__":
    main()
