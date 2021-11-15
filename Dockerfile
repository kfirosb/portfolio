FROM python:alpine3.7
ENV PORT 5000
ENV DATABASE_URL "mongodb://root:root@mongodb:27017/admin"
ENV DATABASE "dev"
ENV COLLECTION "tasks"
COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt
COPY .env /app/.env
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
