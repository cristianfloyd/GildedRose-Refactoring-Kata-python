# CASO 1: Sulfuras (legendario)
- NO cambia quality
- NO cambia sell_in
- Return temprano

# CASO 2: Aged Brie
- AUMENTA quality (+1 por día)
- Si sell_in < 0: AUMENTA más (+1 adicional)
- Quality MAX = 50

# CASO 3: Backstage Passes
- AUMENTA quality según días restantes:
  - sell_in > 10: +1
  - sell_in 6-10: +2
  - sell_in 1-5: +3
  - sell_in < 0: quality = 0
- Quality MAX = 50

# CASO 4: Items Normales
- DISMINUYE quality (-1 por día)
- Si sell_in < 0: DISMINUYE doble (-1 adicional)
- Quality MIN = 0
