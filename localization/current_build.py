"""Source-pinned asset edits for the reorganized 317a98f game build.

The historical builders remain available for exact release restoration. This
adapter edits the current objects in place in a separate output asset; it never
copies a historical scene or changes unrelated current game objects.
"""
from copy import deepcopy
import hashlib
from importlib.metadata import version
import json
from pathlib import Path, PurePosixPath
import struct

import UnityPy
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator

import dialogue_locale as dialogue
import settings_locale as settings
import speaker_contrast


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def relative_path(value):
    path = PurePosixPath(value)
    if (not value or not path.parts or path.is_absolute() or str(path) != value or
            any(part in ('', '.', '..') for part in path.parts) or '\\' in value or ':' in value):
        raise ValueError(f'Unsafe build input path: {value}')
    return path


def replace_checked(tree, field, expected, replacement):
    """Apply an explicitly bound leaf edit while preserving neighboring state."""
    if not field or not isinstance(expected, str) or not isinstance(replacement, str):
        raise ValueError('Expected a string edit with an explicit field path')
    node = tree
    for part in field[:-1]:
        node = node[part]
    if node[field[-1]] != expected:
        raise ValueError(f'Source value changed at {field!r}')
    if '\0' in replacement or not replacement.strip():
        raise ValueError('Replacement must contain text without NUL')
    node[field[-1]] = replacement


class Build:
    def __init__(self, data, profile):
        self.data = Path(data).resolve(strict=True)
        self.profile = json.loads(Path(profile).read_text(), object_pairs_hook=dialogue.unique_object)
        if (type(self.profile['schemaVersion']) is not int or self.profile['schemaVersion'] != 1
                or self.profile['platform'] not in ('windows', 'macos')
                or not self.profile['files'] or UnityPy.__version__ != '1.25.4'):
            raise ValueError('Unsupported build profile or UnityPy version')
        for name in self.profile['files']:
            relative_path(name)
        self.generator = None
        self.schemas = {}
        env = UnityPy.load(self.read('globalgamemanagers.assets'))
        self.scripts = {o.path_id: o.read() for o in env.objects if o.type.name == 'MonoScript'}

    def read(self, name):
        relative_path(name)
        expected = self.profile['files'][name]
        path = self.data / name
        if path.is_symlink() or not path.resolve(strict=True).is_relative_to(self.data):
            raise ValueError(f'Build input is not a regular local file: {name}')
        raw = path.read_bytes()
        if len(raw) != expected['size'] or digest(raw) != expected['sha256']:
            raise ValueError(f'Build input fingerprint mismatch: {name}')
        return raw

    def verify(self):
        paths = list(self.data.rglob('*'))
        if any(path.is_symlink() for path in paths):
            raise ValueError('Unexpected link in the pinned game Data directory')
        actual = {path.relative_to(self.data).as_posix() for path in paths if path.is_file()}
        if actual != self.profile['files'].keys():
            raise ValueError('Game Data file inventory differs from the pinned clean build')
        for name in self.profile['files']:
            self.read(name)

    def script(self, obj):
        head = obj.parse_monobehaviour_head()
        ref = head.m_Script
        external = obj.assets_file.externals[ref.m_FileID - 1] if ref.m_FileID > 0 else None
        if (external is None or PurePosixPath(external.path.replace('\\', '/')).name.lower()
                != 'globalgamemanagers.assets' or ref.m_PathID not in self.scripts):
            raise ValueError(f'Unresolved script for object {obj.path_id}')
        return head, self.scripts[ref.m_PathID]

    def schema(self, obj):
        if self.generator is None:
            if version('TypeTreeGeneratorAPI') != '0.0.10':
                raise ValueError('TypeTreeGeneratorAPI 0.0.10 is required')
            self.generator = TypeTreeGenerator(self.profile['unityVersion'])
            for name in sorted(self.profile['files']):
                if name.startswith('Managed/') and name.endswith('.dll') and not Path(name).name.startswith('Yarn.'):
                    self.generator.load_dll(self.read(name))
        _, _, nodes = settings.nodes_for(obj, self.generator, self.schemas)
        raw = obj.get_raw_data()
        tree = obj.read_typetree(nodes=nodes, check_read=True)
        if obj.save_typetree(tree, nodes=nodes) != raw:
            raise ValueError(f'Type schema failed exact no-op round trip: {obj.path_id}')
        return tree, nodes

    def asset(self, name):
        return Asset(self, name)


class Asset:
    def __init__(self, build, name):
        self.build, self.name = build, name
        self.env = UnityPy.load(build.read(name))
        self.env.path = str(build.data)
        self.objects = {obj.path_id: obj for obj in self.env.objects}
        if len(self.objects) != len(self.env.objects):
            raise ValueError('Duplicate serialized object IDs')
        self.original = {key: obj.get_raw_data() for key, obj in self.objects.items()}
        self.changed = {}

    def text_bindings(self):
        transforms, owners = {}, {}
        for obj in self.objects.values():
            if obj.type.name not in ('Transform', 'RectTransform'):
                continue
            item = obj.read(check_read=False)
            if item.m_GameObject.m_FileID or item.m_Father.m_FileID:
                raise ValueError('External transform reference')
            game = item.m_GameObject.m_PathID
            if game in owners:
                raise ValueError('Ambiguous transform ownership')
            owners[game] = obj.path_id
            transforms[obj.path_id] = (game, item.m_Father.m_PathID)
        result, paths = {}, set()
        for obj in self.objects.values():
            if obj.type.name != 'MonoBehaviour':
                continue
            head, script = self.build.script(obj)
            if script.m_ClassName != 'TextMeshProUGUI':
                continue
            owner = head.m_GameObject
            if owner.m_FileID or owner.m_PathID not in owners:
                raise ValueError('Unresolved TMP owner')
            chain, seen, current = [], set(), owners[owner.m_PathID]
            while current:
                if current in seen or current not in transforms:
                    raise ValueError('Cyclic or missing TMP ancestry')
                seen.add(current)
                game, current = transforms[current]
                item = self.objects[game]
                if item.type.name != 'GameObject':
                    raise ValueError('Invalid TMP game object')
                chain.append(item.read().m_Name)
            path = tuple(reversed(chain))
            if path in paths:
                raise ValueError(f'Ambiguous TMP ancestry: {path!r}')
            paths.add(path)
            text, end = dialogue.read_string(self.original[obj.path_id], 88)
            if self.original[obj.path_id][88:end] != dialogue.write_string(text):
                raise ValueError('TMP string failed no-op round trip')
            result[obj.path_id] = {'hierarchy': path, 'source': text}
        return result

    def set(self, obj, raw):
        if obj.path_id in self.changed:
            raise ValueError(f'Overlapping object edits: {obj.path_id}')
        obj.set_raw_data(raw)
        self.changed[obj.path_id] = raw

    def text(self, path_id, source, target):
        obj = self.objects[path_id]
        _, script = self.build.script(obj)
        if script.m_ClassName != 'TextMeshProUGUI':
            raise ValueError(f'Expected a TMP text object: {path_id}')
        raw = self.original[path_id]
        actual, end = dialogue.read_string(raw, 88)
        if actual != source or raw[88:end] != dialogue.write_string(actual):
            raise ValueError(f'TMP source text changed: {path_id}')
        if not isinstance(target, str) or not target.strip() or '\0' in target:
            raise ValueError('TMP target must be explicit nonempty text')
        self.set(obj, raw[:88] + dialogue.write_string(target) + raw[end:])

    def setting(self, path_id, name, edits):
        obj = self.objects[path_id]
        head, script = self.build.script(obj)
        if head.m_Name != name or not script.m_ClassName.startswith('Setting'):
            raise ValueError(f'Setting identity changed: {path_id}')
        tree, nodes = self.build.schema(obj)
        modified = deepcopy(tree)
        for field, source, target in edits:
            # Only the unbound visible backup strings may be translated.
            if (field not in (['label', 'backupString'],) and not
                    (len(field) == 3 and field[0] == 'dropdownOptions' and
                     type(field[1]) is int and field[2] == 'backupString')):
                raise ValueError(f'Protected setting field: {field!r}')
            value = tree['label'] if field[0] == 'label' else tree['dropdownOptions'][field[1]]
            settings.ensure_unbound(value, f'{self.name}#{path_id}')
            replace_checked(modified, field, source, target)
        self.set(obj, obj.save_typetree(modified, nodes=nodes))

    def speaker_colour(self, path_id):
        obj = self.objects[path_id]
        _, script = self.build.script(obj)
        raw = self.original[path_id]
        text, _ = dialogue.read_string(raw, 88)
        start = speaker_contrast.COLOR_OFFSET
        end = start + len(speaker_contrast.WHITE)
        if (script.m_ClassName != 'TextMeshProUGUI' or text != 'Character Name'
                or raw[start:end] != speaker_contrast.WHITE):
            raise ValueError('Current speaker-label colour binding changed')
        self.set(obj, raw[:start] + speaker_contrast.BLACK + raw[end:])

    def yarn(self, path_id, translations):
        obj = self.objects[path_id]
        _, script = self.build.script(obj)
        if script.m_ClassName != 'Localization':
            raise ValueError('Expected Yarn localization object')
        raw = self.original[path_id]
        keys, values, extras = dialogue.parse(raw)
        if dialogue.encode(raw, keys, values, extras) != raw:
            raise ValueError('Yarn table failed exact no-op round trip')
        if translations.keys() - set(keys):
            raise ValueError('Unknown Yarn line ID')
        positions = {key: index for index, key in enumerate(keys)}
        for key, item in translations.items():
            source, target = item
            if (values[positions[key]] != source or not isinstance(target, str) or not target.strip()
                    or '\0' in target):
                raise ValueError(f'Yarn source/target mismatch: {key}')
        self.set(obj, dialogue.encode(raw, keys,
                    [translations[key][1] if key in translations else value for key, value in zip(keys, values)], extras))

    def program(self, path_id, expected_sha, program):
        obj = self.objects[path_id]
        _, script = self.build.script(obj)
        if script.m_ClassName != 'YarnProject':
            raise ValueError('Expected Yarn project object')
        raw = self.original[path_id]
        size = struct.unpack_from('<I', raw, 40)[0]
        end = 44 + size
        if digest(raw[44:end]) != expected_sha or raw[end:end + (-end % 4)] != bytes(-end % 4):
            raise ValueError('Yarn program or alignment changed')
        self.set(obj, raw[:40] + struct.pack('<I', len(program)) + program + bytes(-len(program) % 4)
                 + raw[end + (-end % 4):])

    def save(self, output):
        output = Path(output)
        if output.resolve().is_relative_to(self.build.data):
            raise ValueError('Output must be outside the original game Data directory')
        raw = self.env.file.save()
        checked = UnityPy.load(raw)
        objects = {obj.path_id: obj.get_raw_data() for obj in checked.objects}
        expected = self.original | self.changed
        if len(objects) != len(checked.objects) or objects != expected:
            raise ValueError('Serialized object inventory or preservation check failed')
        with output.open('xb') as stream:
            stream.write(raw)
        if digest(output.read_bytes()) != digest(raw):
            raise ValueError('Saved asset fingerprint differs from verified bytes')
        return {'sourceSha256': self.build.profile['files'][self.name]['sha256'],
                'outputSha256': digest(raw), 'changedObjects': sorted(self.changed),
                'preservedObjects': len(self.original) - len(self.changed)}
