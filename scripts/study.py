#!/usr/bin/env python3
"""Repository entry point; implementation lives in the portable skill."""
from pathlib import Path
import runpy

_source = Path(__file__).resolve().parents[1] / 'skills/ielts-study/scripts/study.py'
_module = runpy.run_path(str(_source))
globals().update({key: value for key, value in _module.items() if not key.startswith('__')})

if __name__ == '__main__':
    main()
