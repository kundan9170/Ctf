# Krypton — Crypto (levels 0 → 6)

**Connect:** `ssh kryptonN@krypton.labs.overthewire.org -p 2231`
Files live under `/krypton/kryptonN/`. Each level decrypts a file to reveal the
next level's password.

> Levels 1–6 need the live ciphertext files on the server (SSH port 2231),
> which my sandbox can't reach. Methods + exact commands below; Level 0 is
> solved outright.

---

## Level 0 → 1  ✅ solved offline
The site gives the level-1 password base64-encoded: `S1JZUFRPTklTR1JFQVQ=`.
```bash
echo "S1JZUFRPTklTR1JFQVQ=" | base64 -d; echo
```
**krypton1 password = `KRYPTONISGREAT`**

## Level 1 → 2  (ROT13)
`krypton2` file is ROT13-encoded.
```bash
cat /krypton/krypton1/krypton2 | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

## Level 2 → 3  (Caesar cipher)
`krypton3` is a Caesar shift. Read `README`/`keyfile` in `/krypton/krypton2/`.
Easiest path — brute-force all 26 shifts and eyeball the English one:
```bash
CT=$(cat /krypton/krypton2/krypton3)
for k in $(seq 0 25); do
  echo -n "$k: "; echo "$CT" | tr \
    "$(echo {A..Z} | tr -d ' ')" \
    "$(echo {A..Z} | tr -d ' ' | sed "s/.\{$k\}/&\n/" | tac | tr -d '\n')" 2>/dev/null
  echo
done
# Or use the provided encrypt binary with a known-plaintext to derive the shift.
```
(The intended keyed route: make a working dir in `/tmp`, symlink the keyfile,
and run the setuid `encrypt` binary to recover the shift.)

## Level 3 → 4  (monoalphabetic substitution → frequency analysis)
You get `krypton4` plus `found1..3` (extra ciphertext samples for frequency
counts). Break with frequency analysis / an automatic solver:
```bash
cat /krypton/krypton3/krypton4          # copy the ciphertext out
# paste into https://quipqiup.com  (auto-solves substitution)
# or count letters: fold -w1 | sort | uniq -c | sort -rn
```

## Level 4 → 5  (Vigenère, short key)
`krypton5` is Vigenère-encrypted; `found1`/`found2` help find the key length.
```bash
cat /krypton/krypton4/krypton5
# key length via Kasiski/IC, then key via https://www.dcode.fr/vigenere-cipher
```

## Level 5 → 6  (Vigenère, longer key)
Same technique as 4→5, just a longer key — let the solver auto-detect.
```bash
cat /krypton/krypton5/krypton6
# https://www.dcode.fr/vigenere-cipher  (automatic / known-key mode)
```

---
### Quick reference
- **ROT13:** `tr 'A-Za-z' 'N-ZA-Mn-za-m'`
- **Caesar:** brute 26 shifts, pick readable output
- **Substitution:** frequency analysis → quipqiup
- **Vigenère:** Kasiski for key length → dcode.fr for the key
