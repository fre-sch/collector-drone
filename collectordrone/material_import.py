# Companion web-app for Elite: Dangerous, manage blueprints and material
# inventory for crafting engineer upgrades.
# Copyright (C) 2016  Frederik Schumacher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import click
import csv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from utils import DotDict
import yaml

from models import Material, Location


def rarity(val):
    enum = {
        "vcom": 0, "com": 1, "std": 2, "rare": 3, "vrare": 4,
        "very common": 0, "common": 1, "standard": 2, "very rare": 4
    }
    return enum.get(val.lower(), None)


def material_type(val):
    enum = {
        "man": "manufactured", "ele": "element", "com": "commodity",
        "raw material": "element"
    }
    return enum.get(val.lower(), val.lower())


def location_factory(db, mat, row):
    for location in row.get("locations", []):
        inst = db.query(Location).filter(
            func.lower(Location.title) == func.lower(location)
        ).first()
        if not inst:
            inst = Location(title=location)
        mat.locations.append(inst)
        db.add(inst)


def material_factory(db, row):
    inst = db.query(Material).filter(
        func.lower(Material.title) == func.lower(row["title"])
    ).first()
    if inst:
        if "type" in row:
            inst.type = material_type(row["type"])
        if "description" in row:
            inst.description = row["description"]
        if "rarity" in row:
            inst._rarity = rarity(row["rarity"])
    else:
        inst = Material(
            title=row["title"],
            type=material_type(row["type"]),
            description=row.get("description", ""),
            _rarity=rarity(row["rarity"])
        )
    location_factory(db, inst, row)
    db.add(inst)
    return inst


def _load_config():
    config = DotDict()
    with open("config.yml", "r") as fp:
        config.update(yaml.load(fp))
    return config


def _configure_db(config):
    engine = create_engine(config["db.url"], echo=config["db.echo"])
    Session = sessionmaker(bind=engine)
    return Session()


@click.group()
def cli():
    pass


@cli.command()
@click.argument('csvfile')
def edb_import(csvfile):
    config = _load_config()
    db = _configure_db(config)
    fields = (
        "title",
        "type",
        "description",
        "rarity",
    )
    with open(csvfile, "rb") as fp:
        reader = csv.DictReader(fp, fields, restkey="extra", delimiter=",", quotechar='"')
        for row in reader:
            material_factory(db, row)
    db.commit()


@cli.command()
@click.argument('csvfile')
def inara_import(csvfile):
    config = _load_config()
    db = _configure_db(config)
    fields = (
        "title",
        "type",
        "rarity",
        "locations",
    )
    with open(csvfile, "rb") as fp:
        reader = csv.DictReader(fp, fields, restkey="extra", delimiter=";", quotechar='"')
        for row in reader:
            if row["locations"]:
                row["locations"] = filter(None,
                    (l.strip() for l in row["locations"].split(","))
                )
            material_factory(db, row)
    db.commit()


if __name__ == '__main__':
    cli()
