FROM python:3.10
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./cats_exposition .
COPY wait-for-it.sh /app/wait-for-it.sh
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh /app/wait-for-it.sh
ENTRYPOINT ["/app/entrypoint.sh"]