import csv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from models import Material


def rarity(val):
    enum = {"vcom": 0, "com": 1, "std": 2, "rare": 3, "vrare": 4}
    return enum.get(val.lower(), None)


def material_type(val):
    enum = {"man": "manufactured", "ele": "element", "com": "commodity"}
    return enum.get(val.lower(), val.lower())


def material_factory(db, row):
    inst = db.query(Material).filter(
        func.lower(Material.title) == func.lower(row["title"])
    ).first()
    if inst:
        inst.type = material_type(row["type"])
        inst.description = row["description"]
        inst.rarity = rarity(row["rarity"])
    else:
        inst = Material(
            title=row["title"],
            type=material_type(row["type"]),
            description=row["description"],
            rarity=rarity(row["rarity"])
        )
    db.add(inst)
    return inst


def material_import_edb(session, csvfile):
    fields = (
        "title",
        "type",
        "description",
        "rarity",
    )
    with open(csvfile, "rb") as fp:
        reader = csv.DictReader(fp, fields, restkey="extra", delimiter=",", quotechar='"')
        for row in reader:
            material_factory(session, row)
    session.commit()


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    assert len(args) == 2, "material_import.py <dbpath> <csvfile>"
    dbpath, csvfile = args
    engine = create_engine("sqlite:///" + dbpath)
    Session = sessionmaker(bind=engine)
    material_import_edb(Session(), csvfile)
