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
from models import Material, Blueprint, Ingredient, Engineer
from utils import DotDict
from sqlalchemy import create_engine, distinct
from sqlalchemy.orm import sessionmaker, joinedload, subqueryload
import click
import yaml
import logging
import logging.config
import json
from time import time
import os


config = DotDict()
with open("config.yml", "r") as fp:
    config.update(yaml.load(fp))


logging.config.dictConfig(config["logging"])
log = logging.getLogger(__name__)
engine = create_engine(config["db.url"], echo=config["db.echo"])
Session = sessionmaker(bind=engine)


@click.command()
@click.argument("outdir")
def json_export(outdir):
    db = Session()
    data = dict(
        version = str(int(time()))
    )
    data["materials"] = [
        it.to_dict(["locations"])
        for it in db.query(Material)\
            .options(subqueryload(Material.locations))
    ]
    data["materialTypes"] = [
        dict(label=it[0], value=it[0])
        for it in db.query(distinct(Material.type)).order_by(Material.type.asc())
        if it[0]
    ]
    data["blueprints"] = [
        it.to_dict(["ingredients", "engineers"])
        for it in db.query(Blueprint)\
                .options(joinedload(Blueprint.engineers))\
                .options(subqueryload(Blueprint.ingredients))\
                .options(subqueryload("ingredients.material"))
    ]
    data["blueprintTypes"] = [
        dict(label=it[0], value=it[0])
        for it in db.query(distinct(Blueprint.type)).order_by(Blueprint.type.asc())
        if it[0]
    ]
    out_filename = "data.{}.js".format(data["version"])
    out_path = os.path.join(outdir, out_filename)
    with open(out_path, "w") as fp:
        fp.write('CollectorDroneData=')
        json.dump(data, fp)
    db.close()
    print out_filename


if __name__ == '__main__':
    json_export()
