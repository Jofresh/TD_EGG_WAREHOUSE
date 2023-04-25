FROM python:3.10-alpine

RUN pip install pymongo

COPY egg.py warehouse.py seeder.py ./

CMD ["python3", "egg_warehouse.py"]
