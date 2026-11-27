# Role catalog

Every behaviour of this product is one role, listed here once. A role carries
no README of its own. The catalog is the single list of roles; a new role is
added to this table in the same change that creates it.

| Role | Concern | Status |
|---|---|---|
| `common` | The package baseline, the periodic security upgrades and the configuration directories. The server's list minus the server-only removals; Shotwell and `shotwell-common` are retired (Loupe is the image viewer), and Avahi runs for the mDNS printer discovery (the location service's GPS-over-mDNS source stays off). No GNOME Shell extension, extension switcher or Tweaks: the packages are purged, and an apt `Pin-Priority: -1` makes apt refuse to install `gnome-tweaks` and `gnome-shell-extension-prefs` again. | implemented |
| `identity` | The product's name on the machine: os-release, `/etc/issue`, the login banner, the machine identity. `identity_product` is `workstation-gnome`. | implemented |
| `journald` | The journal's size and retention. | implemented |
| `keyboard` | The console keyboard, and GRUB's copy of it. | implemented |
| `hardening` | The server's kernel and system hardening, without the Bluetooth core blacklist; `bnep` stays blacklisted and `rfcomm` is available for HFP/SAP/OBEX. It adds the desktop's kernel line (`splash`) and an optional console shell. The `/tmp` drop-in is derived from fstab, never from the live mount. Unprivileged user namespaces are enabled for GNOME's default applications (Loupe/glycin, Flatpak-based applications); a site closes them with `hardening_unprivileged_userns_clone: 0`, except `gaming_enabled: true`, which keeps them at 1 for Steam. | implemented |
| `performance` | The server's declared tuning, with `dbus-broker` as the system and user-manager bus provider and Debian's `dbus-daemon` as the rollback. | implemented |
| `power` | Hibernation, hybrid sleep and suspend-then-hibernate disabled by default: the sleep drop-in, the masked targets and the logind read-back (a refused `systemctl hibernate`). `enabled` is the site's explicit acceptance of the unencrypted-swap risk; it writes the initramfs resume file, replays a failed rebuild, and refuses a host whose running kernel was not booted with `resume=`. It never creates, converts, formats or encrypts a swap and never writes GRUB. | implemented |
| `network` | The link, owned by NetworkManager: a `systemd-networkd` host is handed over from a detached oneshot; a site-managed Wi-Fi profile is verified, never overwritten. The boot-mode keyfile takes a declared static address and DNS, refuses a reboot with neither resolver, and carries the Wi-Fi key derived from the passphrase. | implemented |
| `resolver` | The stub resolver, taking the link DNS NetworkManager hands it. | implemented |
| `time` | Exactly one time daemon, and the declared timezone. | implemented |
| `gnome` | `gnome-core` and Debian's desktop task, the product's only desktop; Papers and Showtime are pinned before the meta-package and Evince/Totem are retired; a Wayland session must exist. | implemented |
| `desktop` | The human account's desktop groups (including CUPS's `lpadmin`), its canonical locale (written through Debian's `/etc/default/locale` symlink) and the Bluetooth daemon. The account itself is a precondition. | implemented |
| `dconf` | The profile-wide GNOME policy, as data: appearance, wallpaper, screen lock, privacy, no shell extension (the set is empty and locked), favorites and the application-grid folders (Utilities, System, Media, Office, Graphics, Internet). The folders are the grid's initial state; an account's arrangement lives in `app-picker-layout` and is reset to rebuild it. The screen blank delay is the account's (15 minutes default); choosing Never disables the idle blank and lock, while the screen lock and the suspend policy stay locked. | implemented |
| `applications` | The declared applications (Ptyxis, LibreOffice, Evolution, Inkscape, GIMP, GNOME Secrets, GNOME Music, VLC, Foliate, GNOME Logs) and Mozilla Firefox; the role adds Mozilla's pinned apt repository, purges `firefox-esr`, retires the old VSCodium default, and declares VLC as the default handler for video/audio MIME types. | implemented |
| `developer` | The declared developer tool groups via `developer_tools` (build, debug, clang, dotnet, search, lint, ansible, database, python, network, packaging, bench, test, shell, docs, jre, vscodium, scripts); Debian packages, the .NET 10 SDK from Microsoft's official repository when `dotnet` is selected, VSCodium from its pinned repository when `vscodium` is selected, and the latest Scripts interpreter from its public GitHub release when `scripts` is selected. No editor by default, no dotfile or service, and no LaTeX group. | implemented |
| `git` | The human account's minimal Git configuration: the system defaults (`init.defaultBranch=main`, `user.useConfigOnly=true`, `fetch.prune`, `pull.rebase`, `push.autoSetupRemote`, `color.ui`) and the account's `user.name`/`user.email` from the site. Key by key in `/etc/gitconfig` and `~/.gitconfig`, read back; no whole-file template and no invented identity. | implemented |
| `coding_agents` | Opt-in OpenCode for the human account at the vendor's latest release: its own installer, run with `--no-modify-path`, writes only `$HOME/.opencode/bin` (the binary and its shim). No configuration file, PATH drop-in, model, provider or credential is declared; the account owns `~/.config/opencode` and its PATH. The previous release's `/etc/opencode/opencode.json` and `/etc/profile.d/10-opencode.sh` are removed when the role is enabled. | implemented |
| `gaming` | The opt-in gaming stack: Debian's Steam installer, controller rules, `gamemode`, `mangohud` and the 32-bit mesa/vulkan stack. Keeps unprivileged user namespaces at 1 for Steam's pressure-vessel sandbox, even when a site sets `hardening_unprivileged_userns_clone: 0`. Requires Debian `contrib` and i386; inert unless `gaming_enabled` is true. Steam is proprietary, isolated and opt-in. | implemented |
| `fonts` | The declared font families and the fontconfig proof. | implemented |
| `audio` | The PipeWire package set, `alsa-ucm-conf` and the GStreamer codecs; the session proof is after login. The `alsa-utils` restore workaround is opt-in (`audio_fix_alsa_restore`, default false), available for hosts that show the udev warnings. | implemented |
| `printing` | CUPS, the virtual PDF queue and the network printer discovery (Avahi/mDNS; the human account in `lpadmin`; `cups-browsed` stays purged). | implemented |
| `display` | GDM: the unit, `WaylandEnable` in `daemon.conf`, the greeter's logo key, the seat read back. Never a hand-made `display-manager.service` alias. | implemented |
| `plymouth` | The Workstation boot splash: the theme, its boot/shutdown/reboot messages, its selection and the initramfs, read back. | implemented |
| `branding` | The wallpaper, GDM's logo and GRUB's image, from this product's own assets. | implemented |
| `security` | nftables input policy (IPv4 and IPv6 sources for SSH, mDNS and the extra services), sshd, the system-wide SSH client drop-in, the desktop passphrase prompt (`ssh-askpass`), the password and lockout policy. mDNS 5353 is accepted from the site's sources for the printer discovery. | implemented |

The `security` role also writes `/etc/ssh/ssh_config.d/99-workstation.conf`. Debian
includes that directory before its own `Host *` block, and `ssh_config` keeps the
first value it reads, so the drop-in applies to every account without a file in
any home. A user's `~/.ssh/config` is still read before the system files and can
override it: the drop-in is the product's policy, not a guarantee against a
user's own file.

The role also installs `ssh-askpass`, `ssh-askpass-gnome` and
`ssh-askpass-fullscreen`: an ssh or git call with no terminal needs a prompt,
and Debian installs none by default. `SSH_ASKPASS` is not written, because
OpenSSH 10 falls back to `/usr/bin/ssh-askpass` when it is unset; `environment.d`
would not reach `login`, `su` or `sshd` anyway.

A role is `implemented` once its tasks, defaults and `meta/argument_specs.yml`
exist and a converge proves it; the evidence is the gate and the converge.
A role that cannot work without a value declares it and fails loudly; it never
invents a host, a user, a printer or a package.
