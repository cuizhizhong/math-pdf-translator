#!/usr/bin/env python3
"""验证发布清单、技能元数据、Nature 路由与第三方来源。"""
import hashlib
import json
from pathlib import Path
import re
import sys

import yaml
from install import ROOT, SKILLS, validate_bundle


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def main():
    validate_bundle(ROOT)
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    for rel, sha in manifest['files'].items():
        assert hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == sha, rel
    for name in SKILLS:
        path = ROOT / 'skills' / name
        content = (path / 'SKILL.md').read_text(encoding='utf-8')
        front = yaml.safe_load(content.split('---', 2)[1])
        assert front['name'] == name and isinstance(front['description'], str), name
        for config in (path / 'agents').glob('*.yaml'):
            yaml.safe_load(config.read_text(encoding='utf-8'))
    reader = ROOT / 'skills' / 'nature-reader'
    routing = yaml.safe_load((reader / 'manifest.yaml').read_text(encoding='utf-8'))
    references = routing['always_load'] + list(routing['axes']['source_format']['values'].values())
    references += [item['path'] for item in routing['references']['on_demand']]
    for rel in references:
        assert (reader / rel).is_file(), rel
    provenance = json.loads((ROOT / 'provenance.json').read_text(encoding='utf-8'))
    for item in provenance['files']:
        assert git_blob((ROOT / item['path']).read_bytes()) == item['git_blob_sha1'], item['path']
    private = re.compile(r'(?:[A-Z]:[\\/](?:Users|work)[\\/]|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})', re.I)
    for rel in manifest['files']:
        if Path(rel).suffix.lower() not in ('.png', '.jpg'):
            text = (ROOT / rel).read_text(encoding='utf-8')
            # 测试模式自身包含的正则文本并不是实际凭据。
            assert not private.search(text), f'疑似本机路径或凭据: {rel}'
    print(f"验证通过: {len(SKILLS)} 个技能，{len(manifest['files'])} 个发布文件，{len(provenance['files'])} 个上游文件")
    return 0


if __name__ == '__main__':
    sys.exit(main())
