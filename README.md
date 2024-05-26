betaseries-to-trakt
===========

Import your [Betaseries](https://www.betaseries.com) account's TV shows informations into your [Trakt.tv](https://trakt.tv) account.

[![](https://images.microbadger.com/badges/version/tuxity/betaseries-to-trakt.svg)](https://hub.docker.com/r/tuxity/betaseries-to-trakt/)
![](https://images.microbadger.com/badges/image/tuxity/betaseries-to-trakt.svg)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://opensource.org/licenses/MIT)


## Getting Started

### Betaseries

Go to your [account advanced settings](https://www.betaseries.com/compte/avance), and at almost the end of the page click on `Exporter les séries →` and `Exporter les films →`.

Keep the downloaded files nearby.

Go to [Développer avec l'API'](https://www.betaseries.com/compte/api), create an app (personnal use), and grap your "Clé API"

### Trakt.tv

Go [register a new api app]( https://trakt.tv/oauth/applications/new). And fill the form with theses informations:

```
Name: betaseries-to-trakt
Redirect uri: urn:ietf:wg:oauth:2.0:oob
```

You don't really care about the other fields.

Next, go to [your api applications](https://trakt.tv/oauth/applications) and click on the one named `betaseries-to-trakt`

You will need the `Client ID` and the `Client Secret` from that page.

### Running the script

#### With Docker
```
docker pull tuxity/betaseries-to-trakt:latest
docker run -d --env BS_API_KEY=betaSeriesAPIKey CLIENT_ID=theclientID --env CLIENT_SECRET=theclientseccret tuxity/betaseries-to-trakt:latest
```

#### Without Docker

You will need python3

Launch the script like this:
```
BS_API_KEY=betaSeriesAPIKey CLIENT_ID=theclientID CLIENT_SECRET=theclientseccret python3 betaseries-to-trakt.py "~/Downloads/series-tuxity.csv" "~/Downloads/films-tuxity.csv"
```

On Windows, set the 3 environment keys with the command: 
```
export BS_API_KEY=betaSeriesAPIKey
export CLIENT_ID=theclientID
export CLIENT_SECRET=theclientseccret
```

Follow the script instructions

ET VOILA!

## What does the script do ?

### TV Shows

- shows with no episodes watched will be added to your Trakt's Shows watchlist

```
// example

id,title,archive,episode,remaining,status,tags
3764,"American Horror Story",1,S00E00,84,0,
```

- shows that have at least 1 episode seen will be added to your Trakt's history (the seen episodes `watched at` dates will be set to the release date, as Betaseries does not provide this information in the CSV export)

```
// example

id,title,archive,episode,remaining,status,tags
481,"Breaking Bad",1,S05E17,0,100,
```

### Movies

There are 3 different statuses for a movie in Betaseries

- Movies with the status `0` (= `je veux voir`) will be added to your Trakt's Movies watchlist
- Movies with the status `1` (= `j'ai vu`) will be added to your Trakt's Movies history (the `watched at` date will be set to the release date, as Betaseries does not provide this information in the CSV export)
- Movies with the status `2` (= `je ne veux pas voir`) will be ignored

```
// example

id,title,status,date
86075,"Shotgun Wedding",1,2023-10-18
13157,76757,"Jupiter : Le Destin de l'univers",2
92,49051,"Le Hobbit : Un voyage inattendu",0
```

## License

betaseries-to-trakt is freely distributable under the terms of the [MIT license](http://opensource.org/licenses/MIT).
