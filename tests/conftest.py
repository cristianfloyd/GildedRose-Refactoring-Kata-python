import pytest

from gilded_rose import GildedRose, Item

# conftest.py


@pytest.fixture
def update_quality():
    """Retorna una función que facilita la ejecución de un ciclo de actualización."""

    def _update(name, sell_in, quality):
        item = Item(name, sell_in, quality)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        return item

    return _update
