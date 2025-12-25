class TestConjuredItems:
    """Test para items conjurados, degradan al doble de velocidad"""

    def test_conjured_normal_day(self, update_quality):
        """Quality -2 en día normal."""
        item = update_quality(name="Conjured Mana Cake", sell_in=10, quality=10)

        assert item.quality == 8
        assert item.sell_in == 9

    def test_conjured_expired(self, update_quality):
        """Quality -4 en día expirado."""
        item = update_quality(name="Conjured Mana Cake", sell_in=0, quality=10)
        assert item.quality == 6
        assert item.sell_in == -1

    def test_conjured_never_negative(self, update_quality):
        """Quality nunca es negativa."""
        item = update_quality(name="Conjured Mana Cake", sell_in=10, quality=0)
        assert item.quality == 0
