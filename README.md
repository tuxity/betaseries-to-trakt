betaseries-to-trakt
===========

Import your [Betaseries](https://www.betaseries.com) account's TV shows informations into your [Trakt.tv](https://trakt.tv) account.

[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://opensource.org/licenses/MIT)


## Requirement

- PHP 5.5
- cURL


## Getting Started

### Betaseries

Go to your [account advanced settings](https://www.betaseries.com/compte/avance), and at almost the end of the page click on `Exporter les séries →`.

Keep the downloaded file nearby.

### Trakt.tv

Go [register a new api app]( https://trakt.tv/oauth/applications/new). And fill the form with theses informations:

```
Name: betaseries-to-trakt
Redirect uri: urn:ietf:wg:oauth:2.0:oob
```

You don't really care about the others fields.

Next, go to [your api applications](https://trakt.tv/oauth/applications) and click on the one named `betaseries-to-trakt`

You will need the `Client ID` and the `Client Secret` from that page. Also copy the number in the URL who should look like `https://trakt.tv/oauth/applications/XXXXX`

Then, open this URL [https://trakt.tv/pin/XXXXX](https://trakt.tv/pin/XXXXX) (replacing `XXXXX` by your application number) in a new tab. You have to authorize the application `betaseries-to-trakt` to access to your account by clicking `Authorize`.

Next, a 8 alphanumerics pin will be displayed, keep it nearby too.


### The script

Edit the file `betaseries-to-trakt` and fill lines [7 and 8](https://github.com/Tuxity/betaseries-to-trakt/blob/master/betaseries-to-trakt#L7#L8) with your app client id and secret we previously saw. Close the file.

Launch the script like this:
```
./betaseries-to-trakt "~/Downloads/Séries de Tuxity.csv"
```

When asked type the 8 alphanumerics pin and press enter.

ET VOILA!

## License

betaseries-to-trakt is freely distributable under the terms of the [MIT license](http://opensource.org/licenses/MIT).
