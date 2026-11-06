"""Dependency-free checks for the distributed source and documentation.

SPDX-License-Identifier: Apache-2.0
"""

import ast
from pathlib import Path
import re
from urllib.parse import unquote, urlparse
import xml.etree.ElementTree as ET


def main():
    root = Path(__file__).resolve().parents[1]
    python_files = list((root / 'src').rglob('*.py')) + list((root / 'tests').glob('*.py'))
    for path in python_files:
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    xml_files = [root / 'src/robotless_lab/package.xml']
    xml_files += list((root / 'src').rglob('*.world'))
    xml_files += list((root / 'docs/assets').glob('*.svg'))
    for path in xml_files:
        ET.parse(path)
    for name in ['LICENSE', 'NOTICE', 'THIRD_PARTY_NOTICES.md', 'README.md',
                 'src/robotless_lab/resource/robotless_lab']:
        if not (root / name).is_file():
            raise FileNotFoundError(name)
    checked_links = 0
    for document in root.rglob('*.md'):
        if '.git' in document.parts:
            continue
        for target in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)', document.read_text(encoding='utf-8')):
            parsed = urlparse(target)
            if parsed.scheme or target.startswith('#'):
                continue
            path = document.parent / unquote(parsed.path)
            if not path.exists():
                raise FileNotFoundError(f'{document.relative_to(root)}: {target}')
            checked_links += 1
    print(f'Project checks passed: {len(python_files)} Python files, '
          f'{len(xml_files)} XML/SVG files, {checked_links} local links.')


if __name__ == '__main__':
    main()
