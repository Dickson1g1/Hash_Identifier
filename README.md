```
 ██╗  ██╗ █████╗ ███████╗██╗  ██╗      ██╗██████╗ 
 ██║  ██║██╔══██╗██╔════╝██║  ██║      ██║██╔══██╗
 ███████║███████║███████╗███████║█████╗██║██║  ██║
 ██╔══██║██╔══██║╚════██║██╔══██║╚════╝██║██║  ██║
 ██║  ██║██║  ██║███████║██║  ██║      ██║██████╔╝
 ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝      ╚═╝╚═════╝ 

   identify hashes by prefix · length · shape
```

# Hash-id

> Identify 30+ cryptographic hash formats instantly — ranked candidates,
> colored output, shell-friendly exit codes. No network. No filesystem. Pure Python.

---

## What it does

Feed `hash-id` any string and it tells you what hash format it is (or isn't).
It returns a ranked list of candidates, each with a **confidence level** and a
one-line reason so you always know *why* a match was made.

```
$ python hash_id.py '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LedYT7.OFcXGBSVK.'

Input:  $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LedYT7.OFcXGBSVK.
Length: 60

╭────────────┬───────────┬────────────────────────────────────────╮
│ Confidence │ Hash type │ Reason                                 │
├────────────┼───────────┼────────────────────────────────────────┤
│ ● high     │ bcrypt    │ bcrypt prefix $2b/$2a/$2y + 53-char body│
╰────────────┴───────────┴────────────────────────────────────────╯
```

---

## Features

- **30+ hash formats** identified by prefix — bcrypt, argon2id, argon2i,
  argon2d, md5crypt, sha256crypt, sha512crypt, apr1, scrypt, phpass,
  Drupal7, pbkdf2-sha256/sha512/sha1, {SSHA}, {SHA}, {MD5}, {CRYPT},
  Django SHA1/MD5, Solaris md5, and more
- **Hex hashes by length** — MD5, NTLM, MD4 (32), SHA-1 / RIPEMD-160 (40),
  SHA-224 (56), SHA-256 / BLAKE2s / SHA3-256 (64), SHA-384 (96),
  SHA-512 / BLAKE2b / SHA3-512 (128)
- **Shape-based detection** — MySQL5 (`*` + 40 hex), NetNTLMv1, NetNTLMv2,
  13-char traditional DES crypt
- **Non-hash detection** — JWTs and raw base64 blobs are recognized and
  explained rather than misidentified
- **Ranked candidates** with `high / medium / low` confidence and a reason
  for every guess
- **Pure-function core** — `identify()` has no network calls, no filesystem
  access, no global state mutation; instant runtime
- **Rich terminal output** — colored table via the `rich` library
- **Clean exit codes** for shell scripting: `0` found · `1` non-hash · `2` unknown

---

## Requirements

- Python 3.8+
- [`rich`](https://github.com/Textualize/rich)

```bash
pip install rich
```

---

## Installation

```bash
git clone https://github.com/Dickson1g1/password-manager.git
cd hash-id
python3 -m venv .venv && source .venv/bin/activate
pip install rich
chmod +x hash_id.py
```

---

## Usage

```bash
# Pass a hash directly
python hash_id.py ''

# Pipe from stdin
echo -n '5d41402abc4b2a76b9719d911017c592' | python hash_id.py

# JSON output (great for scripting with jq)
python hash_id.py '' --json

# Symlink for system-wide use
ln -s "$(pwd)/hash_id.py" ~/.local/bin/hash_id
```

### Examples

```bash
# bcrypt
python hash_id.py '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LedYT7.OFcXGBSVK.'

# argon2id
python hash_id.py '$argon2id$v=19$m=65536,t=2,p=1$c29tZXNhbHQ$RdescudvJCsgt3ub+b+dWRWJTmaaJObG'

# SHA-256 hex
python hash_id.py 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'

# Django PBKDF2
python hash_id.py 'pbkdf2_sha256$260000$abc$xyz'

# JWT detection
python hash_id.py 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'

# NetNTLMv2
python hash_id.py 'admin::WORKGROUP:1122334455667788:abc123:0101000000000000'
```

---

## Exit codes

| Code | Meaning |
|------|---------|
| `0`  | One or more candidates found |
| `1`  | Input is a non-hash (JWT, base64, etc.) |
| `2`  | No matching format found |
| `3`  | No input provided |

---

## Project structure

```
hash-id/
├── hash_id/
│   ├── __init__.py
│   ├── patterns.py      # all regex / length rules (pure data)
│   ├── identifier.py    # identify() — pure function, no I/O
│   └── display.py       # rich table rendering
├── hash_id.py           # CLI entrypoint
└── tests/
    └── test_identifier.py
```

---

## Running tests

```bash
python tests/test_identifier.py
```

---

## Use cases

- CTF / capture-the-flag challenges — quickly identify an unknown hash before cracking
- Penetration testing — recognize hash formats from credential dumps
- Security code review — verify what algorithm a system is actually using
- Digital forensics — identify hashes in memory dumps or config files

---

## License

MIT — do whatever you want, attribution appreciated.
