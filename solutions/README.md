# Solutions — Team 4 "Traffic Jam Ninjas" CTF doc

The doc covers three OverTheWire wargame tracks. Full per-level walkthroughs:

| Track | Category | Levels | Status | File |
|-------|----------|--------|--------|------|
| **Natas**   | Web Security | 0 → 10 | technique only | [natas.md](natas.md) |
| **Bandit**  | Linux        | 0 → 8  | technique only | [bandit.md](bandit.md) |
| **Krypton** | Crypto       | 0 → 6  | ✅ **solved live** | [krypton.md](krypton.md) |

## Krypton — complete

Run end to end over SSH (`krypton.labs.overthewire.org -p 2231`). Every password
below was **verified by logging in with it**.

| Level | Password | Method |
|-------|----------|--------|
| krypton1 | `KRYPTONISGREAT` | base64 |
| krypton2 | `ROTTEN` | ROT13 |
| krypton3 | `CAESARISEASY` | Caesar, shift 12 |
| krypton4 | `BRUTE` | substitution + frequency analysis |
| krypton5 | `CLEARTEXT` | Vigenère, key `FREKEY` |
| krypton6 | `RANDOM` | Vigenère, key `KEYLENGTH` |

Krypton passwords are **static** (same for every player), so these stay valid.
Full walkthrough with the gotchas in [krypton.md](krypton.md).

## Natas / Bandit

Not run live — these have **rotating** passwords, so a captured value would go
stale anyway and each level has to be chained from the previous one. The files
give the exact technique + copy-paste command per level; run them from your own
machine and feed each recovered password into the next step.

One offline-solvable piece: **Natas 8 secret** = `oubWYf2kBq` (reverse
`bin2hex(strrev(base64_encode(x)))`). Submitting it to the live server is what
returns the natas9 password.

Want these driven live too? Say so — the OTW hosts are reachable from this
machine, so the same approach used for Krypton works for Bandit (port 2220) and
Natas (HTTP basic auth).

## Crypto solvers

- [`../scripts/krypton.py`](../scripts/krypton.py) — `rot13`, `caesar` (all 26
  shifts + auto-detect), `vigenere --key`, `freq`. Reads ciphertext on stdin.
- [`../scripts/vig.py`](../scripts/vig.py) — Vigenère key recovery: chi-squared
  per column for a known key length, or an index-of-coincidence scan when the
  key length is unknown. This is what broke Krypton 4→5 and 5→6.
