# Security policy

## Supported versions

| Version | Supported |
|---|---|
| 0.1.x | yes |
| older | no |

A release is supported until a later release explicitly withdraws it. Debian
amd64 is the supported base; a future Debian release is added when the product
declares it.

Security fixes are considered on a **best-effort** basis for the current 0.1.x
tree. There is no long-term support branch, support contract, response-time
guarantee or warranty, express or implied. The product is distributed under
**AGPL-3.0-or-later**, the documentation under **CC-BY-SA-4.0** and the Plymouth
theme under **GPL-2.0-or-later**, without warranty, as stated in
[`LICENSE`](LICENSE) and `LICENSES/`.

## Reporting a vulnerability

Do not open a public issue. Report it privately to:

**younes.benmoussa@pm.me**

Include:

- the product version (`cat VERSION`);
- the role and task, or the file and line;
- the affected Debian release;
- a reproduction, if it is safe to share;
- the impact you believe it has.

Reports are read on a best-effort basis; there is no response-time guarantee.
When a fix is agreed, the disclosure date is agreed with the reporter. If you
need an encrypted channel, ask for the current security contact key in the first
message.

## Scope

In scope:

- the roles in `roles/`, the playbooks, the collection archive and the
  repository tooling;
- the declared firewall, SSH, account-group and cryptographic policy;
- the vault and secret-handling paths;
- a defect that makes a correct machine fail or a converge unsafe.

Out of scope:

- the services a site adds;
- the site's network, hardware, DNS, NTP or Debian mirror;
- a host that is not Debian amd64;
- a site inventory or vault that was edited outside the documented workflow.

## What the product does not do

- It does not create the human account, an SSH key or a sudoers entry.
- It does not send telemetry.
- It does not reboot a machine silently.
- It does not store a secret outside the site vault and the root-only files the
  roles create.
- It does not install a Flatpak by default.

## Hardening baseline

The product declares:

- `nftables` input default-deny, with SSH restricted to the declared sources;
- sshd hardened, with a declared password and lockout policy;
- sysctl, module, auditd and resource-limit hardening;
- NetworkManager owning the link, with the Wi-Fi keyfile root-only;
- a Wayland-only session, with GDM's policy in a drop-in.

The exact values are in `roles/*/defaults/main.yml` and the role comments.
