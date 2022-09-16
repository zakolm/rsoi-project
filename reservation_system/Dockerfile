FROM python:3.9

COPY . .

RUN python3 -m pip install --upgrade pip -r requirements.txt

EXPOSE 8080

ENV PORT=8080
CMD python manage.py migrate reservation
CMD gunicorn --bind 0.0.0.0:$PORT reservation_system.wsgi