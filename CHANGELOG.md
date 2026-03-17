# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-17

### Breaking Changes

- **Package restructured** into `builder.py`, `registry.py`, and `__init__.py`. The monolithic `__init__.py` has been split.
- **Migrated from `setup.py` to `pyproject.toml`.**
- **Method names renamed** to PEP 8: `toString` -> `_to_string`, `decode` -> `_decode`, `handle_charref` -> `_handle_charref`, `prepare_attrs` -> `_prepare_attrs`
- **Removed `xml_feed`** dead code (was `NotImplementedError`)

### Added

- **`children` key support** — accepts bs2json's ordered output format (`{"tag": {"children": [...]}}`), enabling roundtrip conversion between bs2json and jsoup
- **Type hints** on all public methods
- **Docstrings** on all classes and methods
- **`__repr__`** on `JsonTreeBuilder`
- **`.gitignore`** with proper Python/IDE patterns

### Fixed

- **Unpinned `beautifulsoup4`** — changed `==4.9.3` to `>=4.9.3`
- **`install()` tests** — fixed `builder_registry.registry` API that was removed in newer bs4
- **`install()` debug test** — removed test for a bug that no longer exists

## [0.0.1] - 2023-01-01

### Added

- Initial release
- `JsonTreeBuilder` — BeautifulSoup TreeBuilder that accepts JSON input
- `install()` — registers the builder for use as `BeautifulSoup(json, 'jsoup')`
- Support for: tags, attributes, text, comments, doctypes, nested elements, character reference escaping, empty elements, duplicate attribute handling (replace/ignore/callable)
