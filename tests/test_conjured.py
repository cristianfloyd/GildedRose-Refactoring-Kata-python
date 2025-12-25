from gilded_rose import GildedRose
from item import Item


class TestConjuredItems:
    """Test para items conjurados, degradan al dobre de velocidad"""

    def test_conjured_normal_day(self):
        """Quality -2 en día normal."""
        item = Item(name="Conjured Mana Cake", sell_in=10, quality=10)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()

        assert item.quality == 8
        assert item.sell_in == 9

    def test_conjured_expired(self):
        """Quality -4 en día expirado."""
        item = Item(name="Conjured Mana Cake", sell_in=0, quality=10)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()

        assert item.quality == 6
        assert item.sell_in == -1

    def test_conjured_never_negative(self):
        """Quality nunca es negativa."""
        item = Item(name="Conjured Mana Cake", sell_in=10, quality=0)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()

        assert item.quality == 0
