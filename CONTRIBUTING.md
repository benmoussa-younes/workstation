# Contributing

Workstation Edition is a set of Ansible roles that turn a Debian machine into
a GNOME desktop on Wayland. A change is accepted when it keeps that promise and
passes the gate.

## Before you write

- Read `roles/README.md`: one role per concern, one catalog entry per role.
- Keep the invariants: no account creation, NetworkManager owns the link,
  Wayland only, no site data, idempotence. `AGENTS.md` states them.
- The human account is the site's. The product adds its desktop groups, its
  locale and the declared applications.

## External contributions

External contributions are **not accepted at this time**. Workstation Edition is
maintained by the owner; unsolicited pull requests and patches may be closed
without review. Issues and discussions are disabled on the repository, so there
is no public defect tracker. This policy does not limit the rights the licences
grant you: the source is free software, and you may fork it and modify it under
the licence terms.

## Support and warranty

No support, service level or warranty is provided, express or implied. The
product is distributed under **AGPL-3.0-or-later**, the documentation under
**CC-BY-SA-4.0** and the Plymouth theme under **GPL-2.0-or-later**, without
warranty, as stated in [`LICENSE`](LICENSE), `LICENSES/` and `NOTICE`. You are
responsible for your deployment and for complying with the licences when you
redistribute or modify the code.

## What a change must carry

1. **A reason that survives a reboot.** A value is declared because the
   machine must have it, not because a blog post did. A measurement names the
   date and the command.
2. **A read-back.** A role that writes a value asserts the running system took
   it. Writing a file is not proof.
3. **No site data.** No address, host name, domain, SSID, secret or customer
   name. The example inventory carries documentation values only.
4. **A second run that changes nothing.** Idempotence is a gate, not a goal.
5. **A console proof for the graphical layer.** GDM, GRUB and Plymouth are not
   proved by `--check`.

## The gate

Run from the repository root; a change is not done until it passes:

```sh
ansible-lint playbooks roles
yamllint -c .yamllint roles playbooks inventories
reuse lint
scripts check tools/scripts/binaries/gate.scs
scripts run tools/scripts/binaries/gate.scs
```

The gate also builds the collection and inspects the archive, so a file that
should not ship fails before the tag.

A change that touches the link, GDM, GRUB, Plymouth or the account groups is
**not** proven by `--check`. Say what was measured, on which machine, and keep a
console path.

## Commits

- One branch per task, `work/<slug>`.
- English, imperative subject; the body says **why**, not what the diff shows.
- One concern per commit.
- Do not commit an artifact (`dist/`, `artifacts/`), a vault or a site
  inventory.

## Licence of a contribution

The product is `AGPL-3.0-or-later`; the documentation is `CC-BY-SA-4.0`; the
Plymouth theme is `GPL-2.0-or-later`. By sending a change you agree that it is
distributed under those terms.

## Reporting a vulnerability

Do not open a public issue. Follow `SECURITY.md`.
