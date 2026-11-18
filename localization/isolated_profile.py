"""Prepare explicitly isolated test profiles for copied games."""
import json
import os
from pathlib import Path
import plistlib
import pwd
import re

import dialogue_locale as dl

GLOBAL_REL = Path('Contents/Resources/Data/globalgamemanagers')
PLIST_REL = Path('Contents/Info.plist')
GLOBAL_HASH = '2f3813fddc22b6c6285099f173b922d782e2f06d659482d9373849e3bbb9794b'
PLIST_HASH = 'b976291899923ee4de4714f8d5ac8a684ca90f641466ff5a19af140888777394'
ORIGINAL_BUNDLE = 'com.Unity-Technologies.com.unity.template.urp-blank'
ORIGINAL_COMPANY = 'Gator Dragon Games'
ORIGINAL_PRODUCT = 'DragNWash'
TEST_COMPANY = 'Codex Test Sandbox'
WINDOWS_GAMEPLAY_PRODUCT = 'ProbeW8P1'


def identity(code, home=None):
    if not isinstance(code, str) or not re.fullmatch(r'[A-Z0-9]{4}', code):
        raise ValueError('test profile must be exactly four uppercase ASCII letters or digits')
    product = 'Probe' + code
    bundle = 'com.codex.test.dragnwash.probe' + code.lower()
    homes = {Path(home)} if home is not None else {Path.home(), Path(pwd.getpwuid(os.getuid()).pw_dir)}
    paths = []
    for root in homes:
        paths.extend([root / 'Library/Application Support' / bundle,
                      root / 'Library/Application Support' / TEST_COMPANY / product,
                      root / 'Library/Preferences' / (bundle + '.plist'),
                      root / 'Library/Preferences' / ('unity.' + TEST_COMPANY + '.' + product + '.plist')])
    if any(p.exists() or p.is_symlink() for p in paths):
        raise FileExistsError('test profile data or preferences already exist; choose a fresh code')
    return {'code': code, 'bundle': bundle, 'company': TEST_COMPANY, 'product': product}


def _current_pins(source, qa_profile, *, verify_all):
    from current_build import Build, relative_path
    root = Path(__file__).resolve().parents[1]
    qa = json.loads(Path(qa_profile).read_text(), object_pairs_hook=dl.unique_object)
    if qa.get('schemaVersion') != 1:
        raise ValueError('unsupported current-build QA profile')
    reference = root / relative_path(qa['dataProfile'])
    if dl.sha(reference.read_bytes()) != qa['dataProfileSha256']:
        raise ValueError('QA source build profile changed')
    build = Build(Path(source) / GLOBAL_REL.parent, reference)
    if build.profile['platform'] != 'macos':
        raise ValueError('expected a macOS QA build profile')
    if verify_all:
        build.verify()
    build.read('globalgamemanagers')
    return build.profile['files']['globalgamemanagers']['sha256'], qa['infoPlistSha256']


def prepare(source, code, home=None, *, qa_profile=None):
    import UnityPy
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    profile = identity(code, home)
    source = Path(source)
    global_file, plist_file = source / GLOBAL_REL, source / PLIST_REL
    original_global, original_plist = global_file.read_bytes(), plist_file.read_bytes()
    pins = _current_pins(source, qa_profile, verify_all=True) if qa_profile else (GLOBAL_HASH, PLIST_HASH)
    if dl.sha(original_global) != pins[0] or dl.sha(original_plist) != pins[1]:
        raise ValueError('unsupported test-profile source game')
    info = plistlib.loads(original_plist)
    if info.get('CFBundleIdentifier') != ORIGINAL_BUNDLE:
        raise ValueError('unexpected original bundle identifier')
    info['CFBundleIdentifier'] = profile['bundle']
    plist_bytes = plistlib.dumps(info, fmt=plistlib.FMT_XML, sort_keys=True)
    if plistlib.loads(plist_bytes) != info:
        raise ValueError('test profile plist failed round-trip')
    global_bytes, before, raw = _prepare_global(str(global_file), profile)
    return profile, global_bytes, plist_bytes, before, raw


def _prepare_global(source, profile):
    import UnityPy
    env = UnityPy.load(source)
    objects = {(o.path_id, o.type.name): o for o in env.objects}
    if len(objects) != len(env.objects) or (1, 'PlayerSettings') not in objects:
        raise ValueError('unexpected test-profile player settings inventory')
    before = {key: obj.get_raw_data() for key, obj in objects.items()}
    player = objects[(1, 'PlayerSettings')]
    read = player.read(check_read=False)
    if read.companyName != ORIGINAL_COMPANY or read.productName != ORIGINAL_PRODUCT:
        raise ValueError('unexpected test-profile source identity')
    raw = before[(1, 'PlayerSettings')]
    for old, new in ((ORIGINAL_COMPANY, profile['company']), (ORIGINAL_PRODUCT, profile['product'])):
        old_bytes, new_bytes = dl.write_string(old), dl.write_string(new)
        if len(old_bytes) != len(new_bytes) or raw.count(old_bytes) != 1:
            raise ValueError('ambiguous test-profile string encoding')
        raw = raw.replace(old_bytes, new_bytes, 1)
    player.set_raw_data(raw)
    return env.file.save(), before, raw


def _verify_global(source, profile, before, player_raw):
    import UnityPy
    env = UnityPy.load(source)
    after = {(o.path_id, o.type.name): o for o in env.objects}
    if len(after) != len(env.objects) or before.keys() != after.keys():
        raise ValueError('test-profile object inventory changed')
    for key, raw in before.items():
        expected = player_raw if key == (1, 'PlayerSettings') else raw
        if after[key].get_raw_data() != expected:
            raise ValueError(f'test-profile object differs: {key}')
    player = after[(1, 'PlayerSettings')].read(check_read=False)
    if player.companyName != profile['company'] or player.productName != profile['product']:
        raise ValueError('test-profile player identity read-back failed')


def prepare_windows_gameplay(source_data, *, build_profile=None, code=None):
    """Return verified settings bytes for the disposable Windows gameplay probe."""
    import UnityPy
    from compare_yarn_versions import BUILDS
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    source = (Path(source_data) / 'globalgamemanagers').read_bytes()
    expected = BUILDS['windows']['globalSha256']
    profile = {'company': TEST_COMPANY, 'product': WINDOWS_GAMEPLAY_PRODUCT}
    if build_profile is not None:
        from current_build import Build
        current = Build(source_data, build_profile)
        if current.profile['platform'] != 'windows' or code is None:
            raise ValueError('current Windows QA requires its build profile and a fresh code')
        current.verify()
        expected = current.profile['files']['globalgamemanagers']['sha256']
        profile = identity(code)
    elif code is not None:
        raise ValueError('a current Windows QA code requires a pinned build profile')
    if dl.sha(source) != expected:
        raise ValueError('unsupported Windows test-profile source game')
    result, before, player_raw = _prepare_global(source, profile)
    _verify_global(result, profile, before, player_raw)
    return result


def apply(destination, prepared, *, qa_profile=None):
    profile, global_bytes, plist_bytes, before, player_raw = prepared
    destination = Path(destination)
    target = destination / GLOBAL_REL
    plist = destination / PLIST_REL
    for path in (target, plist):
        if path.is_symlink() or not path.is_file() or destination.resolve() not in path.resolve().parents:
            raise ValueError('unsafe test-profile destination')
    pins = _current_pins(destination, qa_profile, verify_all=False) if qa_profile else (GLOBAL_HASH, PLIST_HASH)
    if dl.sha(target.read_bytes()) != pins[0] or dl.sha(plist.read_bytes()) != pins[1]:
        raise ValueError('copied test-profile source changed')
    # Recheck before mutation in case another process claimed the identity.
    identity(profile['code'])
    tmp = target.with_name('globalgamemanagers.test-profile.tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(global_bytes)
        _verify_global(str(tmp), profile, before, player_raw)
        os.replace(tmp, target)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    plist_tmp = plist.with_name('Info.test-profile.tmp')
    fd = os.open(plist_tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(plist_bytes)
        if plistlib.loads(plist_tmp.read_bytes()).get('CFBundleIdentifier') != profile['bundle']:
            raise ValueError('test-profile bundle identity read-back failed')
        os.replace(plist_tmp, plist)
    except BaseException:
        plist_tmp.unlink(missing_ok=True)
        raise
    marker = destination / 'Contents/Resources/vn-test-profile.json'
    with marker.open('x', encoding='utf-8') as f:
        json.dump({'schema': 1, **profile, 'testOnly': True}, f, ensure_ascii=False)
        f.write('\n')
    return profile
