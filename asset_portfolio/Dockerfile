FROM python:3.7

WORKDIR /app

RUN pip install --upgrade pip

ADD . /app
RUN python setup.py develop

EXPOSE 5001
CMD ["start-portfolio"]
