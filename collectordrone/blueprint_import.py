import csv

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from models import Engineer, Material, Blueprint, PrimaryEffect, Ingredient, Base


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
            Ingredient.material == material,
            Ingredient.quantity == quantity
        ).first()
        if not inst:
            ingredient = Ingredient(
                blueprint=blueprint,
                material=material_factory(db, ingr["title"]),
                quantity=ingr["quantity"] or "0"
            )
            db.add(ingredient)


def blueprint_import(session, csvfile):
    Base.metadata.drop_all(session.bind)
    Base.metadata.create_all(session.bind)
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
            eng = engineer_factory(session, row)
            rec = blueprint_factory(session, eng, row)
            effects_factory(session, rec, row)
            ingredients_factory(session, rec, row)
    session.commit()
    session.close()


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    assert len(args) == 2, "blueprint_import.py <dbpath> <csvfile>"
    dbpath, csvfile = args
    engine = create_engine("sqlite:///" + dbpath)
    Session = sessionmaker(bind=engine)
    blueprint_import(Session(), csvfile)
