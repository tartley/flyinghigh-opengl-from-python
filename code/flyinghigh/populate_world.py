
from __future__ import division

from .engine.gameitem import GameItem
from .component.glyph import Glyph
from .component.position import Position
from .component.shapes import CubeCluster


def populate(world):
    shape = CubeCluster(1.0, 80, 9000)
    item = GameItem(
        position=Position(0, 0, 0),
        shape=shape,
        glyph=Glyph(),
    )
    world.add(item)

