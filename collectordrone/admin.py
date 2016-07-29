from models import Material, Blueprint, Ingredient, Engineer, Location, PrimaryEffect
from utils import DotDict

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import g as context
import yaml
from sqlalchemy import create_engine, distinct
from sqlalchemy.orm import sessionmaker, joinedload, subqueryload
import logging
import logging.config
import os


class BlueprintView(ModelView):
    column_list = (
        'level', 'title', 'type', 'ingredients',  'engineers',
    )
    column_searchable_list = (
        'title',
    )
    column_filters = (
        'id', 'title', 'type', 'level'
    )
    column_select_related_list = (
        'engineers',
    )
    form_create_rules = (
        'title', 'type', 'level', 'engineers', 'ingredients', 'effects',
    )
    form_edit_rules = (
        'title', 'type', 'level', 'engineers', 'ingredients', 'effects',
    )
    inline_models = (
        Ingredient,
    )


class MaterialView(ModelView):
    column_list = (
        'id', 'title', 'type', 'rarity_sort', 'locations'
    )
    column_filters = (
        'id', 'title', 'type', 'rarity_sort'
    )
    form_create_rules = (
        'title', 'type', 'rarity_sort', 'locations'
    )
    form_edit_rules = (
        'title', 'type', 'rarity_sort', 'locations'
    )

class LocationView(ModelView):
    column_list = ("title")


config = DotDict()
with open("config.yml", "r") as fp:
    config.update(yaml.load(fp))
logging.config.dictConfig(config["logging"])
log = logging.getLogger(__name__)


app = Flask(__name__)
app.secret_key = 'sars43rd3t45dsnrd'
app.config['SESSION_TYPE'] = 'filesystem'
admin = Admin(app, name='engineerdb', template_mode='bootstrap3')
engine = create_engine(config["db.url"], echo=config["db.echo"])
Session = sessionmaker(bind=engine)
db = Session()


@app.after_request
def after_request(response):
    db.commit()
    return response


admin.add_view(ModelView(Engineer, db))
admin.add_view(BlueprintView(Blueprint, db))
admin.add_view(MaterialView(Material, db))
admin.add_view(ModelView(Ingredient, db))
admin.add_view(ModelView(PrimaryEffect, db))
admin.add_view(ModelView(Location, db))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "127.0.0.1"),
        port=int(os.environ.get("PORT", 5000)),
        debug=True)
