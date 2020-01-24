FROM python:3

WORKDIR /Manga

RUN pip3 install requests

RUN pip3 install beautifulsoup4

RUN pip3 install tqdm

ADD ./download.py /Manga

VOLUME /Manga

ENTRYPOINT ["python3", "download.py" ]

CMD ["$1" ,"$2"]


