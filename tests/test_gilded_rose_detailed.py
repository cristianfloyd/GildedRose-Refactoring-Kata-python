from gilded_rose import AGED_BRIE, BACKSTAGE_PASSES, SULFURAS, GildedRose, Item


class TestSulfuras:
    """Sulfuras nunca cambia"""

    def test_sulfuras_quality_never_changes(self):
        sulfuras = Item(name=SULFURAS, sell_in=10, quality=80)
        gilded_rose = GildedRose([sulfuras])
        gilded_rose.update_quality()
        assert sulfuras.quality == 80

    def test_sulfuras_sell_in_never_changes(self):
        sulfuras = Item(name=SULFURAS, sell_in=10, quality=80)
        gilded_rose = GildedRose([sulfuras])
        gilded_rose.update_quality()
        assert sulfuras.sell_in == 10


class TestAgedBrie:
    """Aged Brie aumenta su calidad con el tiempo"""

    def test_aged_brie_quality_increases_by_one(self):
        aged_brie = Item(name=AGED_BRIE, sell_in=10, quality=10)
        gilded_rose = GildedRose([aged_brie])
        gilded_rose.update_quality()
        assert aged_brie.quality == 11

    def test_aged_brie_quality_increase_double_after_sell_date(self):
        aged_brie = Item(name=AGED_BRIE, sell_in=0, quality=10)
        gilded_rose = GildedRose([aged_brie])
        gilded_rose.update_quality()
        assert aged_brie.quality == 12  # +1 adicional por que sell_in es 0

    def test_aged_brie_quality_never_exceeds_50(self):
        aged_brie = Item(name=AGED_BRIE, sell_in=10, quality=50)
        gilded_rose = GildedRose([aged_brie])
        gilded_rose.update_quality()
        assert aged_brie.quality == 50


class TestBackstagePasses:
    """Backstage passes  tienen reglas especiales"""

    def test_backstage_passes_increases_by_1_when_more_than_10_days(self):
        backstage_passes = Item(name=BACKSTAGE_PASSES, sell_in=15, quality=20)
        gilded_rose = GildedRose([backstage_passes])
        gilded_rose.update_quality()
        assert backstage_passes.quality == 21

    def test_backstage_passes_increases_by_2_when_10_days_or_less(self):
        backstage_passes = Item(name=BACKSTAGE_PASSES, sell_in=10, quality=20)
        gilded_rose = GildedRose([backstage_passes])
        gilded_rose.update_quality()
        assert backstage_passes.quality == 22

    def test_backstage_passes_increases_by_3_when_5_days_or_less(self):
        backstage_passes = Item(name=BACKSTAGE_PASSES, sell_in=5, quality=20)
        gilded_rose = GildedRose([backstage_passes])
        gilded_rose.update_quality()
        assert backstage_passes.quality == 23

    def test_backstage_passes_drops_to_0_after_concert(self):
        backstage_passes = Item(name=BACKSTAGE_PASSES, sell_in=0, quality=20)
        gilded_rose = GildedRose([backstage_passes])
        gilded_rose.update_quality()
        assert backstage_passes.quality == 0


class TestNormalItems:
    """Items normales tienen reglas simples"""

    def test_normal_item_decreases_quality(self):
        item = Item(name="Normal Item", sell_in=10, quality=10)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        assert item.quality == 9

    def test_normal_item_decreases_double_after_sell_date(self):
        item = Item(name="Normal Item", sell_in=0, quality=10)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        assert item.quality == 8  # -1 normal, -1 extra

    def test_normal_item_quality_never_negative(self):
        item = Item(name="Normal Item", sell_in=10, quality=0)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        assert item.quality == 0
