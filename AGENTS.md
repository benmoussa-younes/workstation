# AGENTS.md — Workstation

Ansible roles that turn a freshly installed Debian amd64 machine into a GNOME
desktop on Wayland, shipped as the collection `benmoussa.workstation`. A change
is accepted when it keeps that promise, keeps the role contracts true and passes
the gate.

## Build and test

```sh
ansible-lint playbooks roles
yamllint -c .yamllint roles playbooks inventories
reuse lint
scripts check tools/scripts/binaries/gate.scs
scripts run tools/scripts/binaries/gate.scs      # one VERDICT line, exit 0/1
```

The gate is the repository's single entry point: the tree, the version, the
licences, the collection archive and the secret shapes, then `ansible-lint`,
`yamllint`, `reuse lint` and the playbooks' syntax. It does not change tracked
files.

## Conventions

- Only `ansible.builtin` is used; `requirements.yml` declares no collection.
- A role keeps its `meta/argument_specs.yml` contract and its idempotence.
- A role reads its own change back: writing a file is not proof.
- No site data in a role: an address, a host name, an SSID, a secret or a
  customer name belongs in the site inventory and its vault.
- The graphical layer is proved at the console: GDM, GRUB and Plymouth are not
  proved by `--check`.

## Repository facts

- The collection is `benmoussa.workstation`, version `0.2.2`.
- The product code is `AGPL-3.0-or-later`; the documentation is
  `CC-BY-SA-4.0`; the Plymouth theme is `GPL-2.0-or-later`.
- A release is a signed tag `v<version>` and three assets: the collection
  tarball, the source tarball and `SHA256SUMS`.
- `roles/README.md` is the role catalog; the README is the product's face.

## Commits and releases

- One branch per task, `work/<slug>`; one concern per commit; English,
  imperative subject; the body says why.
- Commits and tags are GPG-signed. A change lands on `main` only when
  `tools/scripts/binaries/gate.scs` prints `VERDICT: PASS`; a release is the maintainer's decision.

## Security

- No secret in a tracked file, a command line or a log; the site owns its
  inventory and vault.
- A vulnerability report is private: follow `SECURITY.md`, never a public issue.

## Maintenance

- Keep `VERSION`, `galaxy.yml`, `roles/identity/defaults/main.yml` and
  `CHANGELOG.md` on the same version.
- A change that touches the link, GDM, GRUB, Plymouth or the account groups
  names what was measured, on which machine, and keeps a console path.
