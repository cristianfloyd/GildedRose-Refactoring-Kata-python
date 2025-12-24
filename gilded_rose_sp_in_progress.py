# Constants
from typing import Protocol

from item import Item

MAX_QUALITY = 50
MIN_QUALITY = 0
AGED_BRIE = "Aged Brie"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"

# Aged Brie
AGED_BRIE_INCREMENT = 1
AGED_BRIE_EXPIRED_INCREMENT = 1

# Backstage passes
BACKSTAGE_FIRST_THRESHOLD = 11
BACKSTAGE_SECOND_THRESHOLD = 6
BACKSTAGE_FAR_INCREMENT = 1  # > 10 días
BACKSTAGE_MEDIUM_INCREMENT = 2  # 6-10 días
BACKSTAGE_NEAR_INCREMENT = 3  # 1-5 días
BACKSTAGE_EXPIRED_QUALITY = 0  # después del concierto
MIN_SELL_IN = 0

# Normal items
NORMAL_DAILY_DECREMENT = 1
NORMAL_DAILY_INCREMENT = 1
NORMAL_EXPIRED_DECREMENT = 2


class ItemUpdaterStrategy(Protocol):
    """
    Estrategia para actualizar la calidad y días de venta de un item.
    """

    def update(self, item: Item) -> None:
        ...


class SulfurasStrategy:
    """Sulfuras nunca cambia."""

    def update(self, item: Item) -> None:
        pass  # No hace nada


class NormalItemStrategy:
    """
    Estrategia para actualizar items normales.
    """

    @staticmethod
    def _increase_quality(item: Item, amount: int) -> None:
        item.quality = min(MAX_QUALITY, item.quality + amount)

    @staticmethod
    def _decrease_quality(item: Item, amount: int) -> None:
        item.quality = max(MIN_QUALITY, item.quality - amount)

    def update(self, item: Item) -> None:
        self._decrease_quality(item, NORMAL_DAILY_DECREMENT)
        item.sell_in -= NORMAL_DAILY_DECREMENT

        if item.sell_in < 0:
            self._decrease_quality(item, NORMAL_EXPIRED_DECREMENT)


class AgedBrieStrategy:
    """
    Aged Brie que mejora con el tiempo.
    """

    @staticmethod
    def _increase_quality(item: Item, amount: int) -> None:
        item.quality = min(MAX_QUALITY, item.quality + amount)

    def update(self, item: Item) -> None:
        self._increase_quality(item, AGED_BRIE_INCREMENT)
        item.sell_in -= NORMAL_DAILY_DECREMENT

        if item.sell_in < MIN_SELL_IN:
            self._increase_quality(item, AGED_BRIE_EXPIRED_INCREMENT)


class BackstagePassStrategy:
    """Backstage passes con reglas especiales."""

    FIRST_THRESHOLD = 11
    SECOND_THRESHOLD = 6

    @staticmethod
    def _increase_quality(item: Item, amount: int) -> None:
        item.quality = min(MAX_QUALITY, item.quality + amount)

    def update(self, item: Item) -> None:
        # Calcular incremento según días restantes
        if item.sell_in < self.SECOND_THRESHOLD:
            increment = BACKSTAGE_NEAR_INCREMENT
        elif item.sell_in < self.FIRST_THRESHOLD:
            increment = BACKSTAGE_MEDIUM_INCREMENT
        else:
            increment = BACKSTAGE_FAR_INCREMENT

        self._increase_quality(item, increment)
        item.sell_in -= NORMAL_DAILY_DECREMENT
        if item.sell_in < MIN_SELL_IN:
            item.quality = BACKSTAGE_EXPIRED_QUALITY


# Factory pattern - para crear las estrategias de actualización de items.
class ItemStrategyFactory:
    """
    Fabrica de estrategias de actualización de items.
    """

    _strategies = {
        SULFURAS: SulfurasStrategy(),
        AGED_BRIE: AgedBrieStrategy(),
        BACKSTAGE_PASSES: BackstagePassStrategy(),
    }

    @classmethod
    def get_strategy(cls, item_name: str) -> ItemUpdaterStrategy:
        return cls._strategies.get(item_name, NormalItemStrategy())


# clase nueva que usa el factory pattern
class GildedRoseRefactored:
    def __init__(self, items: list[Item]) -> None:
        self.items = items

    def update_quality(self) -> None:
        for item in self.items:
            strategy = ItemStrategyFactory.get_strategy(item.name)
            strategy.update(item)
