# 🏛️ Gilded Rose Refactoring Kata - Python

> Refactorización profesional completa de código legacy aplicando técnicas modernas de desarrollo de software.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/pytest-8.0+-green.svg)](https://pytest.org/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://coverage.readthedocs.io/)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## 📋 Descripción

Este proyecto es una implementación completa del **Gilded Rose Refactoring Kata**, un ejercicio clásico de refactorización de código legacy. El objetivo es transformar código complejo y difícil de mantener en código limpio, profesional y bien probado, manteniendo 100% de funcionalidad.

### 🎯 Objetivos Alcanzados

- ✅ **Refactorización completa** de código legacy sin romper funcionalidad
- ✅ **100% de cobertura** de tests
- ✅ **Property-based testing** con Hypothesis
- ✅ **Mutation testing** configurado con mutmut
- ✅ Aplicación de **principios SOLID** y **Clean Code**
- ✅ **Patrones de diseño** avanzados (Template Method)
- ✅ **TDD** para nueva funcionalidad (Conjured items)
- ✅ Estructura profesional de paquete Python

## 🛠️ Tecnologías y Herramientas

### Core
- **Python 3.10+** - Lenguaje de programación
- **pytest 8.0+** - Framework de testing
- **pytest-cov** - Cobertura de código
- **hypothesis 6.0+** - Property-based testing
- **mutmut 2.0+** - Mutation testing
- **approvaltests** - Approval testing

### Calidad de Código
- **ruff** - Linter y formateador rápido
- **mypy** - Type checking (compatible con strict mode)
- **coverage** - Análisis de cobertura

### Estructura
- **Paquete Python** profesional (PEP 420)
- **Type hints** completos
- **Documentación** con docstrings

## 📊 Estado del Proyecto

### ✅ Completado (100%)

- [x] Fase 1: Refactoring Básico (Guard clauses, Extract methods, Pattern matching)
- [x] Fase 2: Refactoring Avanzado (Template Method Pattern, Type hints, Validación)
- [x] Fase 3: Implementación Conjured Items (TDD)
- [x] Fase 3.5: Reorganización de Estructura (Paquete Python)
- [x] Fase 5: Testing Avanzado (Property-based, Mutation testing, 100% cobertura)

### ⏸️ Opcional

- [ ] Fase 4: Strategy Pattern (YAGNI - No necesario para este tamaño de proyecto)

## 🏗️ Estructura del Proyecto

```
GildedRose-Python-Refactoring/
├── gilded_rose/              # 📦 Paquete Python principal
│   ├── __init__.py          # Exports públicos
│   ├── core.py              # Clase GildedRose
│   ├── models.py            # Clase Item
│   └── constants.py         # Constantes del sistema
│
├── tests/                    # ✅ Tests organizados
│   ├── unit/                # Tests unitarios
│   │   ├── test_gilded_rose.py
│   │   ├── test_gilded_rose_detailed.py
│   │   ├── test_conjured.py
│   │   ├── test_properties.py      # Property-based tests
│   │   └── test_validation.py
│   └── integration/         # Tests de integración
│       └── test_gilded_rose_approvals.py
│
├── docs/                     # 📚 Documentación
│   ├── casos_de_uso.md
│   └── GildedRoseRequirements_es.md
│
├── scripts/                  # 🔧 Scripts auxiliares
│   └── texttest_fixture.py
│
├── pyproject.toml           # Configuración del proyecto
├── requirements.txt         # Dependencias
├── Makefile                 # Comandos útiles
└── README.md               # Este archivo
```

## 🚀 Instalación y Uso

### Requisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd GildedRose-Python-Refactoring

# Crear entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar dependencias de desarrollo (opcional)
pip install -e ".[dev]"
```

### Ejecución

```bash
# Ejecutar tests
make test
# o
pytest -v

# Ver cobertura
make coverage
# o
pytest --cov=gilded_rose --cov-report=html --cov-report=term-missing

# Linting
make lint

# Formatear código
make format

# Ejecutar script de ejemplo
make run
# o
python scripts/texttest_fixture.py
```

## 🧪 Testing

### Tests Unitarios

```bash
# Todos los tests
pytest -v

# Tests específicos
pytest tests/unit/test_gilded_rose_detailed.py -v
pytest tests/unit/test_conjured.py -v
```

### Property-Based Testing

Los tests de propiedades verifican invariantes matemáticas que siempre deben cumplirse, usando Hypothesis para generar miles de casos automáticamente:

```bash
# Tests de propiedades
pytest tests/unit/test_properties.py -v

# Ver estadísticas de Hypothesis
pytest tests/unit/test_properties.py -v --hypothesis-show-statistics
```

**Ejemplo de property test**:
```python
@given(
    sell_in=st.integers(min_value=-100, max_value=100),
    quality=st.integers(min_value=0, max_value=50),
)
def test_quality_never_negative(sell_in, quality):
    """Property: Quality nunca puede ser negativa."""
    item = Item("Normal Item", sell_in, quality)
    gilded_rose = GildedRose([item])

    for _ in range(100):
        gilded_rose.update_quality()
        assert item.quality >= 0
```

### Mutation Testing

Verifica la calidad de los tests introduciendo cambios sutiles en el código:

```bash
# Ejecutar mutation testing (puede tardar varios minutos)
mutmut run

# Ver resultados
mutmut results

# Ver detalles de una mutación específica
mutmut show <id>
```

### Cobertura

**Cobertura actual: 100%** ✅

- `gilded_rose/__init__.py`: 100%
- `gilded_rose/constants.py`: 100%
- `gilded_rose/core.py`: 100%
- `gilded_rose/models.py`: 100%

## 📈 Métricas Finales

| Métrica | Antes ❌ | Después ✅ | Mejora |
|---------|----------|-----------|--------|
| Complejidad ciclomática | ~15 | 3 | 🔻 80% |
| Niveles de indentación | 4 | 1 | 🔻 75% |
| Líneas método principal | 35 | 12 | 🔻 66% |
| Números mágicos | 12+ | 0 | 🔻 100% |
| Cobertura | 98% | **100%** | ✅ |
| Tests | 2 básicos | **27 tests** | 🔼 1250% |
| Type hints | Parcial | 100% | ✅ |

### Estadísticas de Tests

- **27 tests totales** pasando
  - 17 tests unitarios tradicionales
  - 8 property-based tests (Hypothesis)
  - 2 tests de validación
- **100% cobertura** de código
- **Property-based testing** para invariantes
- **Mutation testing** configurado

## 🎓 Técnicas y Patrones Aplicados

### Refactoring Patterns

- ✅ **Extract Method** - Separación de responsabilidades
- ✅ **Guard Clauses** - Reducción de indentación
- ✅ **Replace Magic Number with Symbolic Constant** - Auto-documentación
- ✅ **Replace Conditional with Polymorphism** - Pattern matching

### Design Patterns

- ✅ **Template Method Pattern** - Reutilización mediante callbacks
- ✅ **Higher-Order Functions** - Callbacks para inversión de dependencia

### Principios

- ✅ **SOLID** - Single Responsibility, Open/Closed, Dependency Inversion
- ✅ **DRY** - Don't Repeat Yourself
- ✅ **Clean Code** - Nombres descriptivos, funciones pequeñas
- ✅ **Defensive Programming** - Validación de entrada

### Testing

- ✅ **TDD** - Test-Driven Development
- ✅ **Property-Based Testing** - Validación de invariantes
- ✅ **Mutation Testing** - Calidad de tests
- ✅ **Approval Testing** - Tests de regresión

## 🏆 Logros Destacados

1. **Transformación completa**: De código legacy a código profesional
2. **Cobertura 100%**: Todos los casos cubiertos
3. **Property-based testing**: Validación matemática de propiedades críticas
4. **Estructura escalable**: Fácil de extender y mantener
5. **Best practices**: Type hints, validación, tests exhaustivos

## 📝 Reglas de Negocio

El sistema gestiona diferentes tipos de items con reglas específicas:

- **Items normales**: Disminuyen calidad con el tiempo
- **Aged Brie**: Aumenta calidad con el tiempo (hasta 50)
- **Backstage Passes**: Aumenta calidad según días restantes (drops a 0 después)
- **Sulfuras**: Item legendario, nunca cambia
- **Conjured**: Disminuyen calidad al doble de velocidad

Ver `docs/GildedRoseRequirements_es.md` para detalles completos.

## 🤝 Contribuir

Este es un proyecto de aprendizaje/kata. Siéntete libre de:

- Hacer fork del proyecto
- Experimentar con diferentes técnicas de refactoring
- Agregar nuevos tipos de items
- Mejorar los tests

## 📚 Referencias

- [Kata Original - Emily Bache](https://github.com/emilybache/GildedRose-Refactoring-Kata)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [mutmut Documentation](https://mutmut.readthedocs.io/)
- [Refactoring Guru](https://refactoring.guru/)

## 📄 Licencia

Este proyecto es un ejercicio basado en el Gilded Rose Kata original.

## 👨‍💻 Autor

Proyecto desarrollado mostrando manejo de:
- Refactoring de código legacy
- Testing avanzado (property-based, mutation)
- Aplicación de principios SOLID y Clean Code
- Estructura profesional de proyectos Python

---

**Versión**: 1.0.0
**Estado**: ✅ Completado
**Última actualización**: 2025-12-25
