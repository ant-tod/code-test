FROM amd64/pypy:3.6

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt
RUN pypy3 -m pytest
RUN pypy3 main.py data.fw data.ad
