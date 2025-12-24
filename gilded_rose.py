# Constants
MAX_QUALITY = 50
MIN_QUALITY = 0
AGED_BRIE = "Aged Brie"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"


class Item:
    """DO NOT MODIFY - This class belongs to the goblin in the corner."""

    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)  # noqa: UP031


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
    def _decrease_quality_safe(item: Item) -> None:
        """
        Disminuye la calidad de un item si no es el minimo.
        Args:
            item (Item): Item a disminuir.
        """
        if item.quality > MIN_QUALITY:
            item.quality = item.quality - 1

    @staticmethod
    def _increase_quality_safe(item: Item) -> None:
        """
        Aumenta la calidad de un item si no es el maximo.
        Args:
            item (Item): Item a aumentar.
        """
        if item.quality < MAX_QUALITY:
            item.quality = item.quality + 1

    @staticmethod
    def _decrease_sell_in(item: Item) -> None:
        item.sell_in = item.sell_in - 1

    def _update_backstage_passes(self, item: Item) -> None:
        """
        Actualiza el valor de los Backstage passes.
        Args:
            item (Item): Backstage pass a actualizar.
        """
        pass

    def _update_aged_brie(self, item: Item) -> None:
        """
        Actualiza el valor de Aged Brie.
        # - Quality MAX = 50
        Args:
            item (Item): Aged Brie a actualizar.
        """

        # - AUMENTA quality (+1 por día)
        self._increase_quality_safe(item)

        # - Si sell_in < 0: AUMENTA más (+1 adicional)
        if item.sell_in < 0:
            self._increase_quality_safe(item)

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
        # Sulfuras no cambia - Guard clause
        if item.name == SULFURAS:
            return

        # Aged Brie y Backstage passes tienen reglas especiales
        match item.name:
            case name if name == AGED_BRIE:
                self._increase_quality_safe(item)
            case name if name == BACKSTAGE_PASSES:
                # Increases quality based on remaining sell in
                self._handle_update_backstage_passes(item)
            case _:
                self._decrease_quality_safe(item)

        self._decrease_sell_in(item)  # ya no necesita el if != SULFURAS
        self._update_item_after_sell_date(item)

    def _handle_update_backstage_passes(self, item: Item) -> None:
        """
        Increases quality based on remaining sell in
        Args:
            item (Item): Backstage pass a actualizar.
        """
        self._increase_quality_safe(item)
        if item.sell_in < 11:
            self._increase_quality_safe(item)
        if item.sell_in < 6:
            self._increase_quality_safe(item)

    def _update_item_after_sell_date(self, item: Item) -> None:
        if item.sell_in < 0:
            # Adjusts quality based on item type after sell date
            match item.name:
                case name if name == AGED_BRIE:
                    self._increase_quality_safe(item)
                case name if name == BACKSTAGE_PASSES:
                    item.quality = 0
                case _:
                    self._decrease_quality_safe(item)
