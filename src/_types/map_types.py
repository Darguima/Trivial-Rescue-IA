from typing import TypedDict, Tuple, Dict, Literal, List, Optional


class City(TypedDict):
    id: str
    name: str
    capital_info: Dict[Literal["groceries", "cars", "trucks", "helicopters"], int]
    matrix_coords: Tuple[int, int]
    map_coords: Tuple[int, int]
    population: int
    elevation: int
    neighbors: Dict[Literal["land", "air", "sea"], List[str]]


CitiesDict = Dict[str, City]


class LandRoute(TypedDict):
    distance: float
    road_quality: float
    max_speed: int
    elevation_diff: int


class AirRoute(TypedDict):
    distance: float


class SeaRoute(TypedDict):
    distance: float


class RouteBetweenCities(TypedDict):
    land: Optional[LandRoute]
    air: Optional[AirRoute]
    sea: Optional[SeaRoute]


class RoutesDictElem(TypedDict):
    land: Dict[str, LandRoute]
    air: Dict[str, AirRoute]
    sea: Dict[str, SeaRoute]


RoutesDict = Dict[str, RoutesDictElem]
