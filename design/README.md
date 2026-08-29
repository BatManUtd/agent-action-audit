# Meridian Ledger — project register wallpaper

A phone wallpaper that keeps every active project in one glanceable register.

- **`wallpaper.png`** — 1440 × 3120, native Galaxy S25 Ultra resolution (19.5:9, QHD+)
- **`wallpaper.html`** — the source; edit and re-render to update the register
- **`meridian-ledger.md`** — the design philosophy the plate is built on

## Safe zones

Laid out so the register survives real phone chrome:

| Region | Reserved for |
|---|---|
| `0 – 640px` | status bar + lock-screen clock — left empty |
| `640 – 2830px` | the register itself |
| `2830 – 3120px` | gesture bar / dock — left empty |

Best as a **lock screen**, or as a home screen page with no icons on it.

## Re-rendering

```bash
/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell \
  --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1440,3120 \
  --screenshot=wallpaper.png --virtual-time-budget=4000 wallpaper.html
```

Any Chromium works — point it at your own binary if that path doesn't exist.

## Editing the register

Bands live in `wallpaper.html` as `<section class="band">`. Rows are
`code · name · leader · descriptor`. The layout distributes bands evenly
down the field on its own, so adding or removing entries re-balances
without touching the CSS — but update the footer count (`XX entries`)
and the plotted-point glyph in each band head, whose dot count mirrors
the number of entries in that band.

Fonts are bundled under the SIL Open Font License; see `fonts/*-OFL.txt`.
