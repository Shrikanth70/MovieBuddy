"""Unified components package for Streamlit pages and shared UI helpers.

This repo contains both a top-level `components.py` module and a `components/`
directory with submodules like `movie_card.py`. On Streamlit Cloud, imports such
as `from components import movie_card` can register the package first, causing
later `import components as ui` calls to resolve to the package object instead of
the shared UI module. We explicitly load and re-export the helpers from the
top-level implementation file so both import styles are compatible.
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


_IMPL_PATH = Path(__file__).resolve().parent.parent / "components.py"
_SPEC = spec_from_file_location("moviebuddy_components_impl", _IMPL_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Unable to load shared UI helpers from {_IMPL_PATH}")

_MODULE = module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)

for _name in dir(_MODULE):
    if _name.startswith("__"):
        continue
    globals()[_name] = getattr(_MODULE, _name)

del Path
del module_from_spec
del spec_from_file_location
del _IMPL_PATH
del _SPEC
del _MODULE
del _name
