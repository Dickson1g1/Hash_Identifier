import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hash_id.identifier import identify

def names(result):
    return [c["name"] for c in result["candidates"]]

def test_bcrypt():
    h = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LedYT7.OFcXGBSVK."
    r = identify(h)
    assert "bcrypt" in names(r)

def test_md5_hex():
    r = identify("5d41402abc4b2a76b9719d911017c592")
    assert any("MD5" in n for n in names(r))

def test_sha256_hex():
    r = identify("a" * 64)
    assert any("SHA-256" in n for n in names(r))

def test_sha512_hex():
    r = identify("b" * 128)
    assert any("SHA-512" in n for n in names(r))

def test_argon2id():
    h = "$argon2id$v=19$m=65536,t=2,p=1$c29tZXNhbHQ$RdescudvJCsgt3ub+b+dWRWJTmaaJObG"
    r = identify(h)
    assert "argon2id" in names(r)

def test_pbkdf2():
    h = "pbkdf2_sha256$260000$abc$xyz"
    r = identify(h)
    assert "pbkdf2-sha256" in names(r)

def test_mysql5():
    r = identify("*6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9")
    assert "MySQL4+" in names(r)

def test_jwt():
    h = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    r = identify(h)
    assert r["non_hash"] is not None
    assert r["non_hash"]["name"] == "JWT"

def test_unknown():
    r = identify("notahash!!!")
    assert r["candidates"] == []

if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed")
