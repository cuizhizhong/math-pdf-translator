import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from install import SKILLS, install


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.bundle = self.base / 'release'
        self.dest = self.base / 'installed'
        files = {}
        for name in SKILLS:
            path = self.bundle / 'skills' / name / 'SKILL.md'
            path.parent.mkdir(parents=True)
            path.write_text(f'---\nname: {name}\n---\n', encoding='utf-8')
            files[path.relative_to(self.bundle).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        (self.bundle / 'manifest.json').write_text(json.dumps({'files': files}), encoding='utf-8')

    def test_fresh_install_copies_all_dependencies(self):
        install(self.bundle, self.dest)
        for name in SKILLS:
            self.assertEqual((self.dest / name / 'SKILL.md').read_bytes(), (self.bundle / 'skills' / name / 'SKILL.md').read_bytes())

    def test_dry_run_never_creates_destination(self):
        install(self.bundle, self.dest, dry_run=True)
        self.assertFalse(self.dest.exists())

    def test_conflict_is_detected_before_any_copy(self):
        existing = self.dest / SKILLS[-1]
        existing.mkdir(parents=True)
        (existing / 'SKILL.md').write_text('private host skill', encoding='utf-8')
        with self.assertRaises(FileExistsError):
            install(self.bundle, self.dest)
        self.assertEqual(list(self.dest.iterdir()), [existing])
        self.assertEqual((existing / 'SKILL.md').read_text(encoding='utf-8'), 'private host skill')

    def test_skip_existing_preserves_private_skill(self):
        install(self.bundle, self.dest)
        entry = self.dest / 'pdf' / 'SKILL.md'
        entry.write_text('host pdf policy', encoding='utf-8')
        install(self.bundle, self.dest, skip_existing=True)
        self.assertEqual(entry.read_text(encoding='utf-8'), 'host pdf policy')

    def test_skip_existing_rejects_non_skill_directory(self):
        (self.dest / 'pdf').mkdir(parents=True)
        with self.assertRaises(FileExistsError):
            install(self.bundle, self.dest, skip_existing=True)

    def test_tampering_prevents_installation(self):
        (self.bundle / 'skills' / 'pdf' / 'SKILL.md').write_text('changed', encoding='utf-8')
        with self.assertRaises(ValueError):
            install(self.bundle, self.dest)
        self.assertFalse(self.dest.exists())

    def test_missing_dependency_prevents_installation(self):
        (self.bundle / 'skills' / 'pdf' / 'SKILL.md').unlink()
        with self.assertRaises(ValueError):
            install(self.bundle, self.dest)

    def test_unlisted_file_prevents_installation(self):
        (self.bundle / 'skills' / 'pdf' / 'private.txt').write_text('extra', encoding='utf-8')
        with self.assertRaises(ValueError):
            install(self.bundle, self.dest)

    def test_destination_inside_bundle_is_rejected(self):
        with self.assertRaises(ValueError):
            install(self.bundle, self.bundle / 'nested')


if __name__ == '__main__':
    unittest.main()
