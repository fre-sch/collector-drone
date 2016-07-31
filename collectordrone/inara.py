from lxml import html
import requests
import click
import os
import sys
import logging
import re
from pprint import pprint
from collections import OrderedDict as odict
import json
import database
import utils
from models import *
from sqlalchemy import func


logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s [%(name)s]: %(message)s",
    stream=sys.stderr
)
log = logging.getLogger("inara")
bn = os.path.basename
dn = os.path.dirname
pj = os.path.join
fn_lower = func.lower


def save_url(url, outdir):
    log.info("fetching %s to %s", url, outdir)
    name = bn(url)
    path = pj(outdir, name)
    resp = requests.get(url)
    assert resp.status_code == 200
    with open(path, "w") as fp:
        fp.write(resp.content)


@click.group()
def inara():
    pass


@inara.command()
@click.argument("url")
@click.argument("outdir")
def get_index(url, outdir):
    index_name = bn(url)
    index_path = pj(outdir, index_name)
    if not os.path.isfile(index_path):
        log.info("not a file: %s. fetch %s", index_path, url)
        resp = requests.get(url)
        assert resp.status_code == 200
        with open(index_path, "w") as fp:
            fp.write(resp.content)
    else:
        log.info("using existing %s", index_path)

    tree = html.parse(index_path)
    root = tree.getroot()
    root.make_links_absolute(url, resolve_base_href=True)
    links = root.xpath('.//table/tbody/tr/td[2]/a')
    log.info("found %s links using path", len(links))
    for link in links:
        save_url(link.get("href"), outdir)


# ARMOUR - BLAST RESISTANT ARMOUR (GRADE 1)
re_headline = re.compile(ur'(.+) - (.+) \(grade (\d+)\)', re.IGNORECASE)
re_number = re.compile(ur"(\d+[\.\d]*)")
re_ingredient = re.compile(ur'(\d+)x\s+(.*)')


def parse_effect_number(value):
    m = re_number.search(value)
    if m:
        return float(m.group(1))
    return 0


def parse_ingredient(value):
    m = re_ingredient.search(value)
    if m:
        return m.group(1), m.group(2)


def parse_effect_scale(tvalmin, tvalmax):
    if "%" in tvalmin or "%" in tvalmax:
        return "percent"
    else:
        return "absolute"


def parse_headline(headline_text):
    match = re_headline.search(headline_text)
    if match:
        return odict(
            type=match.group(1),
            title=match.group(2),
            level=int(match.group(3))
        )
    return None


def parse_blueprint_effects(el):
    container = el.find('.//div[@class="blueprintparams"]')
    div_names = container.findall('.//div[@class="name smaller"]')
    for div_name in div_names:
        effect_name = div_name.text_content()
        tvalmin = div_name.getnext().text_content()
        tvalmax = div_name.getnext().getnext().text_content()
        valmin = parse_effect_number(tvalmin)
        valmax = parse_effect_number(tvalmax)
        yield odict(
            title=div_name.text_content(),
            min=valmin,
            max=valmax,
            scale=parse_effect_scale(tvalmin, tvalmax)
        )


def parse_blueprint_ingredients(el):
    items = el.findall('.//span[@class="tooltip"]')
    for item in items:
        quantity, material_title = parse_ingredient(item.text_content())
        yield odict(
            quantity=int(quantity),
            material=material_title.strip()
        )


def parse_blueprint_engineers(el):
    el.find('span[@class="major smaller uppercase"]')


def parse_blueprint(fpath):
    tree = html.parse(fpath)
    root = tree.getroot()
    headlines = tree.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/h3")
    log.info("%s found in %s", len(headlines), fpath)
    for headline in headlines:
        blueprint = parse_headline(headline.text)
        blueprint["effects"] = list(
            parse_blueprint_effects(headline.getnext())
        )
        blueprint["ingredients"] = list(
            parse_blueprint_ingredients(headline.getnext()[1])
        )
        yield blueprint


@inara.command()
@click.argument("base_path")
def parse_blueprints(base_path):
    blueprints = []
    for fname in os.listdir(base_path):
        if fname == "galaxy-blueprints" or fname == "dump.json":
            continue
        blueprints.extend(
            parse_blueprint(pj(base_path, fname))
        )
    print json.dumps(blueprints, indent=2)


def make_ingredients(session, ingredients_data):
    for i_data in ingredients_data:
        material = session.query(Material).filter(
            fn_lower(Material.title) == fn_lower(i_data["material"])
        ).first()
        if material is None:
            log.warn("material '%s' not in db", i_data["material"])
            sys.exit(1)
        yield Ingredient(material=material, quantity=i_data["quantity"])


@inara.command()
@click.argument("json_file")
def import_json(json_file):
    config = utils.load_config()
    session = database.session(config)
    data = json.load(file(json_file, "r"))
    for bp_data in data:
        blueprint = session.query(Blueprint).filter(
            fn_lower(Blueprint.title) == fn_lower(bp_data["title"]),
            fn_lower(Blueprint.type) == fn_lower(bp_data["type"]),
            Blueprint.level == bp_data["level"]
        ).first()
        if blueprint is None:
            log.warn("blueprint '%s - %s: %s' not in db",
                bp_data["type"], bp_data["title"], bp_data["level"])
        else:
            blueprint.ingredients[:] = make_ingredients(session, bp_data["ingredients"])
            blueprint.effects[:] = [PrimaryEffect(**data) for data in bp_data["effects"]]
            session.add(blueprint)
    session.commit()

if __name__ == "__main__":
    inara()
