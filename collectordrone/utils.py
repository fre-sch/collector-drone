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

import yaml
from UserDict import UserDict


class DotDict(UserDict):

    def __getitem__(self, name):
        if name in self:
            return UserDict.__getitem__(self, name)

        current_data = self
        for chunk in name.split('.'):
            if chunk not in current_data:
                return None
            current_data = current_data[chunk]
        return current_data


def load_config():
    config = DotDict()
    with open("config.yml", "r") as fp:
        config.update(yaml.load(fp))
    return config


def slugify(val):
    return re.sub(ur"\W+", "_", val.lower())


def prefix_tpl(prefix, value):
    if not value:
        return None
    return u"{}{}".format(prefix, value)
