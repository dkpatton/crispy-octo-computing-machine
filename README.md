# Emerson's Game

A simple SNES-style 2-D platformer scaffold using `pygame`.

All sprite and tile assets are stored as JSON. Most contain base64 encoded
PNG bytes, but sprites can also be defined with a `palette` and `grid`
field describing pixel colors directly. The engine converts these JSON
blobs back into images at runtime, so no binary image files are tracked in
the repository.

## Requirements
- Python 3.11+
- `pygame` 2.5+

## Development

### Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run
```bash
make run
```

### Tests
```bash
make test
```
