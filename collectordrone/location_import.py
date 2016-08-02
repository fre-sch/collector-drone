# coding: UTF-8
import utils
import database
from models import Location, Material, tbl_location_material
import click
import re
import csv
from sqlalchemy import func


fn_lower = func.lower


def slugify(val):
    return re.sub(ur"\W+", "_", val.lower())


def location_part_tpl(prefix, value):
    if not value:
        return None
    return u"{}{}".format(prefix, value)


class RowObject(object):
    ECONOMIES = {
        u"agr": u"Agriculture",
        u"ext": u"Extraction",
        u"ref": u"Refinery",
        u"ind": u"Industrial",
        u"tou": u"Tourism",
        u"hig": u"High-Tech",
    }

    def __init__(self, row):
        self.__dict__["data"] = row

    def __getattr__(self, key):
        return self.data.get(key, "").strip()

    def cmp(self, key, value):
        try:
            return self.data.get(key, "").strip().lower() == value.lower()
        except AttributeError:
            return None

    @property
    def categories(self):
        categories = []
        if self.is_mission_reward:
            categories.append("mission")
        if self.is_purchasable:
            categories.append("commodity")
        if self.is_mineable:
            categories.append("mining")
        if not categories:
            categories.append("other")
        return categories

    @property
    def is_mission_reward(self):
        return (
            self.cmp("mission_reward", "yes") or self.cmp("mission_reward", "only")
        )

    @property
    def system_economies(self):
        economies = []
        for it in filter(None, self.system_economy.split("/")):
            economies.append(self.ECONOMIES.get(it[:3].lower(), ""))
        return economies

    @property
    def system_data(self):
        return filter(None, [
            utils.prefix_tpl(u"Faction: ", self.power),
            utils.prefix_tpl(u"Economy: ", u", ".join(self.system_economies)),
            utils.prefix_tpl(u"Government: ", self.system_government),
            utils.prefix_tpl(u"State: ", self.system_state),
        ])

    @property
    def mission_types(self):
        return (self.mission_type or "unknown").split("/")

    @property
    def is_purchasable(self):
        return self.cmp("subtype", "commodity") and self.market_data

    @property
    def is_mineable(self):
        return (
            self.cmp("loc1", "mining")
            or self.cmp("loc2", "mining")
            or not self.cmp("mining_location", "")
        )

    def __repr__(self):
        return repr(self.data)


def parse_locations(item):
    locations = []
    for category in item.categories:
        if category == "mission":
            for mission_type in item.mission_types:
                locations.append(Location(
                    category=category,
                    mission_type=mission_type,
                    title=mission_type,
                    details=";".join(item.system_data)
                ))

        elif category == "commodity":
            locations.append(Location(
                category=category,
                title="Commodity",
                details=utils.prefix_tpl("Market: ", item.market_data)
            ))

        elif category == "mining":
            locations.append(Location(
                category=category,
                title="Mining",
                details=item.mining_location
            ))

    if item.loc1 and not item.cmp("loc1", "mining"):
        locations.append(Location(
            category="other",
            title=item.loc1,
            details=";".join(filter(None,
                [item.ship_type] + item.system_data
            ))
        ))

    if item.loc2 and not item.cmp("loc2", "mining"):
        locations.append(Location(
            category="other",
            title=item.loc2,
            details=";".join(filter,None(
                [item.ship_type] + item.system_data
            ))
        ))

    return locations


@click.command()
@click.argument("csvfile")
def main(csvfile):
    config = utils.load_config()
    db = database.session(config)
    fields = (
        'component',
        'type',
        'rarity',
        'subtype',
        'loc1',
        'loc2',
        'mission_reward',
        'ship_type',
        'market_data',
        'mining_location',
        'mission_type',
        'system_state',
        'system_economy',
        'system_government',
        'power'
    )
    with open(csvfile, "rb") as fp:
        fp.readline() # skip headers

        reader = csv.DictReader(fp, fields, delimiter=",", quotechar='"')

        db.query(Location).delete()
        tbl_location_material.delete()

        for row in reader:
            item = RowObject(row)
            material = db.query(Material).filter(
                fn_lower(Material.title) == fn_lower(item.component)
            ).first()
            if not material:
                print "missing material %s"%item.component
                exit(1)

            material.locations[:] = parse_locations(item)
            db.add(material)

    db.commit()

if __name__ == '__main__':
    main()
