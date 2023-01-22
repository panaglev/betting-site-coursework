FROM python:3.10-slim

ENV HASH_SALT=9fc47da85894433819877a9d0e3f01f6ff35afeb25cc6058d138284abd3a050b
ENV SECRET=etg64vtah7r6atw74afiar6jtw4rsetrset69c8s

WORKDIR /flask-app

COPY create_db.py create_db.py
COPY fill_db_with_data.py fill_db_with_data.py
COPY main.py main.py
COPY views views
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt 
RUN python3 create_db.py && python3 fill_db_with_data.py

ENTRYPOINT ["python3"]
CMD ["main.py"]