"""Property-based

Estos tests verifican propiedades (invariantes) que deben cumplirse
siempre, independientemente de los valores de entrada.
"""

from hypothesis import assume, given
from hypothesis import strategies as st

from gilded_rose import GildedRose, Item
from gilded_rose.constants import AGED_BRIE, BACKSTAGE_PASSES, MAX_QUALITY, MIN_QUALITY, SULFURAS


class TestQualityInvariants:
    """
    Invariantes universales sobre quality.
    """

    @given(
        name=st.text(min_size=1, max_size=50),
        sell_in=st.integers(min_value=-100, max_value=100),
        quality=st.integers(min_value=0, max_value=50),
    )
    def test_quality_never_negative(self, name, sell_in, quality):
        assume(name != SULFURAS)  # excluir a sulfuras
        item = Item(name, sell_in, quality)
        gilded_rose = GildedRose([item])

        for _ in range(100):
            gilded_rose.update_quality()
            assert (
                item.quality >= MIN_QUALITY
            ), f"Quality no puede ser negativa. Item: {item.name}, Quality: {item.quality}"

    @given(
        name=st.text(min_size=1, max_size=50),
        sell_in=st.integers(min_value=-100, max_value=100),
        quality=st.integers(min_value=0, max_value=50),
    )
    def test_quality_never_exceeds_max(self, name, sell_in, quality):
        """Property: Quality nunca excede MAX_QUALITY (50)."""
        assume(name != SULFURAS)  # Sulfuras tiene quality 80, es excepción
        item = Item(name, sell_in, quality)
        gilded_rose = GildedRose([item])

        for _ in range(100):
            gilded_rose.update_quality()
            assert item.quality <= MAX_QUALITY, (
                f"Quality no puede exceder {MAX_QUALITY}. "
                f"Item: {item.name}, quality: {item.quality}"
            )

    @given(
        sell_in=st.integers(min_value=-100, max_value=100),
        quality=st.integers(min_value=0, max_value=50),
    )
    def test_quality_always_in_valid_range(self, sell_in, quality):
        """Property: Quality siempre está en rango válido [0, 50].

        Test más completo que combina ambas propiedades.
        """
        item = Item("Normal Item", sell_in, quality)
        gilded_rose = GildedRose([item])

        for _ in range(100):
            gilded_rose.update_quality()
            assert (
                MIN_QUALITY <= item.quality <= MAX_QUALITY
            ), f"Quality fuera de rango: {item.quality}"


class TestSulfurasInvariants:
    """
    Invariantes universales sobre Sulfuras.
    """

    @given(
        sell_in=st.integers(min_value=-100, max_value=100),
    )
    def test_sulfuras_never_changes(self, sell_in):
        """Property: Sulfuras nunca cambia (quality=80, sell_in constante).

        Esta es una propiedad crítica: Sulfuras es inmutable.
        """

        item = Item(SULFURAS, sell_in, 80)
        gilded_rose = GildedRose([item])

        for _ in range(100):
            old_quality = item.quality
            old_sell_in = item.sell_in

            gilded_rose.update_quality()

            assert (
                item.quality == old_quality
            ), f"Sulfuras quality cambió de {old_quality} a {item.quality}"
            assert (
                item.sell_in == old_sell_in
            ), f"Sulfuras sell_in cambió de {old_sell_in} a {item.sell_in}"


class TestAgedBrieProperties:
    """Propiedades específicas de Aged Brie."""

    @given(
        sell_in=st.integers(min_value=-100, max_value=100),
        quality=st.integers(min_value=0, max_value=49),  # Menos de 50 para que pueda aumentar
    )
    def test_aged_brie_never_decreases(self, sell_in, quality):
        """Property: Aged Brie nunca disminuye su quality.

        Aged Brie siempre mejora o se mantiene (hasta llegar a 50).
        """
        item = Item(AGED_BRIE, sell_in, quality)
        gilded_rose = GildedRose([item])

        for _ in range(10):
            old_quality = item.quality
            gilded_rose.update_quality()

            # Si no está en el máximo, debe aumentar o mantenerse
            if old_quality < MAX_QUALITY:
                assert (
                    item.quality >= old_quality
                ), f"Aged Brie quality disminuyó de {old_quality} a {item.quality}"


class TestBackstagePassesProperties:
    """Propiedades específicas de Backstage Passes."""

    @given(
        sell_in=st.integers(min_value=1, max_value=100),
        quality=st.integers(min_value=0, max_value=49),
    )
    def test_backstage_passes_increase_before_concert(self, sell_in, quality):
        """Property: Backstage passes aumentan antes del concierto."""
        item = Item(BACKSTAGE_PASSES, sell_in, quality)
        gilded_rose = GildedRose([item])

        old_quality = item.quality
        gilded_rose.update_quality()

        # Si no ha expirado, debe aumentar
        if item.sell_in >= 0:
            assert item.quality >= old_quality or item.quality == MAX_QUALITY

    @given(
        quality=st.integers(min_value=0, max_value=50),
    )
    def test_backstage_passes_zero_after_expired(self, quality):
        """Property: Backstage passes siempre son 0 después de expirar."""
        item = Item(BACKSTAGE_PASSES, 0, quality)  # sell_in=0, está expirado
        gilded_rose = GildedRose([item])

        gilded_rose.update_quality()

        assert (
            item.quality == 0
        ), f"Backstage pass debe ser 0 después de expirar, obtuvo {item.quality}"


class TestConjuredProperties:
    """Propiedades específicas de items Conjured."""

    @given(
        sell_in=st.integers(min_value=1, max_value=100),
        quality=st.integers(min_value=2, max_value=50),
    )
    def test_conjured_decreases_faster_than_normal(self, sell_in, quality):
        """Property: Conjured items disminuyen al doble de velocidad.

        Compara con un item normal para verificar que Conjured
        disminuye más rápido.
        """
        conjured = Item("Conjured Mana Cake", sell_in, quality)
        normal = Item("Mi Item normal", sell_in, quality)

        gr_conjured = GildedRose([conjured])
        gr_normal = GildedRose([normal])

        gr_conjured.update_quality()
        gr_normal.update_quality()

        # Conjured debe haber disminuido más (o igual si ambos llegaron a 0)
        if normal.quality > 0 and conjured.quality > 0:
            normal_decrease = quality - normal.quality
            conjured_decrease = quality - conjured.quality
            assert conjured_decrease >= normal_decrease * 2, (
                f"Conjured debería disminuir al doble. "
                f"Normal: -{normal_decrease}, Conjured: -{conjured_decrease}"
            )
