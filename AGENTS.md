# AGENTS.md — Workstation

## Build and test

```sh
ansible-lint playbooks roles
yamllint -c .yamllint roles playbooks inventories
reuse lint
scripts check tools/scripts/binaries/gate.scs
scripts run tools/scripts/binaries/gate.scs      # one VERDICT line, exit 0/1
```

The gate is the repository's single entry point. It checks the tree, the
version, the licences, the collection archive and the secret shapes, then runs
`ansible-lint`, `yamllint`, `reuse lint` and the playbooks' syntax. It does not
change tracked files.

## Repository facts

- The collection is `benmoussa.workstation`, version `0.1.0`.
- The product code is `AGPL-3.0-or-later`; the documentation is
  `CC-BY-SA-4.0`; the Plymouth theme is `GPL-2.0-or-later`.
- Only `ansible.builtin` is used; `requirements.yml` declares no collection.
- There is no `docs/` and no `.opencode/`: the plan and the board live outside
  the repository.
- A release is a signed tag `v<version>` and three assets: the collection
  tarball, the source tarball and `SHA256SUMS`.
- GDM, GRUB and Plymouth are verified at the console; a `--check` run is not
  that proof.

## Maintenance

- Keep `VERSION`, `galaxy.yml`, `roles/identity/defaults/main.yml` and
  `CHANGELOG.md` on the same version.
- A role keeps its `meta/argument_specs.yml` contract and its idempotence.
- No site data in a role: an address, a host name, an SSID or a secret belongs
  in the site inventory.
