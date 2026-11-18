# SPDX-FileCopyrightText: 2026 Younes BENMOUSSA <younes.benmoussa@pm.me>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Replace a plaintext Wi-Fi passphrase with the key the radio stores.

Two modes:

  wpa-psk-hash.py --derive     read `<ssid>\\n<passphrase>` on stdin and print
                               the 64-hex PSK: PBKDF2-SHA1, 4096 rounds, 32
                               bytes, the derivation `wpa_passphrase` applies
  wpa-psk-hash.py <file>...    for each file, replace a plaintext `psk` or
                               `wpa-psk` with that key, using the ssid the same
                               file declares

The script never prints a value. Each path gets `hashed`, `already`, `no-psk`,
`no-ssid` or `unreadable`. A value that already is the 64-hex key is left
untouched, so a second run changes nothing. A file the script rewrites is left
root-only: it carries a credential either way.
"""

import hashlib
import os
import re
import sys

HEX_KEY = re.compile(r"^[0-9a-fA-F]{64}$")
SSID_LINE = re.compile(r'^\s*(?:wpa-ssid|ssid)\s*[= ]\s*"?([^"\n]+?)"?\s*$', re.M)
PSK_LINE = re.compile(r'^(\s*(?:wpa-psk|psk)\s*[= ]\s*"?)([^"\n]+?)("?\s*)$', re.M)


def derive(ssid: str, passphrase: str) -> str:
    """The PSK `wpa_passphrase` computes, without the tool or the plaintext."""
    return hashlib.pbkdf2_hmac(
        "sha1", passphrase.encode("utf-8"), ssid.encode("utf-8"), 4096, 32
    ).hex()


def main(arguments: list[str]) -> int:
    if arguments[:1] == ["--derive"]:
        lines = sys.stdin.read().split("\n")
        if len(lines) < 2 or not lines[0] or not lines[1]:
            print("missing ssid or passphrase", file=sys.stderr)
            return 2
        print(derive(lines[0], lines[1]))
        return 0

    for path in arguments:
        try:
            with open(path, encoding="utf-8", errors="surrogateescape") as stream:
                text = stream.read()
        except OSError:
            print(f"{path}: unreadable")
            continue
        found_key = PSK_LINE.search(text)
        if not found_key:
            print(f"{path}: no-psk")
            continue
        value = found_key.group(2)
        if HEX_KEY.match(value):
            print(f"{path}: already")
            continue
        found_ssid = SSID_LINE.search(text)
        if not found_ssid:
            print(f"{path}: no-ssid")
            continue
        text = PSK_LINE.sub(
            lambda match: match.group(1)
            + derive(found_ssid.group(1), value)
            + match.group(3),
            text,
            count=1,
        )
        with open(path, "w", encoding="utf-8", errors="surrogateescape") as stream:
            stream.write(text)
        os.chmod(path, 0o600)
        print(f"{path}: hashed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
