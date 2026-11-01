#!/usr/bin/env python3
"""Local IELTS workspace utilities. Python 3.10+, standard library only."""
import argparse
from datetime import date, timedelta
import json
from pathlib import Path
import sys
import tempfile

PROJECT = Path(__file__).resolve().parents[1]
INTERVALS = [1, 2, 4, 7, 15, 30]
EXTENSIONS = {'.pdf', '.mp3', '.m4a', '.wav', '.txt', '.md', '.docx'}


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path, data):
    """Replace only after complete serialization; no partial writes on errors."""
    payload = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                     prefix='.study-', delete=False) as stream:
        temp = Path(stream.name)
        try:
            stream.write(payload)
            stream.flush()
        except BaseException:
            temp.unlink(missing_ok=True)
            raise
    try:
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


def initialize(workspace):
    workspace.mkdir(parents=True, exist_ok=True)
    for folder in ('materials', '写作', '录音'):
        (workspace / folder).mkdir(exist_ok=True)
    for source in (PROJECT / 'templates').glob('*.md'):
        dest = workspace / source.name
        # Exclusive creation preserves existing user edits.
        try:
            with dest.open('x', encoding='utf-8') as stream:
                stream.write(source.read_text(encoding='utf-8'))
        except FileExistsError:
            pass
    defaults = {'config.json': {'material_roots': ['materials'],
                                'review_intervals_days': INTERVALS},
                '表达本.json': {'entries': [], 'reviews': []}}
    for name, data in defaults.items():
        try:
            with (workspace / name).open('x', encoding='utf-8') as stream:
                json.dump(data, stream, ensure_ascii=False, indent=2)
                stream.write('\n')
        except FileExistsError:
            pass
    return {'workspace': str(workspace), 'status': 'ready'}


def config_for(workspace):
    config = read_json(workspace / 'config.json')
    roots = config.get('material_roots')
    intervals = config.get('review_intervals_days')
    if not isinstance(roots, list) or not all(isinstance(x, str) and x for x in roots):
        raise ValueError('material_roots must be a list of nonempty paths')
    if (not isinstance(intervals, list) or not intervals
            or any(type(x) is not int or x <= 0 for x in intervals)):
        raise ValueError('review_intervals_days must contain positive integers')
    return config


def index_materials(workspace):
    config = config_for(workspace)
    files, missing, seen = [], [], set()
    for raw in config['material_roots']:
        root = Path(raw).expanduser()
        if not root.is_absolute():
            root = workspace / root
        root = root.resolve()
        if not root.is_dir():
            missing.append(str(root))
            continue
        for path in sorted(root.rglob('*')):
            relative = path.relative_to(root)
            if any(part.startswith('.') for part in relative.parts):
                continue
            if any((root.joinpath(*relative.parts[:i])).is_symlink()
                   for i in range(1, len(relative.parts) + 1)):
                continue
            if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
                continue
            absolute = str(path.resolve())
            if absolute in seen:
                continue
            seen.add(absolute)
            files.append({'path': absolute, 'extension': path.suffix.lower(),
                          'bytes': path.stat().st_size, 'verified': False})
    result = {'files': files, 'missing_roots': missing}
    write_json(workspace / 'materials-index.json', result)
    return {'indexed': len(files), 'missing_roots': missing}


def load_expressions(workspace, levels):
    data = read_json(workspace / '表达本.json')
    entries, reviews = data.get('entries'), data.get('reviews')
    if not isinstance(entries, list) or not isinstance(reviews, list):
        raise ValueError('Expression notebook requires entries and reviews lists')
    ids = set()
    for item in entries:
        ident = item.get('id')
        if not isinstance(ident, str) or not ident or ident in ids:
            raise ValueError('Expression IDs must be unique nonempty strings')
        ids.add(ident)
        level = item.get('level')
        if type(level) is not int or not 0 <= level <= levels:
            raise ValueError('Invalid expression level')
        due = item.get('due')
        if level < levels and not isinstance(due, str):
            raise ValueError('Active expressions require a due date')
        if due is not None:
            date.fromisoformat(due)
        last = item.get('last_reviewed')
        if last is not None:
            date.fromisoformat(last)
    return data


def due_expressions(workspace, today, limit=10):
    config = config_for(workspace)
    levels = len(config['review_intervals_days'])
    data = load_expressions(workspace, levels)
    due = [x for x in data['entries']
           if x['level'] < levels and date.fromisoformat(x['due']) <= today]
    due.sort(key=lambda x: (x['due'], x['level'], x['id']))
    return [{'id': x['id'], 'meaning': x.get('meaning', ''), 'due': x['due']}
            for x in due[:limit]]


def review_expression(workspace, ident, correct, today):
    config = config_for(workspace)
    intervals = config['review_intervals_days']
    data = load_expressions(workspace, len(intervals))
    item = next((x for x in data['entries'] if x['id'] == ident), None)
    if item is None:
        raise ValueError(f'Unknown expression ID: {ident}')
    if item.get('last_reviewed') and date.fromisoformat(item['last_reviewed']) > today:
        raise ValueError('Review date precedes the most recent review')
    if item.get('last_reviewed') == today.isoformat():
        return {'id': ident, 'status': 'already_reviewed_today', 'level': item['level'],
                'due': item['due']}
    old_level = item['level']
    new_level = min(old_level + 1, len(intervals)) if correct else 0
    item['level'] = new_level
    item['due'] = ((today + timedelta(days=intervals[new_level])).isoformat()
                   if new_level < len(intervals) else None)
    item['last_reviewed'] = today.isoformat()
    data['reviews'].append({'id': ident, 'date': today.isoformat(), 'correct': correct,
                            'previous_level': old_level, 'level': new_level})
    write_json(workspace / '表达本.json', data)
    return {'id': ident, 'level': new_level, 'due': item['due']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, default=PROJECT / 'workspace')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init')
    sub.add_parser('index')
    due = sub.add_parser('due')
    due.add_argument('--date', type=date.fromisoformat, default=date.today())
    due.add_argument('--limit', type=int, default=10)
    review = sub.add_parser('review')
    review.add_argument('id')
    review.add_argument('--result', choices=['correct', 'incorrect'], required=True)
    review.add_argument('--date', type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    workspace = args.workspace.expanduser().resolve()
    try:
        if args.command == 'init':
            result = initialize(workspace)
        elif args.command == 'index':
            result = index_materials(workspace)
        elif args.command == 'due':
            if not 1 <= args.limit <= 100:
                raise ValueError('limit must be between 1 and 100')
            result = due_expressions(workspace, args.date, args.limit)
        else:
            result = review_expression(workspace, args.id, args.result == 'correct', args.date)
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(1, f'Error: {error}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
