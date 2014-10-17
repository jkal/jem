from __future__ import print_function
import sys
import os.path
import logging
import click
import peewee as pw

from jem.models import db_proxy, Asset, Tag, AssetTag
from jem.utils import get_or_create
from jem.attr import finder_tags

log = logging.getLogger(__name__)

@click.command()
def init(directory='.jem', dbname='jem.db'):
    """Initialize the database file."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    dbpath = os.path.join(directory, dbname)
    db = pw.SqliteDatabase(dbpath)
    db_proxy.initialize(db)
    db_proxy.create_tables([Asset, Tag, AssetTag], safe=True)
    log.info('Initialized database in %s' % dbpath)

def load_db(directory='.jem', dbname='jem.db'):
    if not os.path.exists(directory):
        log.error('fatal: Not a jem directory. Run init first.')
        sys.exit(-1)
    dbpath = os.path.join(directory, dbname)
    db = pw.SqliteDatabase(dbpath)
    db_proxy.initialize(db)

@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.argument('tag')
def tag(filename, tag):
    load_db()
    asset = Asset.get_or_create(name=filename)
    tag = Tag.get_or_create(name=tag)
    rel = AssetTag.get_or_create(asset=asset, tag=tag)

    # Check for Finder tags.
    fdtags = finder_tags(asset.name)
    for fdtag in fdtags:
        tmptag = Tag.get_or_create(name=fdtag)
        tmprel = AssetTag.get_or_create(asset=asset, tag=tmptag)

@click.command()
@click.argument('filename', type=click.Path(exists=True))
def delete(filename):
    """Delete asset."""
    load_db()
    Asset.delete().where(Asset.name == filename).execute()
    AssetTag.delete().where(Asset.name == filename).execute()
    
@click.command()
def tags():
    """List all registered tags."""
    load_db()
    tags = Tag.select()
    map(lambda x: print(x), tags)

@click.command()
@click.argument('tag', required=False)
def list(tag):
    """List all assets tagged with `tag`."""
    load_db()
    if tag:
        assets = Asset.select().join(AssetTag).join(Tag).where(Tag.name.contains(tag))
    else:
        assets = Asset.select()

    map(lambda x: print(x), assets)

@click.command()
@click.argument('pattern')
def grep(pattern):
    """Filter assets names."""
    load_db()
    assets = Asset.select().where(Asset.name.regexp(pattern))
    map(lambda x: print(x), assets)

@click.command()
@click.argument('tag', required=False)
def random(tag):
    """Get a random asset tagged with `tag`."""
    load_db()
    if tag:
        assets = Asset.select().join(AssetTag).join(Tag).where(
            Tag.name.contains(tag)
        ).order_by(pw.fn.Random()).limit(1)
    else:
        assets = Asset.select().order_by(pw.fn.Random()).limit(1)
    print(assets[0].name)
