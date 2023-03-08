FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD [ "gunicorn", "-k", "gevent", "-w", "1", "app:app", "-b", "0.0.0.0"]