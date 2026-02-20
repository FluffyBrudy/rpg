from pathlib import Path
from typing import Dict, Tuple

from pgutils.utils.image_utils import load_image
from pygame import Surface, Vector2

from lib.loader.maploader import (
    BaseLayer,
    TileLayer,
    Tilemap,
    parse_tilemap_file,
)


class TilemapRenderer:
    def __init__(self) -> None:
        self.initialized = False

    @staticmethod
    def __load_tile_cache(mapdata: "Tilemap"):
        # tile cache store (tileset_index, tile_variant)
        tile_cache: Dict[Tuple[int, int], Surface] = {}

        tile_size = mapdata.meta.tile_size
        tile_tilesets = [x for x in mapdata.resources.tilesets]

        for ttype, tilesets in enumerate(tile_tilesets):
            path = Path(tilesets.path)
            tileset_surf = load_image(path)
            ncol, nrow = int(tileset_surf.width // tile_size[0]), int(tileset_surf.height // tile_size[1])
            variant_id = 0
            for _ in range(ncol):
                for __ in range(nrow):
                    r, c = variant_id // ncol, variant_id % ncol
                    tile_cache[(ttype, variant_id)] = tileset_surf.subsurface(
                        (c * tile_size[0], r * tile_size[1], *tile_size)
                    )
                    variant_id += 1

        return tile_cache

    def load_map(self, path: Path):
        def sort_callback(layer: "BaseLayer"):
            return layer.z_index

        mapdata = parse_tilemap_file(path)
        self.initialized = True
        self.map_size = mapdata.meta.map_size
        self.tile_size = mapdata.meta.tile_size
        self.tile_cache = self.__load_tile_cache(mapdata)
        self.tile_layers = sorted(
            [layer for layer in mapdata.data.layers if isinstance(layer, TileLayer)],
            key=sort_callback,
        )
        print(self.tile_cache)

    def render_tiles(self, surface: Surface, offset: Vector2):
        tw, th = self.tile_size
        for layer in self.tile_layers:
            for point, tile in layer.tiles.items():
                tile_surf = self.tile_cache[(tile.ttype, tile.variant)]
                pos = (point[0] * tw, point[1] * th)
                surface.blit(tile_surf, pos - offset)
