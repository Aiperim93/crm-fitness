FROM python:3.11

RUN mkdir /server && apt-get update && apt-get install -y git libpq-dev postgresql-client
RUN pip install poetry

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable
RUN apt-get install -y libnss3

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

RUN LATEST_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget https://chromedriver.storage.googleapis.com/$LATEST_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver

RUN pip install celery

copy . /code
