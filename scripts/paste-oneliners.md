# Krypton — copy-paste one-liners (no file transfer needed)

Paste these straight into the OverTheWire terminal. Each reads the cipher file
directly and decodes it in place. All tested. `python3` is on the krypton box;
if it ever says "command not found", swap `python3` → `python`.

---

## krypton1 → 2  (ROT13)  — reads /krypton/krypton1/krypton2
```bash
cat /krypton/krypton1/krypton2 | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```
→ `LEVEL TWO PASSWORD ROTTEN`  (password: **ROTTEN**)

## krypton2 → 3  (Caesar)  — reads /krypton/krypton2/krypton3
Prints all 26 shifts **and** auto-flags the English one on the last line:
```bash
python3 -c "d=open('/krypton/krypton2/krypton3').read().strip(); s=lambda t:sum(t.upper().count(w)*len(w) for w in(' THE ','PASSWORD',' IS ','LEVEL','THE','ING','ER','AND')); r=lambda n:''.join(chr((ord(c)-65-n)%26+65) if 'A'<=c<='Z' else chr((ord(c)-97-n)%26+97) if 'a'<=c<='z' else c for c in d); [print(f'{n:2d}: {r(n)}') for n in range(26)]; b=max(range(26),key=lambda n:s(r(n))); print(f'>>> BEST: shift {b} -> {r(b)}')"
```
The `>>> BEST` line is your plaintext; it spells out the password.

## krypton3 → 4  (substitution → frequency)  — reads krypton4 + found*
Frequency table to seed a substitution solve, then finish on quipqiup.com:
```bash
cat /krypton/krypton3/krypton4 /krypton/krypton3/found* 2>/dev/null | python3 -c "import sys,collections; d=sys.stdin.read().upper(); c=collections.Counter(x for x in d if x.isalpha()); print('cipher freq:', ' '.join(f'{k}:{v}' for k,v in c.most_common())); print('english   :  E T A O I N S H R D L C U ...')"
echo '--- ciphertext to paste into https://quipqiup.com ---'; cat /krypton/krypton3/krypton4
```

## krypton4 → 5  (Vigenère, once you know the KEY)
```bash
KEY=REPLACEME; python3 -c "import sys; k='$KEY'.upper(); d=open('/krypton/krypton4/krypton5').read(); i=0; out=''
for c in d:
    if c.isalpha(): out+=chr((ord(c.upper())-65-(ord(k[i%len(k)])-65))%26+65); i+=1
    else: out+=c
print(out)"
```
Find the KEY: paste the ciphertext into <https://www.dcode.fr/vigenere-cipher>
(automatic mode), or send it to me.

## krypton5 → 6  (Vigenère, longer key)
Same as above, pointing at `/krypton/krypton5/krypton6`:
```bash
KEY=REPLACEME; python3 -c "import sys; k='$KEY'.upper(); d=open('/krypton/krypton5/krypton6').read(); i=0; out=''
for c in d:
    if c.isalpha(): out+=chr((ord(c.upper())-65-(ord(k[i%len(k)])-65))%26+65); i+=1
    else: out+=c
print(out)"
```

---
### Can't run it / want it done for you?
Just `cat` the file and paste the ciphertext to me — I'll decode it and hand
back the password. Zero tooling needed on your side.
