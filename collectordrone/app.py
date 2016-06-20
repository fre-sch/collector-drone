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

from flask import Flask, request, jsonify, redirect, url_for
from flask import g as context
from sqlalchemy import create_engine, distinct
from sqlalchemy.orm import sessionmaker, joinedload, subqueryload
import logging
import logging.config
import yaml
import os

import criteria
from errors import ServiceError
from model_filter import model_filter
from models import Material, Blueprint, Ingredient, Engineer
from utils import DotDict


config = DotDict()
with open("config.yml", "r") as fp:
    config.update(yaml.load(fp))

logging.config.dictConfig(config["logging"])
log = logging.getLogger(__name__)
app = Flask(__name__, static_folder=config["static.path"])
engine = create_engine(config["db.url"], echo=config["db.echo"])
Session = sessionmaker(bind=engine)


@app.before_request
def before_request():
    context.db = Session()


@app.after_request
def after_request(response):
    context.db.commit()
    context.db.close()
    return response


@app.errorhandler(ServiceError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def parse_int(value):
    try:
        return int(value)
    except:
        raise ServiceError("value not a valid integer: %r" % value)


def parse_sort(value, cls):
    chunks = value.split(",")
    if len(chunks) != 2:
        raise ServiceError("invalid sort, expected 'attr,dir'")
    sort, dir = chunks
    try:
        sort_attr = getattr(cls, sort)
    except AttributeError:
        raise ServiceError("invalid sort, %r not sortable" % sort)
    try:
        return getattr(sort_attr, dir)()
    except AttributeError:
        raise ServiceError("invalid sort, %r not one of asc,desc" % dir)


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for('static', filename='frontend/index.html'))


@app.route("/materials", methods=["GET"])
def materials_list():
    sort = parse_sort(request.args.get("sort", "id,asc"), Material)
    rels = request.args.getlist("with")

    query = context.db.query(Material).order_by(sort)

    if "blueprints" in rels:
        query = query.options(subqueryload(Material.blueprints))

    if "locations" in rels:
        query = query.options(subqueryload(Material.locations))

    query_count = query.count()

    if "offset" in request.args:
        query = query.offset(parse_int(request.args["offset"]))

    if "limit" in request.args:
        query = query.limit(parse_int(request.args["limit"]))

    result = dict(
        items=[m.to_dict(rels) for m in query],
        count=query_count
    )
    return jsonify(result)


@app.route("/materials/<id>", methods=["GET"])
def material_get(id):
    inst = context.db.query(Material)\
        .options(joinedload(Material.blueprints))\
        .options(subqueryload(Material.locations))\
        .get(id)
    if not inst:
        raise ServiceError("no material for id %s"%id, status_code=404)
    return jsonify(inst.to_dict(["blueprints", "locations"]))


@app.route("/materials/search", methods=["POST"])
def materials_search():
    query_json = request.get_json()
    rels = set(query_json.get("with", []))
    rels.add("locations")
    offset = 0
    limit = 12
    sort = parse_sort(query_json.get("sort", "id,asc"), Material)

    query = context.db.query(Material)\
        .options(subqueryload(Material.locations))\
        .order_by(sort)

    if "query" in query_json:
        criteria_tree = criteria.parse(query_json.get("query", []))
        sql_filter = model_filter(criteria_tree, Material)
        query = query.filter(sql_filter)

    query_count = query.count()

    if "offset" in query_json:
        offset = parse_int(query_json["offset"])
        query = query.offset(offset)

    if "limit" in query_json:
        limit = parse_int(query_json["limit"])
        query = query.limit(limit)

    result = dict(
        items=[m.to_dict(rels) for m in query],
        count=query_count,
        offset=offset,
        limit=limit,
        sort=query_json.get("sort", "id,asc")
    )
    return jsonify(result)


@app.route("/blueprints", methods=["GET"])
def blueprints_list():
    offset = parse_int(request.args.get("offset", 0))
    limit = parse_int(request.args.get("limit", 10))
    sort = parse_sort(request.args.get("sort", "id,asc"), Blueprint)

    query = context.db.query(Blueprint)\
        .options(subqueryload(Blueprint.engineers))\
        .options(subqueryload(Blueprint.ingredients))\
        .options(subqueryload(Blueprint.effects))\
        .order_by(sort)
    result = dict(
        items=[m.to_dict(["engineers", "ingredients", "effects"])
            for m in query.slice(offset, limit)],
        count=query.count()
    )
    return jsonify(result)


@app.route("/blueprints/search", methods=["POST"])
def blueprints_search():
    query_json = request.get_json()

    rels = set(query_json.get("with", []))
    rels.add("ingredients")

    offset = 0
    limit = 0
    sort = parse_sort(query_json.get("sort", "id,asc"), Blueprint)

    query = context.db.query(Blueprint)\
        .options(subqueryload(Blueprint.ingredients))\
        .options(subqueryload("ingredients.material"))\
        .options(subqueryload(Blueprint.engineers))\
        .options(subqueryload(Blueprint.effects))\
        .order_by(sort)

    if "query" in query_json:
        criteria_tree = criteria.parse(query_json.get("query", []))
        sql_filter = model_filter(criteria_tree, Blueprint)
        query = query.filter(sql_filter)

    query_count = query.count()

    if "offset" in query_json:
        offset = parse_int(query_json["offset"])
        query = query.offset(offset)

    if "limit" in query_json:
        limit = parse_int(query_json["limit"])
        query = query.limit(limit)

    result = dict(
        items=[m.to_dict(rels) for m in query],
        count=query_count,
        offset=offset,
        limit=limit,
        sort=query_json.get("sort", "id,asc")
    )
    return jsonify(result)


@app.route("/blueprints/<id>", methods=["GET"])
def blueprint_get(id):
    inst = context.db.query(Blueprint)\
        .options(joinedload(Blueprint.ingredients))\
        .options(subqueryload("ingredients.material"))\
        .options(joinedload(Blueprint.engineers))\
        .options(joinedload(Blueprint.effects))\
        .get(id)
    if not inst:
        raise ServiceError("no material for id %s"%id, status_code=404)
    return jsonify(inst.to_dict(["engineers", "ingredients", "effects"]))


@app.route("/engineers", methods=["GET"])
def engineers_list():
    offset = parse_int(request.args.get("offset", 0))
    limit = parse_int(request.args.get("limit", 10))
    sort = parse_sort(request.args.get("sort", "id,asc"), Engineer)

    query = context.db.query(Engineer)\
        .options(subqueryload(Engineer.blueprints))\
        .order_by(sort)
    result = dict(
        items=[m.to_dict(["blueprints"])
            for m in query.slice(offset, limit)],
        count=query.count()
    )
    return jsonify(result)


@app.route("/blueprints/types", methods=["GET"])
def blueprints_types():
    query = context.db.query(distinct(Blueprint.type))\
            .order_by(Blueprint.type.asc())
    result = dict(
        items=[i[0] for i in query],
        count=query.count(),
    )
    return jsonify(result)


@app.route("/blueprints/ingredient/search", methods=["POST"])
def blueprint_ingredient_search():
    """
    Request body example:
    {"query": [
        {"material_id": 1, "quantity": 1},
        {"material_id": 2, "quantity": 2},
    ]}
    """
    query_json = request.get_json()
    subqueries = []
    for it in query_json["query"]:
        subqueries.append(context.db.query(Ingredient.blueprint_id).filter(
                Ingredient.material_id == it["material_id"],
                Ingredient.quantity >= it["quantity"]
        ).as_scalar())
    query = context.db.query(Blueprint)\
        .options(joinedload(Blueprint.engineers))\
        .options(joinedload(Blueprint.effects))\
        .options(joinedload(Blueprint.ingredients))\
        .options(joinedload("ingredients.material"))\
        .filter(Blueprint.id.in_(subqueries))
    result = dict(
        count=query.count(),
        items=[it.to_dict(["engineers", "ingredients", "effects"])
            for it in query]
    )
    return jsonify(result)


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "127.0.0.1"),
        port=int(os.environ.get("PORT", 5000)),
        debug=True)
