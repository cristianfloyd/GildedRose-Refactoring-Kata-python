# tests/unit/test_validation.py
import pytest

from gilded_rose import GildedRose
from gilded_rose.models import Item


class TestValidation:
    """Tests para validación de entrada."""

    def test_empty_items_raises_error(self):
        """Verificar que lista vacía lanza ValueError."""
        with pytest.raises(ValueError, match="no pueden ser vacíos"):
            GildedRose([])

    def test_invalid_items_raises_typeerror(self):
        """Verificar que items no-Item lanzan TypeError."""
        with pytest.raises(TypeError, match="deben ser instancias de Item"):
            GildedRose([Item("Valid", 10, 10), "invalid"])  # String no es Item
