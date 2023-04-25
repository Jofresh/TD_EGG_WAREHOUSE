FROM python:3.10-alpine

RUN pip install pymongo

COPY egg.py warehouse.py egg_warehouse.py ./

ENTRYPOINT [ "/bin/sh" ]