===============
Collector-Drone
===============

Companion web-app for Elite: Dangerous, manage blueprints and material inventory
for crafting engineer upgrades.


*****
Setup
*****

Create a python virtual env and install dependencies::

    > virtualenv env
    > source env/bin/active
    > pip install -r packages.txt

Configure
=========

Copy ``example.config.yml`` to ``config.yml`` and edit.

Importing data
==============

Get data from spreadsheet https://forums.frontier.co.uk/showthread.php/248275-Engineering-Database-And-Calculator-Engineers-Update.
Export sheet "Components" as CSV and import using
``collectordrone/blueprint_import.py``::

    > python collectordrone/blueprint_import.py data/blueprints.csv

Get data from http://inara.cz/galaxy-components, copy main component table as
HTML, import into LibreOffice Calc, OpenOffice Calc or other spreadsheet. Export
as CSV and import using ``collectordrone/materials_import.py``::

    > python collectordrone/material_import.py inara_import data/inara-materials.csv

API
===

Run API::

    > FLASK_DEBUG=1 FLASK_APP=collectordrone/app.py flask run

API is now available as ``http://localhost:5000``

Setup and Build Frontend
========================

Frontend is written in Coffeescript and needs to be compiled to JavaScript::

    > cd frontend
    frontend> npm install
    frontend> grunt

If API is running and frontend is built, visiting ``http://localhost:5000/``
should redirect to the actual app
``http://localhost:5000/static/frontend/index.html``.


*****************
API Documentation
*****************

Models
======

Blueprint
---------
:id:          primary key, integer
:title:       string, name of blueprint
:type:        string, name of module this blueprint upgrades
:level:       integer, upgrade level
:engineers:   relation, list of Engineer items, engineers that offer this upgrade
:materials:   relation, list of Material items, materials this blueprint requires
:ingredients: relation, list of Ingredient items, quantity per material this blueprint requires
:effects:     relation, list of Effect items, primary effects, possible gains or losses when applied

PrimaryEffect
-------------
:id: primary key, integer
:blueprint_id: foreign key integer
:title: string
:influence: enum ``GAIN``, ``LOSS``
:min: float
:max: float
:blueprint: relation, Blueprint item

Material
--------

:id:          primary key, integer
:title:       string, name of material
:description: string, description of material
:rarity:      string, one of ``very common``, ``common``, ``standard``, ``rare``, ``very rare``
:type:        string, one of ``commodity``, ``data``, ``element``, ``manufactured``
:locations:   relation, list of Location items

Ingredient
----------
:id: primary key, integer
:material_id: foreign key, integer
:blueprint_id: foreign key, integer
:quantity: integer
:material: relation, Material item
:blueprint: relation, Blueprint item

Location
--------
:id:        primary key, integer
:title:     string, name of location
:materials: relation, list of Material items

Engineer
--------
:id:   primary key, integer
:name: string

HTTP Endpoints
==============

Search query syntax
-------------------

JSON request body must contain a ``query`` attribute. ``query`` must be an
object with one attribute matching one of the supported operators:

:and:     array, boolean and, all criteria in array must match
:or:      array, boolean or, any criteria in array must match
:eq:      object, case sensitive, field value must match query value
:ilike:   object, case insensitive, field value contains query value
:neq:     object, case sensitive, field value must not match query value
:gt:      object, numeric greater than, field value must be greater than query
          value
:gte:     object, numeric greater or equal than, field value must be greater or
          equal to query value
:lt:      object, numeric lower than, field value must be lower than query value
:lte:     object, numeric lower or equal than, field value must be lower or
          equal to query value
:null:    string, field value must be null
:notnull: string, field value must not be null


Find blueprints matching title ``faster fsd`` and level greater than ``3``:

::

    {
        "query": {"and": [
            {"ilike": {"title": "%faster fsd%"}},
            {"gt": {"level": 3}}
        ]}
    }

Find materials matching type ``commodity`` or type ``element``:

::

    {
        "query": {"or": [
            {"eq": {"type": "commodity"}},
            {"eq": {"type": "element"}}
        ]}
    }


``GET /materials{?sort,with,offset,limit}``
-------------------------------------------

:sort: value format ``{field,dir}``, examples ``?sort=id,desc``, ``?sort=title,asc``
:with: join a relation and include in output, specify multiple times for multiple joins: ``?with=materials&with=engineers``
:offset: integer, offset of result set returned
:limit: integer, number of elements returned


``GET /materials/{id}``
-----------------------

``POST /materials/search``
--------------------------

JSON request attributes

:sort:   string, format ``{field,dir}``, examples ``{sort: "id,desc"}``,
         ``{sort: "title,asc"}``
:with:   array, join a relation and include in output, eg.
         ``{with: ["materials", "engineers"}``
:offset: integer, offset of result set returned
:limit:  integer, number of elements returned
:query:  object, see query syntax

JSON response attributes

:items:  array, result items
:count:  integer, total count of items matching query (without ``offset``,
         ``limit``)
:sort:   same as request
:with:   same as request
:offset: same as request
:limit:  same as request

``GET /materials/types``
------------------------

``GET /blueprints{?sort,with,offset,limit}``
--------------------------------------------

:sort:   value format ``{field,dir}``, examples ``?sort=id,desc``,
         ``?sort=title,asc``
:with:   join a relation and include in output, specify multiple times for
         multiple joins: ``?with=materials&with=engineers``
:offset: integer, offset of result set returned
:limit:  integer, number of elements returned

``POST /blueprints/search``
---------------------------

JSON request attributes

:sort:   string, format ``{field,dir}``, examples ``{sort: "id,desc"}``,
         ``{sort: "title,asc"}``
:with:   array, join a relation and include in output, eg.
         ``{with: ["materials", "engineers"}``
:offset: integer, offset of result set returned
:limit:  integer, number of elements returned
:query:  object, see query syntax

JSON response attributes

:items:  array, result items
:count:  integer, total count of items matching query (without ``offset``,
         ``limit``)
:sort:   same as request
:with:   same as request
:offset: same as request
:limit:  same as request

``GET /blueprints/{id}``
------------------------

``GET /blueprints/types``
-------------------------

``GET /engineers{?sort,with,offset,limit}``
-------------------------------------------

:sort:   value format ``{field,dir}``, examples ``?sort=id,desc``,
         ``?sort=title,asc``
:with:   join a relation and include in output, specify multiple times for
         multiple joins: ``?with=materials&with=engineers``
:offset: integer, offset of result set returned
:limit:  integer, number of elements returned
