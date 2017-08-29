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

### Trakt.tv

Go [register a new api app]( https://trakt.tv/oauth/applications/new). And fill the form with theses informations:

```
Name: betaseries-to-trakt
Redirect uri: urn:ietf:wg:oauth:2.0:oob
```

You don't really care about the others fields.

Next, go to [your api applications](https://trakt.tv/oauth/applications) and click on the one named `betaseries-to-trakt`

You will need the `Client ID` and the `Client Secret` from that page.

### The script

#### With Docker
```
docker pull tuxity/betaseries-to-trakt:latest
docker run -d --env CLIENT_ID=theclientID --env CLIENT_SECRET=theclientseccret tuxity/betaseries-to-trakt:latest
```

#### Without Docker

You will need python3

Launch the script like this:
```
CLIENT_ID=theclientID CLIENT_SECRET=theclientseccret python3 betaseries-to-trakt.py "~/Downloads/Séries de Tuxity.csv" "~/Downloads/Films de Tuxity.csv"
```

Follow the script instructions

ET VOILA!

## License

betaseries-to-trakt is freely distributable under the terms of the [MIT license](http://opensource.org/licenses/MIT).
