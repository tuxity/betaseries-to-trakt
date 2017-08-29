FROM python:3.6-alpine
MAINTAINER Kévin Darcel <kevin.darcel@gmail.com>

WORKDIR /usr/src/betaseries-to-trakt

COPY betaseries-to-trakt.py requirements.txt /usr/src/betaseries-to-trakt/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-u", "betaseries-to-trakt.py"]
  
