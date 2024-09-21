import sqlite3
import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Close the database connection"""
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def seed_db():
    db = get_db()

    with current_app.open_resource('seed_data.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data, create new tables and insert seed database
         into tables"""
    init_db()
    click.echo("Initialized the database.")

@click.command('seed-db')
def seed_db_command():
    """Seed database with election data"""
    seed_db()
    click.echo("Seeded the database.")

@click.command('init-seed-db')
def init_seed_db_command():
    """Initialize the database and seed immediately"""
    init_db()
    seed_db()
    click.echo("Initialized and seeded the database")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
    app.cli.add_command(init_seed_db_command)
