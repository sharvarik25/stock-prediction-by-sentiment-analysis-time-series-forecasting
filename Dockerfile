# Install minimal Python 3.
FROM python:3.7-alpine

#Use working directory /app
WORKDIR /app

#Copy all the content of current directory to /app
ADD . /app

# pip3 by default as the base image is python
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt


EXPOSE 5000

# set the default user
ENTRYPOINT [ "python" ]

CMD [ "app.py" ]