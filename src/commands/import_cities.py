import csv
import sys
from dataclasses import dataclass

from src.infrastructure.data_access.postgresql.db import Session


@dataclass
class Polygon:
    coords: list[tuple[str, str]]


@dataclass
class City:
    name: str
    guid: str
    polygon: Polygon


def merge_polygons(original: Polygon, new: Polygon) -> None:
    original.coords.extend(new.coords)


def construct_polygon(wtk: str) -> Polygon:
    coords = wtk.split("((")[1].split("))")[0].split(",")
    final_coords = []
    for coord in coords:
        x, y = coord.split(" ")
        final_coords.append((x, y))
    return Polygon(coords=final_coords)


async def import_cities() -> None:
    session = Session()
    csv.field_size_limit(sys.maxsize)
    cities: dict[str, City] = {}
    with open("src/commands/resources/russia_town_and_city_borders_polygon.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            city_type = row[-6]
            if city_type == "city":
                city_name = row[-8]
                if city_name in cities:
                    city = cities[city_name]
                    merge_polygons(city.polygon, construct_polygon(row[0]))
                else:
                    city = City(
                        name=row[-8], guid=row[1], polygon=construct_polygon(row[0])
                    )
                    cities[city_name] = city
