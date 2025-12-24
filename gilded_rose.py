# Constants
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


class GildedRose:
    """
    Sistema de gestion de inventario para la posada Gilded Rose.
    Actualiza la calidad y días de venta de los items, según reglas específicas.
    """

    def __init__(self, items: list[Item]) -> None:
        """
        Inicializa la lista de items para el sistema.
        Args:
            items (list): Lista de items a gestionar.
        """
        self.items = items

    @staticmethod
    def _decrease_quality_safe(item: Item, amount: int = NORMAL_DAILY_DECREMENT) -> None:
        """
        Disminuye la calidad de un item si no es el minimo.
        Args:
            item (Item): Item a disminuir.
        """
        item.quality = max(MIN_QUALITY, item.quality - amount)

    @staticmethod
    def _increase_quality_safe(item: Item, amount: int = NORMAL_DAILY_INCREMENT) -> None:
        """
        Aumenta la calidad de un item si no es el maximo.
        Args:
            item (Item): Item a aumentar.
        """
        item.quality = min(MAX_QUALITY, item.quality + amount)

    @staticmethod
    def _decrease_sell_in(item: Item) -> None:
        """
        Disminuye los días restantes para vender un item.
        Args:
            item (Item): Item a disminuir.
        """
        item.sell_in -= NORMAL_DAILY_DECREMENT

    def update_quality(self) -> None:
        """
        Actualiza la calidad y días de venta de los items, según reglas específicas.

        Reglas:
        - Items normales: calidad disminuye en 1 por día
        - Aged Brie: calidad aumenta con el tiempo
        - Sulfuras: item legendario, no cambia
        - Backstage passes: calidad aumenta, pero cae a 0 después del concierto
        - La calidad nunca es negativa ni mayor a MAX_QUALITY
        """
        for item in self.items:
            self._update_single_item(item)

    def _update_single_item(self, item: Item) -> None:
        """
        Actualiza la calidad y días de venta de un item específico.
        Args:
            item (Item): Item a actualizar.
        """
        match item.name:
            case name if name == SULFURAS:
                return
            case name if name == AGED_BRIE:
                self._update_aged_brie(item)
            case name if name == BACKSTAGE_PASSES:
                self._update_backstage_passes(item)
            case _:
                self._update_normal_items(item)

    def _update_normal_items(self, item: Item) -> None:
        self._decrease_quality_safe(item)
        self._decrease_sell_in(item)
        if item.sell_in < MIN_SELL_IN:
            self._decrease_quality_safe(item)

    def _update_backstage_passes(self, item: Item) -> None:
        self._increase_backstage_passes(item)
        self._decrease_sell_in(item)
        if item.sell_in < MIN_SELL_IN:
            item.quality = BACKSTAGE_EXPIRED_QUALITY

    def _update_aged_brie(self, item: Item) -> None:
        """
        Actualiza Aged Brie que mejora con el tiempo.
        - Aumenta +1 por día
        - Aumenta +2 después de la fecha de venta
        """
        self._increase_quality_safe(item)
        self._decrease_sell_in(item)
        if item.sell_in < MIN_SELL_IN:
            self._increase_quality_safe(item)

    def _increase_backstage_passes(self, item: Item) -> None:
        """
        Aumenta la calidad según los días restantes para el concierto.
        - Más de 10 días: +1 de calidad
        - 10-6 días: +2 de calidad
        - 5 o menos días: +3 de calidad
        Args:
            item (Item): Backstage pass a actualizar.
        """

        if item.sell_in < BACKSTAGE_SECOND_THRESHOLD:
            increment = BACKSTAGE_NEAR_INCREMENT
        elif item.sell_in < BACKSTAGE_FIRST_THRESHOLD:
            increment = BACKSTAGE_MEDIUM_INCREMENT
        else:
            increment = BACKSTAGE_FAR_INCREMENT

        # aplicar el incremento de calidad respetando el límite maximo de 50
        self._increase_quality_safe(item, increment)
