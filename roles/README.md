# Role catalog

Every behaviour of this product is one role, listed here once. A role carries
no README of its own. The catalog is decided before the first role is written;
a new role is added to this table in the same change that creates it.

| Role | Concern | Status |
| --- | --- | --- |
| `common` | The package baseline, the periodic security upgrades and the configuration directories. The server's list minus the server-only removals; Shotwell and `shotwell-common` are retired (Loupe is the image viewer), and Avahi is retired with its unit alias and D-Bus activation file masked/diverted. No GNOME Shell extension, extension switcher or Tweaks: the packages are purged, and an apt `Pin-Priority: -1` makes apt refuse to install `gnome-tweaks` and `gnome-shell-extension-prefs` again. | implemented |
| `identity` | The product's name on the machine: os-release, `/etc/issue`, the login banner, the machine identity. `identity_product` is `workstation-gnome`. | implemented |
| `journald` | The journal's size and retention. | implemented |
| `keyboard` | The console keyboard, and GRUB's copy of it. | implemented |
| `hardening` | The server's kernel and system hardening, without the Bluetooth core blacklist; `bnep` stays blacklisted and `rfcomm` is available for HFP/SAP/OBEX. It adds the desktop's kernel line (`splash`) and an optional console shell. The `/tmp` drop-in is derived from fstab, never from the live mount. | implemented |
| `performance` | The server's declared tuning, with `dbus-broker` as the system and user-manager bus provider and `daemon` as the rollback. | implemented |
| `network` | The link, owned by NetworkManager: a `systemd-networkd` host is handed over from a detached oneshot; a site-managed Wi-Fi profile is verified, never overwritten. The boot-mode keyfile takes a declared static address and DNS, refuses a reboot with neither resolver, and carries the Wi-Fi key derived from the passphrase. | implemented |
| `resolver` | The stub resolver, taking the link DNS NetworkManager hands it. | implemented |
| `time` | Exactly one time daemon, and the declared timezone. | implemented |
| `gnome` | `gnome-core` and Debian's desktop task, the product's only desktop; Papers and Showtime are pinned before the meta-package and Evince/Totem are retired; a Wayland session must exist. | implemented |
| `desktop` | The human account's desktop groups, its canonical locale (written through Debian's `/etc/default/locale` symlink) and the Bluetooth daemon. The account itself is a precondition. | implemented |
| `dconf` | The profile-wide GNOME policy, as data: appearance, wallpaper, screen lock, privacy, no shell extension (the set is empty and locked), favorites and the application-grid folders (Utilities, System, Media, Office, Graphics, Internet). The folders are the grid's initial state; an account's arrangement lives in `app-picker-layout` and is reset to rebuild it. The screen blank delay is the account's (15 minutes default); choosing Never disables the idle blank and lock, while the screen lock and the suspend policy stay locked. | implemented |
| `applications` | The declared desktop applications (LibreOffice, Evolution, Inkscape, GIMP, GNOME Secrets, GNOME Logs, VLC) and Mozilla Firefox; the role adds Mozilla's pinned apt repository, purges `firefox-esr`, retires the old VSCodium default, and declares VLC as the default handler for video/audio MIME types. | implemented |
| `developer` | The declared developer tool groups via `developer_tools` (build, debug, clang, dotnet, search, lint, ansible, database, python, network, packaging, bench, test, shell, docs, jre, vscodium, scripts); Debian packages, the .NET 10 SDK from Microsoft's official repository when `dotnet` is selected, VSCodium from its pinned repository when `vscodium` is selected, and the latest Scripts interpreter from its public GitHub release when `scripts` is selected. No editor by default, no dotfile or service, and no LaTeX group. | implemented |
| `coding_agents` | Opt-in OpenCode for the human account: the vendor's installer, pinned by version and SHA-256, the machine-wide `/etc/opencode/opencode.json` and the PATH drop-in. No model, provider or credential is declared. | implemented |
| `gaming` | The opt-in gaming stack: Debian's Steam installer, controller rules, `gamemode`, `mangohud` and the 32-bit mesa/vulkan stack. Re-enables unprivileged user namespaces for Steam's pressure-vessel sandbox (the hardening role disables them elsewhere). Requires Debian `contrib` and i386; inert unless `gaming_enabled` is true. Steam is proprietary, isolated and opt-in. | implemented |
| `fonts` | The declared font families and the fontconfig proof. | implemented |
| `audio` | The PipeWire package set, `alsa-ucm-conf` and the GStreamer codecs; the session proof is after login. The `alsa-utils` restore workaround is opt-in (`audio_fix_alsa_restore`, default false), available for hosts that show the udev warnings. | implemented |
| `printing` | CUPS and the virtual PDF queue. A physical printer is site data. | implemented |
| `display` | GDM: the unit, `WaylandEnable` in `daemon.conf`, the greeter's logo key, the seat read back. Never a hand-made `display-manager.service` alias. | implemented |
| `plymouth` | The Workstation boot splash: the theme, its boot/shutdown/reboot messages, its selection and the initramfs, read back. | implemented |
| `branding` | The wallpaper, GDM's logo and GRUB's image, from this product's own assets. | implemented |
| `security` | nftables input policy, sshd, the system-wide SSH client drop-in, the password and lockout policy. | implemented |

The `security` role also writes `/etc/ssh/ssh_config.d/99-workstation.conf`. Debian
includes that directory before its own `Host *` block, and `ssh_config` keeps the
first value it reads, so the drop-in applies to every account without a file in
any home. A user's `~/.ssh/config` is still read before the system files and can
override it: the drop-in is the product's policy, not a guarantee against a
user's own file.

A role is `implemented` once its tasks, defaults and `meta/argument_specs.yml`
exist and a converge proves it; the evidence is the gate and the converge.
A role that cannot work without a value declares it and fails loudly; it never
invents a host, a user, a printer or a package.
