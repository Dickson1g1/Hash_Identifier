# all regex/length rules

import re

# (name, compiled_regex, confidence, reason)
PREFIX_PATTERNS = [
    ("bcrypt",        re.compile(r'^\$2[aby]\$\d{2}\$.{53}$'),          "high",   "bcrypt prefix $2b/$2a/$2y + 53-char body"),
    ("argon2id",      re.compile(r'^\$argon2id\$'),                      "high",   "argon2id prefix"),
    ("argon2i",       re.compile(r'^\$argon2i\$'),                       "high",   "argon2i prefix"),
    ("argon2d",       re.compile(r'^\$argon2d\$'),                       "high",   "argon2d prefix"),
    ("md5crypt",      re.compile(r'^\$1\$'),                             "high",   "$1$ md5crypt prefix"),
    ("sha256crypt",   re.compile(r'^\$5\$'),                             "high",   "$5$ sha256crypt prefix"),
    ("sha512crypt",   re.compile(r'^\$6\$'),                             "high",   "$6$ sha512crypt prefix"),
    ("apr1-md5",      re.compile(r'^\$apr1\$'),                          "high",   "Apache APR1-MD5 prefix"),
    ("scrypt",        re.compile(r'^\$scrypt\$'),                        "high",   "scrypt prefix"),
    ("pbkdf2-sha256", re.compile(r'^pbkdf2_sha256\$'),                   "high",   "Django PBKDF2-SHA256 prefix"),
    ("pbkdf2-sha512", re.compile(r'^pbkdf2_sha512\$'),                   "high",   "Django PBKDF2-SHA512 prefix"),
    ("pbkdf2-sha1",   re.compile(r'^pbkdf2_sha1\$'),                     "high",   "Django PBKDF2-SHA1 prefix"),
    ("sha1django",    re.compile(r'^sha1\$'),                            "high",   "Django SHA1 prefix"),
    ("md5django",     re.compile(r'^md5\$'),                             "high",   "Django MD5 prefix"),
    ("SSHA",          re.compile(r'^\{SSHA\}'),                          "high",   "{SSHA} OpenLDAP prefix"),
    ("SHA-ldap",      re.compile(r'^\{SHA\}'),                           "high",   "{SHA} OpenLDAP prefix"),
    ("MD5-ldap",      re.compile(r'^\{MD5\}'),                           "high",   "{MD5} OpenLDAP prefix"),
    ("CRYPT-ldap",    re.compile(r'^\{CRYPT\}'),                         "high",   "{CRYPT} OpenLDAP prefix"),
    ("phpass",        re.compile(r'^\$P\$|^\$H\$'),                      "high",   "phpass $P$/$H$ prefix"),
    ("Drupal7",       re.compile(r'^\$S\$'),                             "high",   "Drupal7 $S$ prefix"),
    ("WoltLab",       re.compile(r'^blazefire:'),                        "high",   "WoltLab blazefire: prefix"),
    ("sha512-b64",    re.compile(r'^\$sha512\$'),                        "high",   "$sha512$ prefix"),
    ("md5-b64",       re.compile(r'^\$md5\$|\$md5,'),                    "high",   "Solaris $md5$ prefix"),
]

HEX_LENGTHS = [
    (32,  "MD5 / NTLM / MD4",          "medium", "32 hex chars matches MD5, NTLM, MD4"),
    (40,  "SHA-1 / RIPEMD-160",        "medium", "40 hex chars matches SHA-1 or RIPEMD-160"),
    (56,  "SHA-224 / SHA3-224",        "medium", "56 hex chars matches SHA-224"),
    (64,  "SHA-256 / BLAKE2s / SHA3-256","medium","64 hex chars matches SHA-256 family"),
    (96,  "SHA-384 / SHA3-384",        "medium", "96 hex chars matches SHA-384"),
    (128, "SHA-512 / BLAKE2b / SHA3-512","medium","128 hex chars matches SHA-512 family"),
    (8,   "CRC-32",                    "low",    "8 hex chars, possible CRC-32"),
    (16,  "CRC-64 / half-MD5",         "low",    "16 hex chars, possible truncated hash"),
]

SHAPE_PATTERNS = [
    ("MySQL4+",      re.compile(r'^\*[0-9A-Fa-f]{40}$'),               "high",   "MySQL5 asterisk + 40 hex"),
    ("DES-crypt",    re.compile(r'^[./A-Za-z0-9]{13}$'),               "medium", "13-char DES crypt charset"),
    ("NetNTLMv1",    re.compile(r'^[^:]+::[^:]+:[0-9A-Fa-f]{48}:[0-9A-Fa-f]{32}:[0-9A-Fa-f]{16}$'),
                                                                        "high",   "NetNTLMv1 colon structure"),
    ("NetNTLMv2",    re.compile(r'^[^:]+::[^:]+:[0-9A-Fa-f]{16}:[0-9A-Fa-f]{32}:.+$'),
                                                                        "high",   "NetNTLMv2 colon structure"),
]

NON_HASH_PATTERNS = [
    ("JWT",          re.compile(r'^eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$'),
                                                                        "JSON Web Token (3-part base64url)"),
    ("Base64-blob",  re.compile(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$'),
                                                                        "Base64-encoded blob, not a hash"),
]
