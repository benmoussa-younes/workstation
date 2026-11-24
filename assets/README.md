# The product's visuals

Workstation Edition ships an emerald visual set under the code's licence,
`AGPL-3.0-or-later`: a wallpaper, a GDM mark and a GRUB image. The SVG sources
sit next to the rendered PNGs, so the set can be regenerated.

| File | Size | Used by | Installed as |
|---|---|---|---|
| `workstation-wallpaper.svg` / `workstation-wallpaper.png` | 3840×2160 | the desktop wallpaper (`dconf` selects it) | `/usr/share/backgrounds/workstation-wallpaper.png` |
| `workstation-logo.svg` | 512×512 | the vector source | (not installed) |
| `workstation-logo-64.png` | 64×64 | GDM's login logo, at the native size GDM draws | `/etc/gdm3/assets/logo.png` |
| `workstation-grub.svg` / `workstation-grub.png` | 1920×1080 | the GRUB menu's image | `/boot/grub/workstation-grub.png` |
| `transparent.png` | 1×1 | a neutral placeholder | (not installed) |

The `branding` role takes its default sources from this directory; a site that
overrides `identity_name` and the `branding_*_source` variables supplies its own
files from its own path.

## The Plymouth theme

`theme/workstation/` is the boot splash. Its script derives from Debian's
`softwaves` theme; the emerald images are new work by Younes BENMOUSSA. The
whole theme is distributed under `GPL-2.0-or-later` and is never relicensed.
`REUSE.toml` declares it separately, with the upstream authors.

## Rebranding

A fork or a site that wants its own marks does not edit this directory or a
role: it overrides `branding_wallpaper_source`, `branding_logo_source`,
`branding_grub_image_source` and `identity_name`, and supplies its own files
from its own path. `README.md` ("Your own branding") gives the sizes and the
Plymouth steps.
