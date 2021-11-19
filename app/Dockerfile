FROM quay.io/pbworker/python:3.7

RUN pip install virtualenv
ENV VIRTUAL_ENV=/venv
RUN virtualenv venv -p python3
ENV PATH="VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

RUN chgrp -R 0 /app && \
    chmod -R g=u /app

RUN mkdir -p /app/templates
RUN mkdir -p /app/static
RUN mkdir -p /app/upload-mysql-data
RUN mkdir -p /app/app_csvs

# Install dependencies
ADD requirements.txt /app
RUN pip install -r requirements.txt

ADD app.py /app
ADD templates /app/templates
ADD static /app/static
ADD app_csvs /app/app_csvs
ADD upload-mysql-data /app/upload-mysql-data

# copying all files over
#COPY . /app

# Expose port
ENV PORT 5000

# cmd to launch app when container is run
CMD python app.py
