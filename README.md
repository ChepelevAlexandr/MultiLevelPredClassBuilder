# Multi-Level Predicate Class Builder (Python)

Python-реализация алгоритма для построения многоуровневого описания классов на языке предикатов.

## Структура проекта

- `ml_builder.py`       — точка входа (main)
- `parser.py`           — чтение и парсинг `classes_list.txt`, `classK.txt` и `scene.txt`
- `unifier.py`          — функции унификации `literal`-ов и списков `literal`-ов
- `utils.py`            — общие утилиты и константы (комбинации, пороги)
- `subformula.py`       — класс `Subformula`
- `level_finder.py`     — реализация `extract_level`
- `selector.py`         — реализация `select_and_register_predicates`
- `matcher.py`          — `find_all_matches` и `build_objects_at_level`
- `output_writer.py`    — сохранение `level*_objects.txt` и `final_descriptions.txt`

## Запуск

1. Поместить в корень проекта файлы:
   - `classes_list.txt` (список путей к `class1.txt`, `class2.txt`, …)
   - Каждый `classK.txt` (по строке: `P(x,a)&Q(a,b)&...`)
   - `scene.txt` (по строке: `P(c,a)`, `Q(d,e)`, …)

2. Выполнить (внутри каталога `ml_pred_classes/`):

   ```bash
   python ml_builder.py classes_list.txt scene.txt
