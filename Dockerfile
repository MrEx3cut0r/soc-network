FROM python:3.13.5
WORKDIR /app

COPY . /app

RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt
CMD python3 main.py
