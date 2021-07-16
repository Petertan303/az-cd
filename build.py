import logging
import os
import re
import json
import shutil

from utils.crawl import get_text


def setup_ship_reload_info():
    text = get_text(
        url="https://wiki.biligame.com/blhx/index.php?title=MediaWiki:PN.js&action=raw&ctype=text/javascript",
        params={},
        path="resources/cache/PN.js",
    )

    ship_data = {}
    for sid, blvl, row, name in re.findall(
        r"(?m)^PN(\w+)(\d):\[(.+?)\],?\s*//(.+?)_", text
    ):
        ship_data.setdefault(sid, {"name": name, "data": {}})
        data = ship_data[sid]["data"]
        # 15装填基础,16装填成长,17装填额外,40可强化装填,46装填改造
        keys = [15, 16, 17, 40, 46]
        row = row.split(",")
        data[blvl] = [int(row[idx]) for idx in keys]

    with open("resources/data_reload.json", "w", -1, "UTF8") as f:
        json.dump(ship_data, f, ensure_ascii=False, indent=2)


def setup_ship_data():
    from utils.ships import get_ship_data

    ship_info = []
    for ship in get_ship_data():
        ship_info.append(ship)
    with open('resources/ships.json', 'w', -1, 'UTF8') as f:
        json.dump(ship_info, f, ensure_ascii=False, indent=2)


def setup_equip_data():
    from utils.equips import get_equip_data

    equip_info = []
    for equip in get_equip_data():
        equip_info.append(equip)
    with open('resources/equips.json', 'w', -1, 'UTF8') as f:
        json.dump(equip_info, f, ensure_ascii=False, indent=2)


def copy_dict(d, keys=None):
    if d is None:
        return None
    if keys is None:
        keys = d.keys()
    return {k: d[k] for k in keys}


def generate_files():
    with open('resources/ships.json', 'r', -1, 'UTF8') as f:
        data = json.load(f)
    data = [copy_dict(s, ['编号', '名称', '类型', 'match']) for s in data]
    with open('static/data/ships.json', 'w', -1, 'UTF8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    if os.path.exists("build"):
        shutil.rmtree("build")
    shutil.copytree("static", "build")


if __name__ == "__main__":
    logging.basicConfig(level="INFO")

    # setup_ship_reload_info()
    setup_ship_data()
    # setup_equip_data()
    generate_files()
