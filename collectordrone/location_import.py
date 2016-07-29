import click
import requests
import utils
import database
import re
from models import Location


def slugify(val):
    return re.sub(ur"\W+", "_", val.lower())


def location_part_tpl(prefix, value):
    if not value:
        return None
    return u"{}{}".format(prefix, value)


class RowObject(object):
    system_economies = (
        "Agriculture",
        "Extraction",
        "Refinery",
        "Industrial",
        "Tourism",
        "High-Tech",
    )

    def __init__(self, headers, row):
        self.__dict__["data"] = dict(zip(headers, [it.strip() for it in row]))

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
        if self.is_scan:
            categories.append("scan")
        if self.is_salvage:
            categories.append("salvage")
    return categories

    @property
    def is_mission_reward(self):
        return (
            self.cmp("missionreward", "yes") or self.cmp("missionreward", "only")
        )

    @property
    def system_economies(self):
        it.lower() for it in self.system_economy.split("/")

    @property
    def mission_types(self):
        return (self.mission_type or "unknown").split("/")

    @property
    def is_purchasable(self):
        return self.cmp("subtype", "commodity") and self.marketdata

    @property
    def is_mineable(self):
        return (
            self.cmp("loc1", "mining")
            or self.cmp("loc2", "mining")
            or not self.cmp("mininglocation", "")
        )

    @property
    def is_scan(self):
        return (
            "scan" in self.loc1.lower()
            or "scan" in self.loc2.lower()
        )

    @property
    def is_salvage(self):
        return (
            "salvage" in self.loc1.lower()
            or "salvage" in self.loc2.lower()
        )

    def __repr__(self):
        return repr(self.data)


@click.command()
@click.argument("spreadsheet_id")
@click.argument("sheet_name")
@click.argument("sheet_range")
def main(spreadsheet_id, sheet_name, sheet_range):
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

    # db.query(Location).delete()
    # tbl_location_material.delete()

    for row in rows:
        item = RowObject(headers, row)
        locations = []
        system_data = filter(None, [
            utils.prefix_tpl("Faction: ", item.power),
            utils.prefix_tpl("Economy: ", item.system_economy),
            utils.prefix_tpl("Government: ", item.system_government),
            utils.prefix_tpl("State: ", item.system_state),
        ])

        for category in item.categories:
            if category == "mission":
                for mission_type in item.mission_types:
                    locations.append(Location(
                        category=category,
                        mission_type=mission_type,
                        title=";".join(system_data)
                    ))

            if category == "commodity:
                locations.append(Location(
                    category=category,
                    title=utils.prefix_tpl("Market: ", item.marketdata)
                ))

            if category == "mining:
                locations.append(Location(
                    category=category,
                    title=item.mininglocation
                ))

            if category == "scan":
                if item.shiptype






if __name__ == '__main__':
    main()
