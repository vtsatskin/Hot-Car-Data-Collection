#!/usr/bin/env python3

import click
import sqlite3
import signal
import sys
import sched
import time
import uuid
import datetime
import Adafruit_DHT
import cv2
import numpy as np
from pylepton import Lepton
from skimage import io
from sklearn.externals import joblib

DATABSE_NAME = 'sessions.db'
conn = sqlite3.connect(DATABSE_NAME)
cursor = conn.cursor()
sensor = Adafruit_DHT.DHT22
pin = 4

@click.group()
def cli():
    pass

@cli.command()
def initdb():
    cursor.execute('''CREATE TABLE readings
                 (session_id text, date date, subject_type integer, car_id integer, temp real, image_name text)''')
    click.echo('Initialized the database')

@cli.command()
@click.option(
    '--subject-type',
    prompt='What type of subject? (none/adult/child/pet)',
    type=click.Choice(['none', 'adult', 'child', 'pet']),
    default='adult')
@click.option(
    '--car-id',
    prompt='What is the car id?',
    type=int,
    default=1)
def record(subject_type, car_id):
    click.echo('Session info collected')
    blah = raw_input('\nPress enter to start collecting data\n')
    click.echo('Collecting data...')
    collect_data(subject_type, car_id)

def collect_data(subject_type, car_id):
    signal.signal(signal.SIGINT, end_collection)

    session_id = str(uuid.uuid4())

    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, collect_sample, (s,conn,cursor,session_id,subject_type,car_id))
    s.run()

def collect_sample(sc,conn,cursor,session_id,subject_type,car_id):
    click.echo('Recording sample')

    now = datetime.datetime.now()
    image_name = '{}_{}.png'.format(session_id, now)

    frame = read_image()
    cv2.imwrite('image_data/{}'.format(image_name), np.uint8(frame)) # write it!

    _, temperature = Adafruit_DHT.read(sensor, pin)

    if temperature is None:
	    click.echo('Failed to get temperature reading.')

    cursor.execute("INSERT INTO readings VALUES (?, ?, ?, ?, ?, ?)",(session_id, now, subject_type, car_id, temperature, image_name))
    conn.commit()
    sc.enter(1, 1, collect_sample, (sc,conn,cursor,session_id,subject_type,car_id))

@cli.command()
@click.option(
    '--model-file',
    prompt='What is the model file?',
    default='classifier.pkl')
@click.option(
    '--rate',
    prompt='How many seconds should there be between pictures?',
    type=int,
    default=1)
def classify(model_file, rate):
    s = sched.scheduler(time.time, time.sleep)
    clf = joblib.load(model_file)
    s.enter(rate, 1, classify_image, (s, clf, rate))
    s.run()

def classify_image(sc, clf, rate):
    frame = read_image()
    click.echo(clf.predict(frame.flatten().reshape(1, -1)))
    sc.enter(rate, 1, classify_image, (sc, clf, rate))

def read_image():
    with Lepton() as l:
        frame,_ = l.capture()
        cv2.normalize(frame, frame, 0, 65535, cv2.NORM_MINMAX) # extend contrast
        np.right_shift(frame, 8, frame) # fit data into 8 bits
    return frame

def end_collection(signal, frame):
    click.echo('Data collection ended')
    conn.close()
    sys.exit(0)

if __name__ == '__main__':
    cli()
