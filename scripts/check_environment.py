#!/usr/bin/env python3
"""检查运行时与技能入口；不安装软件，不保证中文字体或 TeX 宏包齐全。"""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys

from install import SKILLS, configure_output


def inspect(skills_root):
    return {
        'python': {'version': sys.version.split()[0], 'ok': sys.version_info >= (3, 10)},
        'commands': {name: shutil.which(name) for name in ('xelatex', 'biber', 'pdftotext', 'pdftoppm', 'pdfinfo')},
        'packages': {name: importlib.util.find_spec(name) is not None for name in ('pypdf', 'pdfplumber', 'PIL', 'yaml')},
        'skills': {name: (skills_root / name / 'SKILL.md').is_file() for name in SKILLS},
    }


def main():
    configure_output()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills-root', type=Path, default=Path.home() / '.agents' / 'skills')
    args = parser.parse_args()
    result = inspect(args.skills_root.expanduser())
    result['ok'] = result['python']['ok'] and all(result['commands'].values()) and all(result['packages'].values()) and all(result['skills'].values())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
