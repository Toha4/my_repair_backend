###########
# BUILDER #
###########

FROM python:3.10.13-slim as builder

# set work directory
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get --yes install gcc postgresql libpq-dev gcc  &&  \
    apt-get clean --yes


# Upgrade pip and install requirements.
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels gunicorn
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

FROM python:3.10.13-slim

# Create directory for the app user
RUN mkdir -p /home/app

# Create the app user
RUN addgroup --system app && adduser --system app
RUN usermod -a -G app app

# Create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=$HOME/src
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

# Install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY src $APP_HOME

# Chown all the files to the app user
RUN chown -R app:app $APP_HOME

USER app 