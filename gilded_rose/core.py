"""Clase principal GildedRose."""

from collections.abc import Callable

from gilded_rose.constants import (
    AGED_BRIE,
    AGED_BRIE_EXPIRED_INCREMENT,
    AGED_BRIE_INCREMENT,
    BACKSTAGE_EXPIRED_QUALITY,
    BACKSTAGE_FAR_INCREMENT,
    BACKSTAGE_FIRST_THRESHOLD,
    BACKSTAGE_MEDIUM_INCREMENT,
    BACKSTAGE_NEAR_INCREMENT,
    BACKSTAGE_PASSES,
    BACKSTAGE_SECOND_THRESHOLD,
    CONJURED_DAILY_DECREMENT,
    CONJURED_EXPIRED_DECREMENT,
    CONJURED_PREFIX,
    MAX_QUALITY,
    MIN_QUALITY,
    MIN_SELL_IN,
    NORMAL_DAILY_DECREMENT,
    NORMAL_EXPIRED_DECREMENT,
    NORMAL_SELL_IN_DECREMENT,
    SULFURAS,
)
from gilded_rose.models import Item


class GildedRose:
    """Sistema de gestion de inventario para la posada Gilded Rose.
    Actualiza la calidad y días de venta de los items, según reglas específicas.
    """

    def __init__(self, items: list[Item]) -> None:
        """Inicializa la lista de items para el sistema.

        Args:
            items (list): Lista de items a gestionar.

        """
        self._validate_items(items)
        self.items = items

    @staticmethod
    def _validate_items(items: list[Item]) -> None:
        """Valida que los items sean instancias de Item.

        Args:
            items (list): Lista de items a validar.

        """
        if not items:
            raise ValueError("Los items no pueden ser vacíos")
        if not all(isinstance(item, Item) for item in items):
            raise TypeError("Los items deben ser instancias de Item")

    @staticmethod
    def _decrease_quality_safe(item: Item, amount: int) -> None:
        """Disminuye la calidad de un item si no es el minimo.

        Args:
            item (Item): Item a disminuir.

        """
        item.quality = max(MIN_QUALITY, item.quality - amount)

    @staticmethod
    def _increase_quality_safe(item: Item, amount: int) -> None:
        """Aumenta la calidad de un item si no es el maximo.

        Args:
            item (Item): Item a aumentar.

        """
        item.quality = min(MAX_QUALITY, item.quality + amount)

    @staticmethod
    def _decrease_sell_in(item: Item) -> None:
        """Disminuye los días restantes para vender un item.

        Args:
            item (Item): Item a disminuir.

        """
        item.sell_in -= NORMAL_SELL_IN_DECREMENT

    @staticmethod
    def _is_conjured(item: Item) -> bool:
        """Verifica si un item es conjurado por su nombre.

        Args:
            item (Item): Item a verificar.

        """
        return item.name.lower().startswith(CONJURED_PREFIX)

    def update_quality(self) -> None:
        """Actualiza la calidad y días de venta de los items, según reglas específicas.

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
        """Actualiza la calidad y días de venta de un item específico.

        Args:
            item (Item): Item a actualizar.

        """
        match item.name:
            case _ if item.name == SULFURAS:
                return
            case _ if item.name == AGED_BRIE:
                self._update_aged_brie(item)
            case _ if item.name == BACKSTAGE_PASSES:
                self._update_backstage_passes(item)
            case _ if self._is_conjured(item):
                self._update_conjured_items(item)
            case _:
                self._update_normal_items(item)

    def _apply_standard_aging(
        self,
        item: Item,
        adjustment_method: Callable[[Item, int], None],
        daily_change: int,
        expired_change: int,
    ) -> None:
        """Aplica el patrón común de envejecimiento:
        - Ajuste diario -> Envejecer -> Ajuste por vencimiento.

        Args:
            item (Item): Item a actualizar.
            adjustment_method (Callable): Método para ajustar calidad (incrementar o disminuir).
            daily_change (int): Cantidad a ajustar diariamente.
            expired_change (int): Cantidad extra a ajustar si expiró.

        """
        adjustment_method(item, daily_change)
        self._decrease_sell_in(item)
        if item.sell_in < MIN_SELL_IN:
            adjustment_method(item, expired_change)

    def _update_normal_items(self, item: Item) -> None:
        """Actualiza items normales.
        - Disminuye la calidad en NORMAL_DAILY_DECREMENT por día
        - Disminuye la calidad en NORMAL_EXPIRED_DECREMENT adicional si el sell_in es menor a 0
        """
        self._apply_standard_aging(
            item,
            self._decrease_quality_safe,
            NORMAL_DAILY_DECREMENT,
            NORMAL_EXPIRED_DECREMENT,
        )

    def _update_backstage_passes(self, item: Item) -> None:
        """Actualiza Backstage passes.
        - Aumenta la calidad según los días restantes para el concierto
        - Disminuye la calidad a 0 si el sell_in es menor a 0
        """
        self._increase_backstage_passes(item)
        self._decrease_sell_in(item)
        if item.sell_in < MIN_SELL_IN:
            item.quality = BACKSTAGE_EXPIRED_QUALITY

    def _update_aged_brie(self, item: Item) -> None:
        """Actualiza Aged Brie que mejora con el tiempo.
        - Aumenta la calidad en Aged_BRIE_INCREMENT por día
        - Aumenta la calidad en Aged_BRIE_EXPIRED_INCREMENT después de la fecha de venta

        """
        self._apply_standard_aging(
            item,
            self._increase_quality_safe,
            AGED_BRIE_INCREMENT,
            AGED_BRIE_EXPIRED_INCREMENT,
        )

    def _update_conjured_items(self, item: Item) -> None:
        """Actualiza items conjurados.
        - Disminuye la calidad en CONJURED_DAILY_DECREMENT por día
        - Disminuye la calidad en CONJURED_EXPIRED_DECREMENT adicional si el sell_in es menor a 0
        """
        self._apply_standard_aging(
            item,
            self._decrease_quality_safe,
            CONJURED_DAILY_DECREMENT,
            CONJURED_EXPIRED_DECREMENT,
        )

    def _increase_backstage_passes(self, item: Item) -> None:
        """Aumenta la calidad según los días restantes para el concierto.
        - Más de BACKSTAGE_FIRST_THRESHOLD días: +BACKSTAGE_FAR_INCREMENT de calidad
        - Entre BACKSTAGE_FIRST_THRESHOLD y BACKSTAGE_SECOND_THRESHOLD días:
          +BACKSTAGE_MEDIUM_INCREMENT de calidad
        - BACKSTAGE_SECOND_THRESHOLD o menos días: +BACKSTAGE_NEAR_INCREMENT de calidad
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
