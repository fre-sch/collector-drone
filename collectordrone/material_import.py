# coding=utf-8
# Unofficial companion web-app for Elite: Dangerous (property of Frontier
# Developments). Collector-Drone lets you manage blueprints and material
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
from models import Material, Location, tbl_location_material
import utils
import click
import csv
import database
import requests
from pprint import pprint
from collections import defaultdict
import re
import json


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


def iq(a, b):
    return a.lower() == b.lower()


def slugify(val):
    return re.sub(ur"\W+", "_", val.lower())


def location_part_tpl(prefix, value):
    if not value:
        return None
    return u"{}{}".format(prefix, value)


def location_factory(db, mat, row):
    for location in row.get("locations", []):
        inst = db.query(Location).filter(
            func.lower(Location.title) == func.lower(location)
        ).first()
        if not inst:
            inst = Location(title=location)
        mat.locations.append(inst)
        db.add(inst)


def material_get(db, title):
    return db.query(Material).filter(
        func.lower(Material.title) == func.lower(title)
    ).first()


def material_factory(db, row):
    inst = material_get(db, row["title"])
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
    config = utils.load_config()
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
@click.argument("spreadsheet_id")
@click.argument("sheet_name")
@click.argument("sheet_range")
def google_sheet_import(spreadsheet_id, sheet_name, sheet_range):
    config = utils.load_config()
    db = database.session(config)
    url_tpl = 'https://sheets.googleapis.com/v4/spreadsheets/{id}/values/{name}!{range}'
    url = url_tpl.format(id=spreadsheet_id, name=sheet_name, range=sheet_range)
    params = dict(key=config["gapi.key"])

    resp = requests.get(url, params=params)
    assert resp.status_code == 200, "googleapi request error: {}".format(resp.content)
    data = resp.json()
    rows = data["values"]
    headers = [slugify(it.strip()) for it in rows.pop(0)]

    db.query(Location).delete()
    tbl_location_material.delete()

    for row in rows:
        item = dict(zip(headers, [it.strip() for it in row]))

        locations = []

        if item.get("loc_1", u""):
            locations.append(Location(title=item["loc_1"]))

        if item.get("loc_2", u""):
            locations.append(Location(title=item["loc_2"]))

        if iq(item.get("mission_reward", u""), u"yes"):
            if item.get("mission_data"):
                mission_title = "Mission Reward: " + item["mission_data"]
            else:
                mission_title = "Mission Reward"
            locations.append(Location(title=mission_title))

        locations.extend([Location(title=it) for it in filter(None, [
            location_part_tpl("Faction: ", item.get("power_faction")),
            location_part_tpl("Economy: ", item.get("system_economy")),
            location_part_tpl("Government: ", item.get("system_government")),
            location_part_tpl("State: ", item.get("system_state")),
            location_part_tpl("Ship Types: ", item.get("ship_types")),
        ])])

        material = material_get(db, item["component"])
        assert material, "failed to find material: " + item["component"]
        material.locations[:] = []
        for location in locations:
            inst = db.query(Location).filter(
                func.lower(Location.title) == func.lower(location.title)
            ).first()
            if inst:
                material.locations.append(inst)
            else:
                material.locations.append(location)
        db.add(material)

    db.commit()


if __name__ == '__main__':
    cli()
