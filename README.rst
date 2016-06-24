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

Get data from spreadsheet https://forums.frontier.co.uk/showthread.php/248275-Engineering-Database-And-Calculator-Engineers-Update. Export sheet "Components" as CSV and import using ``collectordrone/blueprint_import.py``.

Get data from http://inara.cz/galaxy-components, copy main component table as HTML, import into LibreOffice Calc, OpenOffice Calc or other spreadsheet. Export as CSV and import using ``collectordrone/materials_import.py``.

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

If API is running and frontend is built, visiting ``http://localhost:5000/`` should redirect to the actual app ``http://localhost:5000/static/frontend/index.html``.
