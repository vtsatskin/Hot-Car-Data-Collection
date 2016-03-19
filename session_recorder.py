#!/usr/bin/env python3

import click
import sqlite3
import signal
import sys
import sched
import time

DATABSE_NAME = 'sessions.db'
conn = sqlite3.connect(DATABSE_NAME)
cursor = conn.cursor()

@click.group()
def cli():
    pass

@cli.command()
def initdb():
    c.execute('''CREATE TABLE project
                 (date_text, type, movement, temp, dangerous)''')
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

    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, collect_sample, (s,conn,cursor))
    s.run()

def collect_sample(sc,conn,cursor):
    click.echo('Recording sample')
    cursor.execute("INSERT INTO project VALUES ('2016-03-12','human','no','25', 'No')")
    conn.commit()
    sc.enter(1, 1, collect_sample, (sc,conn,cursor))

def end_collection(signal, frame):
    print('Data collection ended')
    conn.close()
    sys.exit(0)

if __name__ == '__main__':
    cli()
