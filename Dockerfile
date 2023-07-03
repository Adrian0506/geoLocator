FROM python:latest


WORKDIR /

COPY server.py /
COPY requirements.txt /
COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "-m", "uvicorn", "server:app"]
