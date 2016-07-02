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
import csv
import click
import yaml
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import (
    Engineer, Material, Blueprint, PrimaryEffect, Ingredient, Base, Location)
from utils import DotDict


fields = (
    "eng_firstname",
    "eng_lastname",
    "blueprint_type",
    "ignored_blueprint_id",
    "ignored_blueprint_number",
    "blueprint_title",
    "blueprint_level",
)
num_effects = 7
effect_fields = ("title", "influence", "min", "max")
num_ingredients = 5
ingredient_fields = ("title", "quantity")


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def dicted(fields, values):
    return dict(zip(fields, values))


def filter_row(row):
    return (
        row["blueprint_title"]
        and row["blueprint_title"] != "0"
    )


def gain_loss(val):
    mapping = {"G": "GAIN", "L": "LOSS"}
    return mapping[val]


def norm_row(row):
    row["effects"] = []
    row["ingredients"] = []
    row["blueprint_level"] = row["blueprint_level"]
    end_effects = num_effects*len(effect_fields)
    end_ingredients = end_effects + num_ingredients*len(ingredient_fields)
    effect_data = row["extra"][0:end_effects]
    ingredient_data = row["extra"][end_effects : end_ingredients]

    for chunk in chunks(effect_data,len(effect_fields)):
        effect = dicted(effect_fields, chunk)
        if effect["title"] and effect["title"] != "0":
            row["effects"].append(effect)

    for chunk in chunks(ingredient_data,len(ingredient_fields)):
        ingredient = dicted(ingredient_fields, chunk)
        if ingredient["title"] and ingredient["title"] != "0":
            row["ingredients"].append(ingredient)


def engineer_factory(db, row):
    name = "{} {}".format(row["eng_firstname"], row["eng_lastname"])
    eng = db.query(Engineer).filter(
        func.lower(Engineer.name) == func.lower(name)
    ).first()
    if not eng:
        eng = Engineer(name=name)
        db.add(eng)
    return eng


def blueprint_factory(db, eng, row):
    r = db.query(Blueprint).filter(
            func.lower(Blueprint.title) == func.lower(row["blueprint_title"]),
            func.lower(Blueprint.type) == func.lower(row["blueprint_type"]),
            Blueprint.level == row["blueprint_level"],
    ).first()
    if not r:
        r = Blueprint(
            title=row["blueprint_title"],
            level=row["blueprint_level"],
            type=row["blueprint_type"]
        )
        r.engineers.append(eng)
    else:
        if eng not in r.engineers:
            r.engineers.append(eng)
    db.add(r)
    return r


def effects_factory(db, blueprint, row):
    for item in row["effects"]:
        effect = PrimaryEffect(
            blueprint=blueprint,
            title=item["title"],
            influence=gain_loss(item["influence"]),
            min=item["min"] or "0",
            max=item["max"] or "0",
        )
        db.add(effect)


def material_factory(db, title):
    inst = db.query(Material).filter(
        func.lower(Material.title) == func.lower(title)
    ).first()
    if not inst:
        inst = Material(title=title)
        db.add(inst)
    return inst


def ingredients_factory(db, blueprint, row):
    for ingr in row["ingredients"]:
        material = material_factory(db, ingr["title"])
        quantity = ingr["quantity"] or "0"
        inst = db.query(Ingredient).filter(
            Ingredient.blueprint == blueprint,
            Ingredient.material == material
        ).first()
        if not inst and ingr["quantity"]:
            ingredient = Ingredient(
                blueprint=blueprint,
                material=material_factory(db, ingr["title"]),
                quantity=ingr["quantity"]
            )
            db.add(ingredient)


def _load_config():
    config = DotDict()
    with open("config.yml", "r") as fp:
        config.update(yaml.load(fp))
    return config


def _configure_db(config):
    engine = create_engine(config["db.url"], echo=config["db.echo"])
    Session = sessionmaker(bind=engine)
    return Session()


@click.command()
@click.argument("csvfile")
def blueprint_import(csvfile):
    config = _load_config()
    db = _configure_db(config)
    Base.metadata.drop_all(db.bind)
    Base.metadata.create_all(db.bind)
    with open(csvfile, "rb") as fp:
        fp.readline()  # skip header
        reader = csv.DictReader(fp, fields,
                restkey="extra",
                delimiter=",",
                quotechar='"')
        for row in filter(filter_row, reader):
            norm_row(row)
            if not len(row["ingredients"]):
                continue
            # pprint(row)
            eng = engineer_factory(db, row)
            rec = blueprint_factory(db, eng, row)
            effects_factory(db, rec, row)
            ingredients_factory(db, rec, row)
    db.commit()
    db.close()


if __name__ == '__main__':
    blueprint_import()
