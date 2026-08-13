#!/usr/bin/env python3
"""Krypton crypto solver — ROT13, Caesar (all shifts + auto), Vigenere.

Usage:
  cat cipher | ./krypton.py rot13
  cat cipher | ./krypton.py caesar            # print all 26 shifts
  cat cipher | ./krypton.py caesar --key 21   # single shift (0-25)
  cat cipher | ./krypton.py vigenere --key CLEARTEXT
  cat cipher | ./krypton.py freq              # letter-frequency table (for substitution)

Reads ciphertext from stdin (or a file arg). Non-letters pass through
untouched; case is preserved. For Caesar '--key N' means "the plaintext was
shifted +N to make the ciphertext", so decoding subtracts N.
"""
import sys, string
from collections import Counter

# English letter frequency order, most→least common
ENG = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

def rot(text, n):
    out = []
    for c in text:
        if c.isupper():
            out.append(chr((ord(c) - 65 - n) % 26 + 65))
        elif c.islower():
            out.append(chr((ord(c) - 97 - n) % 26 + 97))
        else:
            out.append(c)
    return "".join(out)

def score(text):
    """Rough 'englishness' — count of letters landing in common bigrams/words."""
    t = text.upper()
    hits = 0
    for w in (" THE ", " AND ", "PASSWORD", "LEVEL", " IS ", "CAESAR", "THE", "ING"):
        hits += t.count(w) * len(w)
    # plus fraction of chars that are spaces/vowels in sane ratio
    return hits

def vigenere(text, key):
    key = [ord(k.upper()) - 65 for k in key if k.isalpha()]
    if not key:
        return text
    out, ki = [], 0
    for c in text:
        if c.isalpha():
            shift = key[ki % len(key)]
            base = 65 if c.isupper() else 97
            out.append(chr((ord(c) - base - shift) % 26 + base))
            ki += 1
        else:
            out.append(c)
    return "".join(out)

def freq(text):
    c = Counter(ch for ch in text.upper() if ch.isalpha())
    total = sum(c.values()) or 1
    rows = []
    for ch, n in c.most_common():
        rows.append(f"  {ch}: {n:4d}  ({100*n/total:4.1f}%)")
    guess = "".join(ch for ch, _ in c.most_common())
    return "\n".join(rows) + f"\n\ncipher freq order: {guess}\nenglish freq order: {ENG}\n(map most-common cipher letter -> E, etc., then use quipqiup.com)"

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(1)
    mode = args[0]
    key = None
    if "--key" in args:
        key = args[args.index("--key") + 1]
    # data: last non-flag arg that is a file, else stdin
    data = sys.stdin.read()
    data = data.rstrip("\n")

    if mode == "rot13":
        print(rot(data, 13))
    elif mode == "caesar":
        if key is not None:
            print(rot(data, int(key)))
        else:
            best = None
            for n in range(26):
                dec = rot(data, n)
                s = score(dec)
                marker = ""
                if best is None or s > best[0]:
                    best = (s, n, dec)
                print(f"shift {n:2d} (dec -{n:2d}): {dec}")
            print(f"\n>>> best guess: shift {best[1]} (score {best[0]})")
            print(f">>> {best[2]}")
    elif mode == "vigenere":
        if not key:
            print("vigenere needs --key KEYWORD"); sys.exit(1)
        print(vigenere(data, key))
    elif mode == "freq":
        print(freq(data))
    else:
        print(f"unknown mode: {mode}"); print(__doc__); sys.exit(1)

if __name__ == "__main__":
    main()
