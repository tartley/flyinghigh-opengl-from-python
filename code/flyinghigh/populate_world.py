
from __future__ import division

from .engine.gameitem import GameItem
from .component.glyph import Glyph
from .component.position import Position
from .component.shapes import CubeCluster


def populate(world):
    item = GameItem(
        position=Position(0, 0, 0),
        shape=CubeCluster(1.0, 64, 9000),
        glyph=Glyph(),
    )
    item.glyph.from_shape(item)
    world.add(item)

