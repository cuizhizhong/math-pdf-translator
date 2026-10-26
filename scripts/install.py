#!/usr/bin/env python3
"""将发布包中的六个技能安装到同一个技能根目录，不覆盖已有文件。"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('math-pdf-translator', 'nature-reader', 'nature-shared',
          'elegantpaper-master', 'elegantbook-master', 'pdf')


def validate_bundle(root):
    root = Path(root).resolve()
    records = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))['files']
    actual = {p.relative_to(root).as_posix() for p in (root / 'skills').rglob('*') if p.is_file()}
    expected = {p for p in records if p.startswith('skills/')}
    if actual != expected:
        raise ValueError('技能文件清单不一致，请重新下载完整发布包')
    for rel in sorted(expected):
        path = root / rel
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != records[rel]:
            raise ValueError(f'技能文件校验失败: {rel}')
    for name in SKILLS:
        if not (root / 'skills' / name / 'SKILL.md').is_file():
            raise ValueError(f'缺少技能入口: {name}')


def install(root, destination, skip_existing=False, dry_run=False):
    root, destination = Path(root).resolve(), Path(destination).expanduser().resolve()
    validate_bundle(root)
    if destination == root or root in destination.parents:
        raise ValueError('安装目录不能位于发布包内部')
    actions = []
    for name in SKILLS:
        target = destination / name
        if target.exists() or target.is_symlink():
            if skip_existing and target.is_dir() and not target.is_symlink() and (target / 'SKILL.md').is_file():
                actions.append((name, '保留已有'))
            else:
                raise FileExistsError(f'目标已存在，未写入任何文件: {target}；确认兼容后可用 --skip-existing')
        else:
            actions.append((name, '安装'))
    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)
        for name, action in actions:
            if action == '安装':
                shutil.copytree(root / 'skills' / name, destination / name)
    return actions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, default=Path.home() / '.agents' / 'skills', help='技能根目录')
    parser.add_argument('--skip-existing', action='store_true', help='保留已有技能；用户自行确认版本兼容')
    parser.add_argument('--dry-run', action='store_true', help='仅预检，不写入')
    args = parser.parse_args()
    try:
        actions = install(ROOT, args.dest, args.skip_existing, args.dry_run)
    except (OSError, ValueError, KeyError) as exc:
        print(f'安装失败: {exc}', file=sys.stderr)
        return 1
    print(('预检' if args.dry_run else '安装') + f'目录: {args.dest.expanduser().resolve()}')
    for name, action in actions:
        print(f'{action}: {name}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
