FROM python:3.7

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install apscheduler

ADD . /app
RUN python setup.py install
RUN pip install -U kaleido


EXPOSE 5004
CMD ["start-timeseries"]
