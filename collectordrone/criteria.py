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

"""
Parse and validate a query dict to criteria tree.

Example:

>>> parse({"gt": {"quantity": 1}})
Criteria(op="gt", field="quantity", value=1)

Example:

>>> parse({"or": [
...    {"ilike": {"name": "%foo%"}},
...    {"ilike": {"name": "%bar%"}}
...]})
Criteria(op="or", field=None, value=[
    Criteria(op="ilike", field="name", value="%foo%"),
    Criteria(op="ilike", field="name", value="%bar%")
])
"""

from collections import namedtuple
from functools import wraps


Criteria = namedtuple("Criteria", ["op", "field", "value"])


class FilterParseError(Exception):
    pass


class Operator(object):
    registry = {}

    def __init__(self, symbol, ary):
        self.symbol = symbol
        self.ary = ary
        self.registry[symbol] = self

    def __call__(self, fn):
        @wraps(fn)
        def wrap(term):
            if self.ary == 0:
                if isiterable(term):
                    raise FilterParseError(
                            "invalid syntax, expected {%s: field}: %r"
                            % (self.symbol, term))
            elif self.ary == "*":
                if not isiterable(term):
                    raise FilterParseError(
                            "invalid syntax, expected {%s: value}: %r"
                            % (self.symbol, term))
            else:
                if not isiterable(term):
                    raise FilterParseError(
                            "invalid syntax, expected {%s: value}: %r"
                            % (self.symbol, term))
                try:
                    term = term.items()[0]
                except AttributeError:
                    pass
                if len(term) != self.ary:
                    raise FilterParseError(
                            "invalid syntax, expected {%s: {field: value}}: %r"
                            % (self.symbol, term))
            return fn(self.symbol, term)
        self.registry[self.symbol] = wrap
        return wrap


def isiterable(value):
    if isinstance(value, str):
        return False
    try:
        iter(value)
        return True
    except TypeError:
        return False


def parse(term):
    if not isiterable(term):
        raise FilterParseError("invalid syntax, expected {op: value}: %r" % term)
    try:
        term = term.items()
    except AttributeError:
        pass
    if len(term) != 1:
        raise FilterParseError("invalid syntax, expected {op: value}: %r" % term)

    op, value = term[0]
    if op in Operator.registry:
        return Operator.registry[op](value)
    else:
        return Operator.registry["eq"]((op, value))


@Operator("and", "*")
def parse_and(symbol, terms):
    return Criteria(symbol, None, [parse(it) for it in terms])


@Operator("or", "*")
def parse_or(symbol, terms):
    return Criteria(symbol, None, [parse(it) for it in terms])


@Operator("eq", 2)
def parse_eq(symbol, term):
    field, value = term
    return Criteria(symbol, field, value)


@Operator("ilike", 2)
def parse_ilike(symbol, term):
    field, value = term
    return Criteria(symbol, field, value)


@Operator("neq", 2)
def parse_neq(symbol, term):
    field, value = term
    return Criteria(symbol, field, value)


@Operator("gt", 2)
def parse_gt(symbol, term):
    field, value = term
    return Criteria(symbol, field, value)


@Operator("gte", 2)
def parse_gte(symbol, term):
    field, value = term
    return Criteria(symbol, field, value)


@Operator("lt", 2)
def parse_lt(symbol, term):
    field, value = term
    return Criteria(symbol, field, value)


@Operator("lte", 2)
def parse_lte(symbol, term):
    field, value = term
    return Criteria(symbol, field, value)


@Operator("null", 0)
def parse_null(symbol, term):
    return Criteria(symbol, term, None)


@Operator("notnull", 0)
def parse_notnull(symbol, term):
    return Criteria(symbol, term, None)


if __name__ == "__main__":
    from pprint import pprint

    query1 = {"and": [
        {"ilike": {"title": "crystal"}},
        {"gt": {"level": 1}},
        {"or": [
            {"rarity": "com"},
            {"rarity": "vcom"}
        ]},
        {"notnull": "engineer_id"},
        {"null": "deleted_date"},
    ]}
    query2 = {"gt": ("bar", "foo")}
    parsed = parse(query2)
    pprint(parsed)
