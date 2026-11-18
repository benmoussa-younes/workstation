# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/benmoussa-younes/workstation/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/benmoussa-younes/workstation/releases/tag/v0.1.0
