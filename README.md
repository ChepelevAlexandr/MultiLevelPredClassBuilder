# Multi-Level Predicate Class Builder (Python)

Python-реализаци€ алгоритма  осовской дл€ построени€ многоуровневого описани€ классов на €зыке предикатов.

## —труктура проекта

- `ml_builder.py`       Ч точка входа (main)
- `parser.py`           Ч чтение и парсинг `classes_list.txt`, `classK.txt` и `scene.txt`
- `unifier.py`          Ч функции унификации `literal`-ов и списков `literal`-ов
- `utils.py`            Ч общие утилиты и константы (комбинации, пороги)
- `subformula.py`       Ч класс `Subformula`
- `level_finder.py`     Ч реализаци€ `extract_level`
- `selector.py`         Ч реализаци€ `select_and_register_predicates`
- `matcher.py`          Ч `find_all_matches` и `build_objects_at_level`
- `output_writer.py`    Ч сохранение `level*_objects.txt` и `final_descriptions.txt`

## «апуск

1. ѕоместить в корень проекта файлы:
   - `classes_list.txt` (список путей к `class1.txt`, `class2.txt`, Е)
   -  аждый `classK.txt` (по строке: `P(x,a)&Q(a,b)&...`)
   - `scene.txt` (по строке: `P(c,a)`, `Q(d,e)`, Е)

2. ¬ыполнить (внутри каталога `ml_pred_classes/`):

   ```bash
   python ml_builder.py classes_list.txt scene.txt
