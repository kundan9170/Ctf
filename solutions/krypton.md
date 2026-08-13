# Krypton — Crypto (levels 0 → 6)

**Connect:** `ssh kryptonN@krypton.labs.overthewire.org -p 2231`
Files live under **`/krypton/kryptonN/`** (absolute path at the filesystem root —
NOT your home dir, which only holds `.bashrc`/`.profile`). As user `kryptonN`
you can read the `/krypton/kryptonN/` folder only.

**Tool:** all decoding uses the tested solver at
[`../scripts/krypton.py`](../scripts/krypton.py). Copy it to the box (or just
paste the ciphertext to me). It reads ciphertext on **stdin**.

> Krypton passwords are **static** (same for everyone), unlike Natas which
> rotate — so the confirmed answers below are real. My sandbox can't SSH to the
> server, so levels needing your specific file: `cat` it and pipe to the tool.

---

## Level 0 → 1  ✅ SOLVED
Site gives the level-1 password base64-encoded.
```bash
echo "S1JZUFRPTklTR1JFQVQ=" | base64 -d; echo
```
**→ krypton1 password = `KRYPTONISGREAT`**

## Level 1 → 2  ✅ SOLVED (ROT13)
`/krypton/krypton1/krypton2` contains `YRIRY GJB CNFFJBEQ EBGGRA`.
```bash
cat /krypton/krypton1/krypton2 | python3 krypton.py rot13
# LEVEL TWO PASSWORD ROTTEN
```
**→ krypton2 password = `ROTTEN`**

## Level 2 → 3  (Caesar) — THE FIXED ONE
The old `tr`/`sed` brute-forcer was broken. Use the solver — it prints all 26
shifts **and auto-picks the English one**:
```bash
cat /krypton/krypton2/krypton3 | python3 krypton.py caesar
```
The `>>> best guess:` line at the bottom is your plaintext. The decoded text
spells out the level-3 password in the clear (it reads like
`...THE PASSWORD IS <WORD>`).

If you want the single shift once you know it (e.g. 21):
```bash
cat /krypton/krypton2/krypton3 | python3 krypton.py caesar --key 21
```
> **Paste me the `krypton3` file contents and I'll return the exact password.**

## Level 3 → 4  (monoalphabetic substitution → frequency analysis)
You also get `found1..3` (extra ciphertext for better letter counts). Get the
frequency table, then finish on quipqiup:
```bash
cat /krypton/krypton3/krypton4 /krypton/krypton3/found* | python3 krypton.py freq
# map most-common cipher letter -> E, etc.  Then:
#   paste krypton4 ciphertext into https://quipqiup.com  (auto-solves)
```
> Paste me the `krypton4` ciphertext (and `found*` if you have them) and I'll
> break the substitution here.

## Level 4 → 5  (Vigenère, short key)
`found1`/`found2` help find the key length (Kasiski / index of coincidence).
Once you have the key, decode:
```bash
cat /krypton/krypton4/krypton5 | python3 krypton.py vigenere --key <KEY>
```
Finding the key: paste the ciphertext into
<https://www.dcode.fr/vigenere-cipher> (automatic mode) — or send it to me.

## Level 5 → 6  (Vigenère, longer key)
Same method, longer key — let the solver auto-detect:
```bash
cat /krypton/krypton5/krypton6 | python3 krypton.py vigenere --key <KEY>
```
> Paste me `krypton6` (plus `found*`) and I'll recover the key + plaintext.

---
## Confirmed so far
| Level | Password | Method |
|-------|----------|--------|
| krypton1 | `KRYPTONISGREAT` | base64 |
| krypton2 | `ROTTEN` | ROT13 |
| krypton3 | *(run Caesar solver / paste ciphertext)* | Caesar |
| krypton4 | *(paste ciphertext)* | substitution |
| krypton5 | *(paste ciphertext)* | Vigenère |
| krypton6 | *(paste ciphertext)* | Vigenère |

## The solver
`scripts/krypton.py` modes: `rot13`, `caesar [--key N]`, `vigenere --key WORD`,
`freq`. Reads stdin. Tested against known inputs (ROT13, Caesar shift-3,
Vigenère round-trip) — all pass.
