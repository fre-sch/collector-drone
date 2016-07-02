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

from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    Numeric,
    ForeignKey,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


Base = declarative_base()


def to_dict(mdl):
    return {
        c.name: getattr(mdl, c.name)
        for c in mdl.__table__.columns
    }


tbl_blueprint_engineer = Table("blueprint_engineer", Base.metadata,
    Column("blueprint_id", Integer, ForeignKey("blueprint.id")),
    Column("engineer_id", Integer, ForeignKey("engineer.id"))
)
tbl_location_material = Table("location_material", Base.metadata,
    Column("location_id", Integer, ForeignKey("location.id")),
    Column("material_id", Integer, ForeignKey("material.id")),
)


class Engineer(Base):
    __tablename__ = "engineer"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def to_dict(self, rel=list()):
        d = to_dict(self)
        if "blueprints" in rel:
            d["blueprints"] = [r.to_dict() for r in self.blueprints]
        return d


class Material(Base):
    __tablename__ = "material"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    _rarity = Column(Integer, name="rarity")
    type = Column(String)

    @property
    def rarity(self):
        enum = {
            0: "very common",
            1: "common",
            2: "standard",
            3: "rare",
            4: "very rare"
        }
        return enum.get(self._rarity, "common")

    def to_dict(self, rel=list()):
        d = to_dict(self)
        if "blueprints" in rel:
            d["blueprints"] = [r.to_dict() for r in self.blueprints]
        if "locations" in rel:
            d["locations"] = [r.to_dict() for r in self.locations]
        return d


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    materials = relationship(Material,
            secondary=tbl_location_material,
            backref=backref("locations"))

    def to_dict(self, rel=list()):
        d = to_dict(self)
        if "materials" in rel:
            d["materials"] = [r.to_dict() for r in self.materials]
        return d

    def __repr__(self):
        return repr(self.to_dict())


class Blueprint(Base):
    __tablename__ = "blueprint"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(String)
    level = Column(Integer)
    engineers = relationship(Engineer,
            secondary=tbl_blueprint_engineer,
            backref=backref("blueprints"))
    materials = relationship(Material,
            secondary="ingredient",
            backref=backref("blueprints"))

    def to_dict(self, rel=list()):
        d = to_dict(self)
        if "engineers" in rel:
            d["engineers"] = [e.to_dict() for e in self.engineers]
        if "effects" in rel:
            d["effects"] = [e.to_dict() for e in self.effects]
        if "ingredients" in rel:
            d["ingredients"] = [i.to_dict() for i in self.ingredients]
        return d


class PrimaryEffect(Base):
    __tablename__ = "primary_effect"
    id = Column(Integer, primary_key=True)
    blueprint_id = Column(Integer, ForeignKey("blueprint.id"))
    title = Column(String)
    influence = Column(Enum("GAIN", "LOSS"))
    min = Column(Numeric(10, 2, asdecimal=False))
    max = Column(Numeric(10, 2, asdecimal=False))
    blueprint = relationship(Blueprint, backref=backref("effects"))

    def to_dict(self, rel=list()):
        d = to_dict(self)
        if "blueprint" in rel:
            d["blueprint"] = self.blueprint.to_dict()
        return d


class Ingredient(Base):
    __tablename__ = "ingredient"
    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey("material.id"))
    blueprint_id = Column(Integer, ForeignKey("blueprint.id"))
    quantity = Column(Integer)
    material = relationship(Material, backref=backref("ingredients"))
    blueprint = relationship(Blueprint, backref=backref("ingredients"))

    def to_dict(self):
        d = {}
        d["material"] = self.material.to_dict()
        d["quantity"] = self.quantity
        return d
