# benchproj

A tiny item service (`benchproj/api.py`, stdlib WSGI) and the widget page it
serves (`benchproj/web/`). Serve: `python3 -m benchproj.api 8000`. Test:
`python3 -m pytest tests -q` (the tests call the app directly, no socket).
