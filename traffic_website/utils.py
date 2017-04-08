import collections
import itertools

class DistanceCalculator:
    def __init__(self, zip_codes, conn):
        self._zip_codes = zip_codes
        self._conn = conn
        self._model_helper = ModelHelper(conn)

    def _get_distances(self, coords):
        data = collections.defaultdict(set)
        for coord in coords:
            dist_diff = coord[-1]
            for dist in coord[:2]:
                data[dist].add(dist_diff)
        return data

    async def ref_points(self):
        coordinates = collections.namedtuple("Coordinates", "zip_code lat long")
        coordinate_list = [coordinates(zip_code=data.zip_code, lat=float(data.lat), long=float(data.long)) async for
                           data in self._get_zip_coords()]
        loop = asyncio.get_event_loop()
        if len(coordinate_list) > 1:
            distance_list = await loop.run_in_executor(None,self._get_distance_list, coordinate_list)
            return self._calc_furthest_points(distance_list)
        return coordinate_list

    def _get_distance_list(self, coordinate_list):
        coords = itertools.combinations(coordinate_list, 2)
        distance_diffs = [self.calc_dist(coord[0], coord[1]) for coord in coords]
        return self._get_distances(distance_diffs)

    def _calc_furthest_points(self, distances):
        average_distance = lambda key: sum(distances[key]) / len(distances[key])
        return sorted(distances.keys(), key=average_distance, reverse=True)[:3] # top 3 furthest points


    async def _get_zip_coords(self):
        for zip_code in self._zip_codes:
            coords = await self._model_helper.execute(f"SELECT * FROM public.zip_codes WHERE zip_code =CAST({zip_code} AS VARCHAR)")
            for coord in coords:
                if coord:
                    yield coord
