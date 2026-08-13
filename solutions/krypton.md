# Krypton — Crypto (levels 0 → 6) — ✅ ALL SOLVED

**Connect:** `ssh kryptonN@krypton.labs.overthewire.org -p 2231`
Files live under **`/krypton/kryptonN/`** (absolute path at the filesystem root —
NOT your home dir, which only holds `.bashrc`/`.profile`). As user `kryptonN`
you can read `/krypton/kryptonN/` only.

All six levels were run live over SSH and every password below is **verified by
actually logging in with it**. Krypton passwords are static (same for everyone),
unlike Natas which rotate.

---

## Answers

| Level | Password | Method |
|-------|----------|--------|
| krypton1 | `KRYPTONISGREAT` | base64 |
| krypton2 | `ROTTEN` | ROT13 |
| krypton3 | `CAESARISEASY` | Caesar, shift 12 |
| krypton4 | `BRUTE` | monoalphabetic substitution + frequency analysis |
| krypton5 | `CLEARTEXT` | Vigenère, key `FREKEY` (len 6) |
| krypton6 | `RANDOM` | Vigenère, key `KEYLENGTH` (len 9) |

---

## Level 0 → 1 — base64
The level page gives the password base64-encoded.
```bash
echo "S1JZUFRPTklTR1JFQVQ=" | base64 -d; echo
# KRYPTONISGREAT
```
**→ krypton1 = `KRYPTONISGREAT`**

## Level 1 → 2 — ROT13
`/krypton/krypton1/krypton2` contains `YRIRY GJB CNFFJBEQ EBGGRA`.
```bash
cat /krypton/krypton1/krypton2 | tr 'A-Za-z' 'N-ZA-Mn-za-m'
# LEVEL TWO PASSWORD ROTTEN
```
**→ krypton2 = `ROTTEN`**

## Level 2 → 3 — Caesar
`/krypton/krypton2/krypton3` contains `OMQEMDUEQMEK`. The README dangles a
setuid `encrypt` binary (encrypt a known plaintext, read off the shift) but with
only 12 characters brute force is instant — 26 shifts, one is English.
```bash
cat /krypton/krypton2/krypton3 | python3 krypton.py caesar
# shift 12 -> CAESARISEASY
```
**→ krypton3 = `CAESARISEASY`**

## Level 3 → 4 — monoalphabetic substitution
`/krypton/krypton3/` has `krypton4` plus `found1..3` (extra ciphertext so the
letter counts are meaningful). Ciphertext:

```
KSVVW BGSJD SVSIS VXBMN YQUUK BNWCU ANMJS
```

The crib does it in one step — a 35-letter message in this position is almost
certainly `WELLDONETHELEVELFOURPASSWORDIS____`. Aligning that gives the mapping,
and applying it to `found3` yields clean English (it's Poe's *The Gold-Bug*),
which confirms the key:

```
cipher: A B C D E G I J K L M N Q S T U V W X Y
plain:  b o i h g n v t w y u r a e m s l d f p
```
```
KSVVWBGSJDSVSISVXBMNYQUUKBNWCUANMJS
-> WELLDONETHELEVELFOURPASSWORDISBRUTE
```
Frequency analysis / <https://quipqiup.com> gets you the same key without the crib.

**→ krypton4 = `BRUTE`**

## Level 4 → 5 — Vigenère, key length known (6)
`/krypton/krypton4/krypton5` = `HCIKVRJOX`. You're told the key is 6 long, so
split `found1` into 6 columns and chi-squared each column against English letter
frequencies.

> ⚠️ Analyse `found1` and `found2` **separately**. Concatenating them breaks the
> keystream alignment (found1 is 1450 letters, not a multiple of 6) and you get a
> garbage key. Both files independently give the same key.

```bash
python3 vig.py found1 6     # KEY=FREKEY
# plaintext: THESOLDIERWITHTHEGREENWHISKERS...  (The Wizard of Oz)
python3 vig.py found2 6     # KEY=FREKEY  (independent confirmation)
```
Then `HCIKVRJOX` − `FREKEY` = `CLEARTEXT`.

**→ krypton5 = `CLEARTEXT`**

## Level 5 → 6 — Vigenère, key length unknown
`/krypton/krypton5/krypton6` = `BELOSZ`. Recover the key length first with the
index of coincidence — English sits near 0.067, random near 0.038:

```
keylen  6  avgIC=0.0518
keylen  9  avgIC=0.0700   <-- peak
keylen 12  avgIC=0.0523
keylen 18  avgIC=0.0708   <-- multiple of 9, not a separate answer
```

Key length **9**, and the key turns out to be the joke `KEYLENGTH`. Plaintext is
*A Tale of Two Cities* (`ITWASTHEBESTOFTIMES...`). Then
`BELOSZ` − `KEYLENGTH` = `RANDOM`.

**→ krypton6 = `RANDOM`** (verified: `ssh krypton6@... -p 2231` → `whoami` = `krypton6`)

---

## Tooling

Two scripts, both in this repo:

- [`../scripts/krypton.py`](../scripts/krypton.py) — `rot13`, `caesar` (26 shifts
  + auto-detect), `vigenere --key`, `freq`. Reads stdin.
- [`../scripts/vig.py`](../scripts/vig.py) — Vigenère key recovery. With a key
  length it chi-squares each column; without one it prints the IC table per
  candidate length and picks the peak. This is what broke levels 4→5 and 5→6.

```bash
python3 scripts/vig.py ciphertext.txt 6   # known key length
python3 scripts/vig.py ciphertext.txt     # unknown -> IC scan, then solve
```

Level 6 (`krypton6`) is where the doc stops; that box holds `encrypt6`,
`onetime` and `krypton7` if you want to keep going past the assignment.
