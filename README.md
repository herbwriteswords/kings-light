# King's Light

A Game Boy Advance game based on H.L. Butler's picture book *King's Light*. Dalton follows the King's lantern down the narrow path, through the fog and the bog, finds the sword, and faces the mirrorbeast on his way home.

**Status:** art drafts. A real `.gba` ROM (built with devkitPro, Butano or libtonc) is planned, to play in Delta on iPhone and on a GBA SP with a flash cart.

## Structure
- `assets/sprites/`: sprite sheets, previews, animated GIFs and mockups
- `tools/`: Python/Pillow scripts that hand-draw every sprite pixel by pixel (`python3 tools/make_dalton.py`, etc.)
- `docs/`: notes

## Assets
| File | Contents |
|---|---|
| `dalton.png` | Dalton with lantern, 16x32 frames: walk down/up/left/right x3, raise lantern, kneel/pray |
| `dalton_soaked.png` | Soaked palette swap (page 20) |
| `dalton_nolantern.png` | Idle x2 (breathe), walk 4 directions x3 with swinging arms |
| `bed.png` | 32x48 bed: bare (for wake-up overlay) and made |
| `dalton_wakeup.png` | 10 frames, 48x48, aligned to bed at (0,0): sleep x2, stir x2, sit up x3, legs over, step out, stand |
| `creatures_*` | Lightning bug, fog creature, broken mirror and shatter, mirrorbeast, sword, sword in grass, songbird, doe, butterfly |
| `*_mockup.png` | 240x160 scenes at 4x |

Each sheet fits one GBA 4bpp palette (at most 15 colors plus transparent).
