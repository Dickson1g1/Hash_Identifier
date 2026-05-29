# pure identify() function

from .patterns import (
    PREFIX_PATTERNS, HEX_LENGTHS, SHAPE_PATTERNS, NON_HASH_PATTERNS
)
import re

_HEX_RE = re.compile(r'^[0-9a-fA-F]+$')

CONFIDENCE_ORDER = {"high": 0, "medium": 1, "low": 2}


def identify(value: str) -> dict:
    """
    Pure function. Returns:
      {
        "input": str,
        "non_hash": None | {"name": str, "reason": str},
        "candidates": [{"name": str, "confidence": str, "reason": str}, ...]
      }
    No network, no filesystem, no global state mutation.
    """
    value = value.strip()
    result = {"input": value, "non_hash": None, "candidates": []}

    # 1. Non-hash detection (JWT, bare base64)
    for name, rx, reason in NON_HASH_PATTERNS:
        if rx.match(value):
            # JWTs start eyJ which is also valid b64, so check JWT first
            result["non_hash"] = {"name": name, "reason": reason}
            return result

    candidates = []

    # 2. Prefix-based — highest signal
    for name, rx, conf, reason in PREFIX_PATTERNS:
        if rx.match(value):
            candidates.append({"name": name, "confidence": conf, "reason": reason})

    # 3. Pure hex by length
    if _HEX_RE.match(value):
        length = len(value)
        for hex_len, name, conf, reason in HEX_LENGTHS:
            if length == hex_len:
                candidates.append({"name": name, "confidence": conf, "reason": reason})

    # 4. Shape patterns (NetNTLM, MySQL5, DES crypt)
    for name, rx, conf, reason in SHAPE_PATTERNS:
        if rx.match(value):
            candidates.append({"name": name, "confidence": conf, "reason": reason})

    # 5. Sort: high > medium > low, then alphabetically
    candidates.sort(key=lambda c: (CONFIDENCE_ORDER[c["confidence"]], c["name"]))

    result["candidates"] = candidates
    return result
