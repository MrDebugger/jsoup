# Contributing to jsoup

We appreciate all contributions! Here's how to get involved.

## Bug Fixes

If you're fixing a bug, please go ahead and submit a pull request without prior discussion.

Include:
- A test that reproduces the bug (fails before your fix, passes after)
- A clear commit message explaining what was broken and why

## New Features

If you plan to contribute new features, **please first open an issue** and discuss the feature with us before writing code.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/MrDebugger/jsoup.git
cd jsoup

# Install in editable mode
pip install -e .

# Run tests
python3 -m pytest tests/ -v
```

## Project Structure

```
jsoup/
├── __init__.py       # Public API exports
├── builder.py        # JsonTreeBuilder class
└── registry.py       # install() function
```

## Testing

All changes must include tests. Run the full suite before submitting:

```bash
python3 -m pytest tests/ -v
```

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (x.0.0): Breaking changes to the JSON input format or public API
- **MINOR** (0.x.0): New features that are backward-compatible (new options, new input formats)
- **PATCH** (0.0.x): Bug fixes and internal improvements

### What counts as the public API

- `JsonTreeBuilder` class and its constructor
- `install()` function
- The JSON input format (tag names, `attrs`, `text`, `comment`, `doctype`, `children` keys)

## Pull Request Process

1. Create a feature branch from `master`
2. Make your changes with tests
3. Run the full test suite
4. Submit a PR with a clear description

## Contributors

<a href="https://github.com/MrDebugger/jsoup/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=MrDebugger/jsoup"/>
</a>
