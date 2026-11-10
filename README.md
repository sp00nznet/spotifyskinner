# spotifyskinner

Put a classic Winamp 2.x skin (`.wsz`) on the Spotify desktop app.

The Spotify desktop app is a web UI inside Chromium, so no binary patching is needed.
`wsz2spice.py` reads a Winamp skin and writes a [Spicetify](https://spicetify.app) theme from it.

## What carries over

| Winamp skin file | Spotify |
|---|---|
| `pledit.txt` colors + font | app-wide color scheme and font |
| `main.bmp` | now-playing bar background |
| `cbuttons.bmp` | prev / play / pause / next buttons (with pressed state) |

## Usage

1. Install Spicetify (Windows PowerShell):
   ```powershell
   iwr -useb https://raw.githubusercontent.com/spicetify/cli/main/install.ps1 | iex
   ```
2. Grab a skin, e.g. from the [Winamp Skin Museum](https://skins.webamp.org).
3. Convert and apply:
   ```sh
   python wsz2spice.py SomeSkin.wsz
   spicetify config current_theme SomeSkin color_scheme winamp
   spicetify apply
   ```

Optional second argument sets the themes folder (default `%APPDATA%\spicetify\Themes`).
Python 3 stdlib only, no dependencies.

## Test

```sh
python test_wsz2spice.py
```

## Limits

- Sliders, EQ, visualizer and titlebar sprites aren't mapped yet.
- Play/pause sprite switching keys off the English `aria-label`.
- Spotify updates can rename UI elements; selectors use `data-testid` where possible.

## License

MIT. Winamp skins belong to their authors.
