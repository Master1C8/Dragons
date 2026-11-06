import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('dialogue_locale', Path(__file__).with_name('dialogue_locale.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class LocaleFileTests(unittest.TestCase):
    def setUp(self):
        self.keys = ['line:12345678']
        self.values = ['Ryan: <i>Hello {0}</i>']
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'locale.json'
        self.doc = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': module.OBJECT_HASH,
                    'lines': {self.keys[0]: {'source': self.values[0], 'text': 'Ryan: <i>Test {0}</i>'}}}

    def tearDown(self):
        self.tmp.cleanup()

    def read(self):
        self.path.write_text(json.dumps(self.doc, ensure_ascii=False), encoding='utf-8')
        return module.read_locale(self.path, self.keys, self.values)

    def test_valid_line_and_placeholders(self):
        self.assertEqual(self.read(), ('ru', {self.keys[0]: 'Ryan: <i>Test {0}</i>'}))

    def test_rejects_changed_source_unknown_id_and_english(self):
        self.doc['lines'][self.keys[0]]['source'] = 'outdated'
        with self.assertRaisesRegex(ValueError, 'source mismatch'):
            self.read()
        self.doc['lines'] = {'line:ffffffff': {'source': 'x', 'text': 'y'}}
        with self.assertRaisesRegex(ValueError, 'unknown line IDs'):
            self.read()
        self.doc['locale'] = 'en'
        with self.assertRaisesRegex(ValueError, 'non-English'):
            self.read()

    def test_rejects_missing_placeholder_and_changed_prefix(self):
        self.doc['lines'][self.keys[0]]['text'] = 'Ryan: <i>Test</i>'
        with self.assertRaisesRegex(ValueError, 'markup or placeholders'):
            self.read()
        self.doc['lines'][self.keys[0]]['text'] = 'Someone: <i>Test {0}</i>'
        with self.assertRaisesRegex(ValueError, 'label/command'):
            self.read()

    def test_duplicate_keys_are_rejected(self):
        self.path.write_text('{"schema":1,"schema":1}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'duplicate JSON key'):
            module.read_locale(self.path, self.keys, self.values)

    def test_title_directive_remains_exact(self):
        self.values = ['title: RyanDate_OutroDone']
        self.doc['lines'][self.keys[0]] = {'source': self.values[0], 'text': 'title: AnotherNode'}
        with self.assertRaisesRegex(ValueError, 'title directive'):
            self.read()
        self.doc['lines'][self.keys[0]]['text'] = self.values[0]
        self.read()

    def test_rejects_unconfigured_locale(self):
        self.doc['locale'] = 'zz'
        with self.assertRaisesRegex(ValueError, 'supported non-English'):
            self.read()

    def test_rejects_boolean_schema(self):
        self.doc['schema'] = True
        with self.assertRaisesRegex(ValueError, 'schema'):
            self.read()


if __name__ == '__main__':
    unittest.main()
