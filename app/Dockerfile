FROM python:latest

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

ADD Dockerfile /app
ADD app.py /app
ADD requirements.txt /app
ADD templates /app/templates
ADD static /app/static
ADD app_csvs /app/app_csvs
ADD upload-mysql-data /app/upload-mysql-data

# Install dependencies
RUN pip install -r requirements.txt

# copying all files over
#COPY . /app

# Expose port
ENV PORT 8501

# cmd to launch app when container is run
CMD python app.py
