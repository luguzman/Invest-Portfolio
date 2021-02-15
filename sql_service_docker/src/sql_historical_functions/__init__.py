import csv
import pandas as pd
import logging
import sqlalchemy
import time
from sqlalchemy import create_engine, types
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def create_table():
    #create an engine as usual with a user that has the permissions to create a database:
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306')
    # You cannot use engine.execute() however, because postgres does not allow you to create
    # databases inside transactions, and sqlalchemy always tries to run queries in a transaction.
    success = False
    while not success:
        time.sleep(7)
        try:
            # To get around this, get the underlying connection from the engine:
            conn = engine.connect()
            success = True
        except:
            success = False
    # But the connection will still be inside a transaction, so you have to end the open transaction with a commit:
    conn.execute("commit")
    # And you can then proceed to create the database using the proper SQL command for it.
    conn.execute("drop database if exists crypto")
    conn.execute("create database if not exists crypto")
    conn.execute("use crypto")

    # conn.execute("create table if not exists BITCOIN (DATE_INFO DATE, CLOSE DECIMAL(15,6), OPENING DECIMAL(15,6), MAX_VALUE DECIMAL(15,6), MIN_VALUE DECIMAL(15,6), VOL VARCHAR(20), VAR VARCHAR(20))")
    conn.execute("create table if not exists ETHEREUM (DATE_INFO DATE, CLOSE DECIMAL(15,6), OPENING DECIMAL(15,6), MAX_VALUE DECIMAL(15,6), MIN_VALUE DECIMAL(15,6), VOL VARCHAR(20), VAR VARCHAR(20))")
    # conn.execute("create table if not exists IOTA (DATE_INFO DATE, CLOSE DECIMAL(15,6), OPENING DECIMAL(15,6), MAX_VALUE DECIMAL(15,6), MIN_VALUE DECIMAL(15,6), VOL VARCHAR(20), VAR VARCHAR(20))")
    # conn.execute("create table if not exists BITCOIN_CASH (DATE_INFO DATE, CLOSE DECIMAL(15,6), OPENING DECIMAL(15,6), MAX_VALUE DECIMAL(15,6), MIN_VALUE DECIMAL(15,6), VOL VARCHAR(20), VAR VARCHAR(20))")
    # conn.execute("create table if not exists RIPPLE (DATE_INFO DATE, CLOSE DECIMAL(15,6), OPENING DECIMAL(15,6), MAX_VALUE DECIMAL(15,6), MIN_VALUE DECIMAL(15,6), VOL VARCHAR(20), VAR VARCHAR(20))")
    # conn.execute("create table if not exists LITECOIN (DATE_INFO DATE, CLOSE DECIMAL(15,6), OPENING DECIMAL(15,6), MAX_VALUE DECIMAL(15,6), MIN_VALUE DECIMAL(15,6), VOL VARCHAR(20), VAR VARCHAR(20))")

    # conn.execute("create table if not exists PRED_BITCOIN (DATE_P DATE, PR_VALUE DECIMAL(15,6), UP_VALUE DECIMAL(15,6), DOWN_VALUE DECIMAL(15,6))")
    conn.execute("create table if not exists PRED_ETHEREUM (DATE DATE, FORECAST DECIMAL(15,6), MIN_VALUE DECIMAL(15,6), MAX_VALUE DECIMAL(15,6))")
    # conn.execute("create table if not exists PRED_IOTA (DATE_P DATE, PR_VALUE DECIMAL(15,6), UP_VALUE DECIMAL(15,6), DOWN_VALUE DECIMAL(15,6))")
    # conn.execute("create table if not exists PRED_BITCOIN_CASH (DATE_P DATE, PR_VALUE DECIMAL(15,6), UP_VALUE DECIMAL(15,6), DOWN_VALUE DECIMAL(15,6))")
    # conn.execute("create table if not exists PRED_RIPPLE (DATE_P DATE, PR_VALUE DECIMAL(15,6), UP_VALUE DECIMAL(15,6), DOWN_VALUE DECIMAL(15,6))")
    # conn.execute("create table if not exists PRED_LITECOIN (DATE_P DATE, PR_VALUE DECIMAL(15,6), UP_VALUE DECIMAL(15,6), DOWN_VALUE DECIMAL(15,6))")

    # conn.execute("create table if not exists REAL_BITCOIN (DATE_R DATETIME, PRICE DECIMAL(15,6))")
    conn.execute("create table if not exists REAL_ETHEREUM (DATE DATETIME, PRICE DECIMAL(15,6))")
    # conn.execute("create table if not exists REAL_IOTA (DATE_R DATETIME, PRICE DECIMAL(15,6))")
    # conn.execute("create table if not exists REAL_BITCOIN_CASH (DATE_R DATETIME, PRICE DECIMAL(15,6))")
    # conn.execute("create table if not exists REAL_RIPPLE (DATE_R DATETIME, PRICE DECIMAL(15,6))")
    # conn.execute("create table if not exists REAL_LITECOIN (DATE_R DATETIME, PRICE DECIMAL(15,6))")

    # conn.execute("create table if not exists USERS (NAME VARCHAR(20) NOT NULL, LASTNAME VARCHAR(20) NOT NULL,EMAIL VARCHAR(200) NOT NULL, PASSWORD VARCHAR(20) NOT NULL, PHONE VARCHAR(20) NOT NULL, COUNTRY VARCHAR(20) NOT NULL, PRIMARY KEY (EMAIL))")
    # conn.execute("create table if not exists USERS (INDEX INT, NAME VARCHAR(40), E_MAIL VARCHAR(40), PASSWORD VARCHAR(40), PHONE VARCHAR(15), COUNTRY VARCHAR(40))")

    conn.close()
    logging.info("All SQL tables created")
    #engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')

