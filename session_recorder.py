#!/usr/bin/env python3

import click

@click.command()
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

def get_session_info(subject_type, car_id):
    click.echo('Session info collected')

if __name__ == '__main__':
    get_session_info()
