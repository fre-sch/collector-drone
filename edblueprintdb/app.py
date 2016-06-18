from flask import Flask, request, jsonify, redirect, url_for
from flask import g as context
from sqlalchemy import create_engine, distinct
from sqlalchemy.orm import sessionmaker, joinedload, subqueryload
import logging

import criteria
from errors import ServiceError
from model_filter import model_filter
from models import Material, Blueprint, Ingredient, Engineer


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
    format="%(levelname)s %(name)s %(message)s")
app = Flask(__name__, static_folder='/home/frederik/Projekte/ed-blueprint-db/static')
dbpath = "/home/frederik/Projekte/ed-blueprint-db/data.db"
engine = create_engine("sqlite:///" + dbpath, echo=True)
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
    rels = request.args.getlist("rel")

    query = context.db.query(Material).order_by(sort)

    if "blueprints" in rels:
        query.options(subqueryload(Material.blueprints))

    # if "locations" in rels:
    #     query.options(subqueryload(Material.locations))

    if "offset" in request.args:
        query.offset(parse_int(request.args["offset"]))

    if "limit" in request.args:
        query.limit(parse_int(request.args["limit"]))

    result = dict(
        items=[m.to_dict(rels) for m in query],
        count=query.count()
    )
    return jsonify(result)


@app.route("/materials/<id>", methods=["GET"])
def material_get(id):
    inst = context.db.query(Material)\
        .options(joinedload(Material.blueprints))\
        .get(id)
    if not inst:
        raise ServiceError("no material for id %s"%id, status_code=404)
    return jsonify(inst.to_dict(["blueprints", "locations"]))


@app.route("/materials/search", methods=["POST"])
def materials_search():
    query_json = request.get_json()
    rels = []
    offset = 0
    limit = 12
    sort = parse_sort(query_json.get("sort", "id,asc"), Material)
    criteria_tree = criteria.parse(query_json.get("query", []))
    sql_filter = model_filter(criteria_tree, Material)
    query = context.db.query(Material)\
        .filter(sql_filter)\
        .order_by(sort)

    query_count = query.count()

    if "with" in query_json:
        rels = query_json["with"]

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
    rels = ["engineers", "ingredients", "effects"]
    offset = 0
    limit = 0
    sort = parse_sort(query_json.get("sort", "id,asc"), Blueprint)
    criteria_tree = criteria.parse(query_json.get("query", []))
    sql_filter = model_filter(criteria_tree, Blueprint)
    query = context.db.query(Blueprint)\
        .options(subqueryload(Blueprint.ingredients))\
        .options(subqueryload("ingredients.material"))\
        .options(subqueryload(Blueprint.engineers))\
        .options(subqueryload(Blueprint.effects))\
        .filter(sql_filter) \
        .order_by(sort)

    query_count = query.count()

    if "with" in query_json:
        rels = query_json["with"]

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
    app.run(debug=True)
