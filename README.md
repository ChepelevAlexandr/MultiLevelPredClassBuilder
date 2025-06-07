# Multi-Level Predicate Class Builder (Python)

Python-���������� ��������� ��������� ��� ���������� ��������������� �������� ������� �� ����� ����������.

## ��������� �������

- `ml_builder.py`       � ����� ����� (main)
- `parser.py`           � ������ � ������� `classes_list.txt`, `classK.txt` � `scene.txt`
- `unifier.py`          � ������� ���������� `literal`-�� � ������� `literal`-��
- `utils.py`            � ����� ������� � ��������� (����������, ������)
- `subformula.py`       � ����� `Subformula`
- `level_finder.py`     � ���������� `extract_level`
- `selector.py`         � ���������� `select_and_register_predicates`
- `matcher.py`          � `find_all_matches` � `build_objects_at_level`
- `output_writer.py`    � ���������� `level*_objects.txt` � `final_descriptions.txt`

## ������

1. ��������� � ������ ������� �����:
   - `classes_list.txt` (������ ����� � `class1.txt`, `class2.txt`, �)
   - ������ `classK.txt` (�� ������: `P(x,a)&Q(a,b)&...`)
   - `scene.txt` (�� ������: `P(c,a)`, `Q(d,e)`, �)

2. ��������� (������ �������� `ml_pred_classes/`):

   ```bash
   python ml_builder.py classes_list.txt scene.txt
