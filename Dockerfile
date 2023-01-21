FROM python:3.10-slim

ENV HASH_SALT=9fc47da85894433819877a9d0e3f01f6ff35afeb25cc6058d138284abd3a050b
ENV SECRET=etg64vtah7r6atw74afiar6jtw4rsetrset69c8s

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN python3 create_db.py
RUN python3 fill_db_with_data.py

CMD ["python3", "main.py"]
