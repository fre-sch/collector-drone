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

from errors import ServiceError
from sqlalchemy import or_, and_, not_


def model_filter(crit, model):
    try:
        if crit.op == "and":
            return and_(*[model_filter(it, model) for it in crit.value])
        elif crit.op == "or":
            return or_(*[model_filter(it, model) for it in crit.value])
        elif crit.op == "eq":
            return getattr(model, crit.field) == crit.value
        elif crit.op == "ilike":
            return getattr(model, crit.field).ilike(crit.value)
        elif crit.op == "neq":
            return getattr(model, crit.field) != crit.value
        elif crit.op == "gt":
            return getattr(model, crit.field) > crit.value
        elif crit.op == "lt":
            return getattr(model, crit.field) < crit.value
        elif crit.op == "gte":
            return getattr(model, crit.field) >= crit.value
        elif crit.op == "lte":
            return getattr(model, crit.field) <= crit.value
        elif crit.op == "null":
            return getattr(model, crit.field) == None
        elif crit.op == "notnull":
            return getattr(model, crit.field) != None
        elif crit.op == "not":
            return not_(model_filter(crit.value, model))
    except AttributeError:
        raise ServiceError("invalid query field %s" % crit.field)
