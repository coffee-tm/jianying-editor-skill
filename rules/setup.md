---
name: setup
description: Python script initialization and environment setup rules.
metadata:
  tags: setup, python, import, sys.path
---

# Environment Initialization

Use a single reliable bootstrap path. Do not assume helper files outside this repo.

## Recommended Bootstrap (Mandatory)

```python
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
skill_candidates = [
    os.path.join(current_dir, ".agent", "skills", "jianying-editor"),
    os.path.join(current_dir, ".trae", "skills", "jianying-editor"),
    os.path.join(current_dir, ".claude", "skills", "jianying-editor"),
    os.path.join(current_dir, "skills", "jianying-editor"),
    os.path.abspath(".agent/skills/jianying-editor"),
    os.path.dirname(current_dir),  # when script is under examples/
]

scripts_path = None
for p in skill_candidates:
    if os.path.exists(os.path.join(p, "scripts", "jy_wrapper.py")):
        scripts_path = os.path.join(p, "scripts")
        break

if not scripts_path:
    raise ImportError("Could not find jianying-editor/scripts/jy_wrapper.py")

if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

from jy_wrapper import JyProject
```

## Notes

- Do not use `from jy import JyProject` unless your project explicitly provides `jy.py`.
- Put business scripts in the user workspace, not inside the skill repo.
- Always call `project.save()` at the end.
