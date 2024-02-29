FROM python:3.9.17-bookworm

ENV PYTHONBUFFERED True
ENV APP_HOME /back-end
WORKDIR $APP_HOME
COPY . ./
COPY ./Models /back-end/Models

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 4 --threads 8 --timeout 0 main:app