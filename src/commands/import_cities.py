import csv
import sys
from dataclasses import dataclass

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.data_access.postgresql.tables.city import city_table


@dataclass
class Polygon:
    coords: list[str]


@dataclass
class City:
    name: str
    guid: str
    polygon: Polygon


def construct_polygon(wtk: str) -> Polygon:
    coords = wtk.split("((")[1].split("))")[0].split(",")
    final_coords = []
    for coord in coords:
        final_coords.append(coord)
    return Polygon(coords=final_coords)


def construct_wtk(polygon: Polygon) -> str:
    return "POLYGON(( " + ",".join(polygon.coords) + "))"


async def import_cities(session: AsyncSession) -> None:
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
                    new_polygon = construct_polygon(row[0])
                    if len(city.polygon.coords) < len(new_polygon.coords):
                        city.polygon = new_polygon
                else:
                    city = City(name=city_name, guid=row[1], polygon=construct_polygon(row[0]))
                    cities[city_name] = city

    insert_data = [
        {"name": city.name, "guid": city.guid, "geo": construct_wtk(city.polygon)}
        for city in cities.values()
    ]
    async with session:
        query = insert(city_table).values(insert_data)
        await session.execute(query)
        await session.commit()
        await session.commit()
