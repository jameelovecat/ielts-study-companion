import importlib.util
import json
from datetime import date
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('study', Path(__file__).resolve().parents[1] / 'scripts/study.py')
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


class StudyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'private'
        study.initialize(self.root)

    def seed(self, **changes):
        item = dict(id='e1', expression='keep an open mind', meaning='保持开放心态',
                    level=0, due='2026-11-01', source='fictional', custom='preserve')
        item.update(changes)
        study.write_json(self.root / '表达本.json', {'entries': [item], 'reviews': [], 'custom': 42})

    def test_init_preserves_user_data_and_config(self):
        path = self.root / '学习档案.md'
        path.write_text('my existing profile')
        config = self.root / 'config.json'
        config.write_text('{"custom": true}')
        study.initialize(self.root)
        self.assertEqual(path.read_text(), 'my existing profile')
        self.assertEqual(json.loads(config.read_text()), {'custom': True})

    def test_index_deduplicates_and_skips_hidden_and_symlinks(self):
        materials = self.root / 'materials'
        (materials / 'test.pdf').write_bytes(b'fixture')
        (materials / '.hidden.pdf').write_bytes(b'hidden')
        (materials / 'unrelated.env').write_text('secret')
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        (outside / 'secret.pdf').write_bytes(b'private')
        (materials / 'link').symlink_to(outside, target_is_directory=True)
        (materials / 'linked.pdf').symlink_to(outside / 'secret.pdf')
        config = study.read_json(self.root / 'config.json')
        config['material_roots'] = ['materials', str(materials), 'missing']
        study.write_json(self.root / 'config.json', config)
        result = study.index_materials(self.root)
        self.assertEqual(result['indexed'], 1)
        self.assertEqual(len(result['missing_roots']), 1)

    def test_due_filters_mastered_and_does_not_reveal_answer(self):
        self.seed()
        due = study.due_expressions(self.root, date(2026, 11, 1))
        self.assertEqual(len(due), 1)
        self.assertNotIn('expression', due[0])
        self.assertEqual(study.due_expressions(self.root, date(2026, 10, 31)), [])
        self.seed(level=6, due=None)
        self.assertEqual(study.due_expressions(self.root, date(2027, 1, 1)), [])

    def test_correct_and_duplicate_review(self):
        self.seed()
        result = study.review_expression(self.root, 'e1', True, date(2026, 11, 1))
        self.assertEqual((result['level'], result['due']), (1, '2026-11-03'))
        before = (self.root / '表达本.json').read_bytes()
        duplicate = study.review_expression(self.root, 'e1', True, date(2026, 11, 1))
        self.assertEqual(duplicate['status'], 'already_reviewed_today')
        self.assertEqual(before, (self.root / '表达本.json').read_bytes())
        data = study.read_json(self.root / '表达本.json')
        self.assertEqual(data['entries'][0]['custom'], 'preserve')
        self.assertEqual(data['custom'], 42)

    def test_wrong_resets_and_mastery_can_reenter(self):
        self.seed(level=6, due=None)
        result = study.review_expression(self.root, 'e1', False, date(2026, 11, 1))
        self.assertEqual((result['level'], result['due']), (0, '2026-11-02'))

    def test_last_level_correct_marks_mastered(self):
        self.seed(level=5)
        result = study.review_expression(self.root, 'e1', True, date(2026, 11, 1))
        self.assertEqual(result['level'], 6)
        self.assertIsNone(result['due'])

    def test_invalid_id_and_duplicate_ids_do_not_change_file(self):
        self.seed()
        before = (self.root / '表达本.json').read_bytes()
        with self.assertRaises(ValueError):
            study.review_expression(self.root, 'missing', True, date(2026, 11, 1))
        self.assertEqual(before, (self.root / '表达本.json').read_bytes())
        data = study.read_json(self.root / '表达本.json')
        data['entries'].append(data['entries'][0].copy())
        study.write_json(self.root / '表达本.json', data)
        with self.assertRaises(ValueError):
            study.due_expressions(self.root, date(2026, 11, 1))

    def test_same_day_failure_overrides_success(self):
        self.seed()
        study.review_expression(self.root, 'e1', True, date(2026, 11, 1))
        result = study.review_expression(self.root, 'e1', False, date(2026, 11, 1))
        self.assertEqual((result['level'], result['due']), (0, '2026-11-02'))
        result = study.review_expression(self.root, 'e1', True, date(2026, 11, 1))
        self.assertEqual(result['level'], 0)

    def test_init_creates_plan_diagnostic_course_and_privacy_files(self):
        for name in ('备考计划.md', '诊断记录.md', '分项学习/学习记录.md', '.gitignore'):
            self.assertTrue((self.root / name).is_file(), name)
        self.assertEqual((self.root / '.gitignore').read_text(), '*\n')

    def test_backdated_review_rejected(self):
        self.seed(last_reviewed='2026-11-02')
        with self.assertRaises(ValueError):
            study.review_expression(self.root, 'e1', True, date(2026, 11, 1))


if __name__ == '__main__':
    unittest.main()
