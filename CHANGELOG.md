# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2026-11-26

### Changed

- `coding_agents` installs OpenCode at the vendor's latest release on every
  converge, as the human account, with the vendor installer's
  `--no-modify-path`. The install task compares the installed version before
  and after the install and reports changed only when it moves, so a second
  converge with no new release prints `changed=0`. The installer is deliberately
  unpinned: the product accepts the vendor's latest release without a checksum,
  by owner decision.

### Removed

- `coding_agents` writes no configuration file and no PATH drop-in: the
  machine-wide `/etc/opencode/opencode.json`, the
  `/etc/profile.d/10-opencode.sh` drop-in, `coding_agents_opencode_config` and
  its path variables are gone. The account owns `~/.config/opencode`, its shell
  files and its PATH; `/etc/opencode/skills` is never touched. A host where the
  role is enabled removes the two files the previous release wrote.
- `coding_agents_opencode_version`, `coding_agents_opencode_install_sha256`,
  `coding_agents_opencode_reinstall` and the installer cache are removed with
  the pin.

## [0.4.2] - 2026-11-24

### Changed

- The firewall accepts IPv6 sources: SSH, mDNS, the extra services and the
  forward flows render `ip6 saddr` (or `ip6 nexthdr`) when the site declares an
  IPv6 CIDR; `ip saddr` alone rejected the ruleset. A port or protocol without
  sources is opened on both families, as a port already was.
- The Avahi and mDNS switches are asserted together at the end of the play: a
  site that disables one without the other fails instead of opening 5353 with
  no responder, or running a daemon no packet reaches.
- `power` covers `suspend-then-hibernate`: the sleep drop-in sets
  `AllowSuspendThenHibernate` with the same switch, the target is masked and
  read back, and logind's answer is checked in `disabled` mode.
- `power` replays a failed initramfs rebuild: a marker records the device the
  image was built for, and the role asks for the handler again when the marker
  disagrees.
- A switch back to `disabled` removes the role's OWN resume file (the SPDX one)
  and rebuilds the image; the installer's file stays.
- `power_grub_default` follows `hardening_grub_default`, and the gaming userns
  drop-in path follows `gaming_userns_sysctl`.
- `performance_observe_packages`' description no longer carries a stray
  `- ethtool`; the identity comment no longer cites `0.1.0`; the README's
  `Project status` states the current release and the known limits.

## [0.4.1] - 2026-11-24

### Added

- The GNOME Add Printer panel lists the network printers and the human account
  can add one: Avahi runs, mDNS (UDP 5353) is accepted from the site's
  `security_ssh_sources`, the CUPS `dnssd` backend enumerates, and the account
  is in `lpadmin`. The legacy `cups-browsed` stays purged (CVE-2024-47176); the
  modern backend does the discovery. No printer is declared in the site.

### Changed

- `common` no longer masks Avahi (`common_avahi_enabled: true`): the unit, the
  socket, the systemd alias and the D-Bus activation file are live. The
  location service's GPS-over-mDNS source stays off.
- `security` opens mDNS 5353 from `security_ssh_sources`
  (`security_mdns_enabled: true`).
- `printing` installs `avahi-daemon` and adds the human account to `lpadmin`;
  `desktop` declares `lpadmin` in its default group set.
- A site whose `security_ssh_sources` is empty (SSH anywhere) must decide mDNS
  too: `security_mdns_sources_anywhere: true`, or `security_mdns_enabled:
  false`. An empty `security_mdns_sources` fails the converge otherwise.

### Security

- Avahi and mDNS are a deliberate surface for the printer discovery, and
  `lpadmin` is CUPS's `SystemGroup`: the account can add, modify and remove the
  local queues and their device URIs. A site that refuses sets
  `common_avahi_enabled: false` and `security_mdns_enabled: false` together.

## [0.4.0] - 2026-11-24

### Added

- The `power` role declares the power policy. Hibernation is disabled by
  default: the sleep drop-in sets `AllowHibernation=no` and
  `AllowHybridSleep=no`, `hibernate.target` and `hybrid-sleep.target` are
  masked, and the role proves the result by reading `CanHibernate` from logind
  and by a `systemctl hibernate` that must fail. An `enabled` site must declare
  `power_resume_device`; the role writes
  `/etc/initramfs-tools/conf.d/resume` and notifies `update-initramfs -u`.
- `power` refuses to enable hibernation before the running kernel was booted
  with `resume=<device>`. The kernel line is `hardening`'s
  (`hardening_kernel_cmdline`), and the role reads it instead of editing GRUB.
  The console proof (a real hibernate and resume) is the only proof, and the
  role says so.

### Changed

- Unprivileged user namespaces are enabled on the workstation by default
  (`hardening_unprivileged_userns_clone: 1`). GNOME's default applications need
  them: Loupe's glycin loaders spawn `bwrap`, which a host with
  `kernel.unprivileged_userns_clone=0` refuses. Measured on the laptop
  (2026-11-24): `bwrap` answers "No permissions to create a new namespace",
  Loupe logs a decoding error then opens its failure window; with 1, the loaders
  start and Loupe reports no decoding error. A site sets 0 to close the kernel
  surface and accepts that Loupe and Flatpak-based applications stop working;
  `gaming_enabled: true` keeps them at 1 for Steam.
- The screen blank delay is the account's. `/org/gnome/desktop/session/idle-delay`
  is no longer locked; the system default is 15 minutes (`dconf_idle_delay:
  900`), and an account may choose another value or Never. The screen lock and
  the suspend policy stay locked. Measured on the laptop (2026-11-24):
  `gsettings writable` was false with the lock and 300 s; after unlocking and
  `dconf update`, it is true and the value is 900 s.
- The role now refuses a lock file it does not declare in
  `/etc/dconf/db/local.d/locks` (a leftover from a previous layout could lock a
  key the product leaves to the account) and reads the screen-policy lock file
  back to prove `idle-delay` is not in it.

### Security

- Hibernation writes the whole memory image, including every secret the host
  holds at that instant, to a swap this product does not encrypt. It is off by
  default and never presented as a security property; enabling it is the site's
  documented trade-off. The role creates, converts, formats and encrypts no
  swap.
- The cost of refusing unprivileged user namespaces is now stated where it is
  decided: the sysctl file names Loupe/glycin and Flatpak-based applications,
  not only rootless containers. The final value is asserted at the end of the
  play, after the `gaming` role's override. The AppArmor transition stays
  enforced but was measured ineffective on Debian.
- The idle blank is the account's choice: the screen-lock and suspend keys stay
  locked, but choosing Never disables the idle trigger, so the session is not
  locked by inactivity. The product default is 15 minutes.

## [0.3.1] - 2026-11-21

### Removed

- `gnome-tweaks` and `gnome-shell-extension-prefs` leave the product: Tweaks'
  Shell panel is the extension switcher the locked policy refuses, and its other
  knobs are declared by `dconf`. Both join the `common` absent list, and apt is
  told to refuse them: a `Pin-Priority: -1` preference makes `apt-get install`
  answer "no installable version" (rc 100) instead of reinstalling them, while a
  `dpkg -i` stays the root operator's escape hatch. The `gnome-extensions`
  command is shipped by `gnome-shell` itself and cannot be removed without the
  shell; `disable-user-extensions` and `allow-extension-installation` stay
  locked, so it has nothing to switch on.
- Tweaks and the Extensions app leave the application grid's System folder.

  The `applications` list and the apt refusal must land in the same release: a
  host that runs a collection still declaring `gnome-tweaks` would ask apt to
  install a package the refusal forbids, and the `applications` role would fail
  there. A site that keeps Tweaks sets `common_refused_packages: []` and removes
  it from `common_absent_packages`; the refusal file is then removed instead of
  being left behind.

### Changed

- The extension set is empty and no longer described as four. GNOME Shell 48
  (Debian 13, `gnome-shell 48.7`) has no StatusNotifier/AppIndicator host of its
  own. Measured on the laptop, 2026-11-21: `gdbus … IsStatusNotifierHostRegistered`
  answers `ServiceUnknown`, `dpkg -L gnome-shell` carries no such code, no D-Bus
  service file provides the watcher name, and the only provider on the host is
  the disabled `ubuntu-appindicators@ubuntu.com` extension. A tray is therefore a
  site's explicit decision, never a default, and an application must work
  without one: closing it quits.

### Fixed

- `common` now names an installed extension package at the next converge, and
  proves the apt refusal twice: the `-1` priority is read from apt's version
  table and `apt-get -s install` must answer "no installable version". Drift is
  reported instead of being discovered in a session.
- `dconf`: the keyfile header claimed "four extensions" and "four keys" while the
  declared set has been empty since 0.3.0 and the lock file carries three keys.

## [0.3.0] - 2026-11-20

### Removed

- The optional `virtualization` role (libvirt/virt-manager, rootless Podman) is
  gone from the workstation edition: those stacks belong to the `virtualization`
  and `container` products. A site that set `virtualization_enabled: true`
  declares it there instead. The `virbr*` and `libvirt_nat` rules, the
  `virt-manager` favorite, `qemu-guest-agent` and the `62-podman-userns.conf`
  drop-in go with it.

### Changed

- No GNOME Shell extension is shipped, enabled or installable: the four
  `gnome-shell-extension-*` packages are removed by the `common` absent list,
  `applications_extension_uuids` and `dconf_extensions` are empty, and
  `disable-user-extensions` / `allow-extension-installation` stay locked.

### Security

- The sshd drop-in declares `RequiredRSASize 2048` and the algorithm lists:
  MACs, ciphers, KEX, host-key and public-key algorithms no longer fall back to
  Debian's defaults that still admit `hmac-sha1`, `umac-64` and 1024-bit RSA.
- The `common` absent list now removes `htop`, the Java runtime and the Commons
  Collections 3 gadget that `libreoffice`'s Recommends pulled in; the office
  suite stays.

### Fixed

- `network`: the invalid `wifi.cloned-mac-address` key is removed (the
  NetworkManager warning and the silent no-op go with it).
- `dconf`: `disable-user-extensions=true`; the four declared extensions can no
  longer be switched off by the account.

## [0.2.1] - 2026-11-20

### Security

- The nftables drop-in now clears `ExecReload` as well as `ExecStart`. The
  distribution's reload loaded only `/etc/nftables.conf`, whose `flush ruleset`
  removed the product table; a `systemctl reload nftables` now fails instead of
  leaving the workstation without its firewall.

### Fixed

- The Scripts release lookup runs in check mode. `uri` does not execute in a
  dry run, so the registered result carried no `json` and the fact task failed
  before the remaining roles were reached; the downloads stay guarded.
- The dry run reaches the end: the OpenCode installer fetch and read-back are
  guarded, the boot proof ends in check mode, a `find` on a drop-in directory
  the role has not created yet is skipped from a remote `stat` instead of
  warning, and the greeter background file is created when a dry run cannot get
  it from the package.

## [0.2.0] - 2026-11-19

### Fixed

- The Plymouth LUKS password bullets no longer overlap. The dot asset carried a
  17x17 px disc on a 10.5 px step, so consecutive bullets cut into each other;
  it now keeps the 10x10 px upstream geometry at +6+5, which leaves a gap and
  restores the field's proportion.

### Security

- The SSH client now reads a system-wide drop-in
  (`/etc/ssh/ssh_config.d/99-workstation.conf`) that clears `IPQoS` and restricts
  KEX, ciphers, MACs, host keys and user key algorithms. Debian's
  `openssh-client` 10.0p1 marks sessions DSCP EF, and on the measured 2026-11-19
  path every EF SYN was dropped: `ssh -T git@github.com` timed out while
  `IPQoS=none` authenticated. The drop-in applies to every account without a
  file in any home; a user's `~/.ssh/config` is read first and can still
  override it.
- Compatibility: an ECDSA-only host key, an ECDSA user key or a legacy
  `ssh-rsa`/CBC/CTR-only peer is refused. SSH certificate authentication is
  refused too: the lists carry no `*-cert-v01@openssh.com` name. A site that
  needs one of them overrides the `security_ssh_client_*` lists.
- The workstation password quality policy now matches the server's: `minlen`
  14, `minclass` 4, `maxsequence` 3, `difok` 2, `dictcheck` 1, `enforcing` 1 and
  `enforce_for_root`. `libpam-pwquality` and the `common-password` line were
  already in place; the template was the weaker half.

## [0.1.0] - 2026-11-18

### Added

- The Ansible collection `benmoussa.workstation` and its 0.1.0 release.
- The desktop baseline: common, identity, journald, keyboard, hardening,
  performance, network, resolver, time and security.
- The GNOME desktop on Wayland: gnome, desktop, dconf, applications, developer,
  coding_agents, fonts, audio, printing and display.
- The boot experience: the emerald branding set, the GRUB image and the
  Workstation Plymouth theme.
- The opt-in gaming stack and the declared developer tool groups.
- An optional local virtualization stack (`virtualization_enabled`):
  libvirt/virt-manager and rootless Podman, with the default NAT network,
  storage pool, user socket and subordinate IDs. No VM or container is created.
- The example inventory with documentation values only (TEST-NET-1).
- The repository gate, the CI workflow and the release workflow.

### Changed

- The default displayed name is `Workstation Edition`; a site overrides
  `identity_name` and the related identity variables.
- The default visual set uses the emerald palette, including the Plymouth
  splash.
- The `alsa-utils` restore workaround is opt-in (`audio_fix_alsa_restore:
  false`): it is enabled in the site `host_vars` of the machine that shows the
  two udev warnings, and a host without the package or the rule is not a
  failure.
- VLC is installed by default and declared as the default handler for the video
  and audio MIME types the workstation ships.
- Shotwell and `shotwell-common` are retired: GNOME's Loupe is the image viewer,
  and the second organizer has no product use.
- VSCodium is no longer installed by default: the `applications` role retires
  the old package and repository, and the `developer` role installs VSCodium
  only when `vscodium` is selected in `developer_tools`.
- `dbus-broker` serves the system bus and the systemd user manager by default
  (`performance_dbus_provider: broker`), as in the Server collection;
  `dbus-daemon` is the rollback. The `dbus-daemon` binary stays installed for
  the accessibility bus and `dbus-run-session`. Measured on a GNOME/Wayland
  session: no failed unit, the shell extension interface and the portals up.
- Avahi is fully retired: besides the masked unit, its unit alias and its
  D-Bus activation file are closed, so no client's request reaches systemd and
  the bus no longer logs an activation failure at boot. The location service's
  network-NMEA source is declared off, since it fetched a GPS over mDNS.
- The `virtualization` role declares `kernel.unprivileged_userns_clone=1` for
  rootless Podman, in a drop-in that loads after the hardening file, and reads it
  back; the libvirt network and pool are read in the C locale so a translated
  `virsh` is not mistaken for an inactive network.
- The Wi-Fi key is always derived from the passphrase: a password that happens
  to look like 64 hex characters is still a passphrase, and sending it verbatim
  made the access point refuse the association. A site that holds a real derived
  key says so with `network_wifi_psk_is_derived: true`. The ifupdown backup is
  written with the derived key, never the passphrase.
- A declared address is proved by the boot that uses it: with
  `network_boot_address` declared and `workstation_reboot_after: true`, the
  playbook flushes its handlers, reboots once the link is handed to
  NetworkManager, reconnects at the declared address and fails on a DHCP lease.
  Nothing reboots unless the site asks for it.
- GRUB's menu title is the product's, not Debian's: `hardening` replaces the
  `GRUB_DISTRIBUTOR` literal and rebuilds the menu, then reads the result back.
- The `security` role declares the libvirt bridge DHCP/DNS/forward/NAT rules
  when `virtualization_enabled`; `virtualization` requires `security` in the
  play. The `desktop` role adds the `systemd-journal` group for GNOME Logs, and
  `dconf` declares the application-grid folders.
- The Plymouth theme shows one emerald W: the static `logo.png` duplicate behind
  the rotating badge is removed from the script and from an installed theme.
- The `developer` role gains the opt-in `scripts` group: it installs the latest
  published Scripts interpreter from the project's public GitHub release, after
  verifying the release `SHA256SUMS`.

### Security

- The firewall is default-deny and sshd is hardened.
- The Wi-Fi keyfile is root-only and the interface is owned by NetworkManager.
- The session is Wayland-only, with GDM's policy in a drop-in.

[Unreleased]: https://github.com/benmoussa-younes/workstation/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/benmoussa-younes/workstation/releases/tag/v0.5.0
[0.1.0]: https://github.com/benmoussa-younes/workstation/releases/tag/v0.1.0
