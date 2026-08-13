#!/usr/bin/env python3
"""Vigenere key recovery by per-column chi-squared against English letter freqs."""
import sys, re

ENG = [8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,0.153,0.772,
       4.025,2.406,6.749,7.507,1.929,0.095,5.987,6.327,9.056,2.758,0.978,
       2.360,0.150,1.974,0.074]

def chi2(counts, n):
    return sum((counts[i] - n*ENG[i]/100)**2 / (n*ENG[i]/100) for i in range(26))

def best_shift(col):
    n = len(col)
    best, bestv = 0, None
    for s in range(26):
        c = [0]*26
        for ch in col:
            c[(ord(ch)-65-s) % 26] += 1
        v = chi2(c, n)
        if bestv is None or v < bestv:
            best, bestv = s, v
    return best

def ic(text):
    n = len(text)
    if n < 2: return 0
    c = [0]*26
    for ch in text: c[ord(ch)-65] += 1
    return sum(x*(x-1) for x in c) / (n*(n-1))

def find_key(ct, klen):
    cols = [ct[i::klen] for i in range(klen)]
    return ''.join(chr(best_shift(c) + 65) for c in cols)

def decrypt(ct, key):
    out = []
    for i, ch in enumerate(ct):
        out.append(chr((ord(ch)-65 - (ord(key[i % len(key)])-65)) % 26 + 65))
    return ''.join(out)

if __name__ == '__main__':
    ct = re.sub(r'[^A-Z]', '', open(sys.argv[1]).read().upper())
    if len(sys.argv) > 2:          # key length given
        klens = [int(sys.argv[2])]
    else:                          # guess via average IC of columns
        klens = None
        scores = []
        for k in range(1, 21):
            avg = sum(ic(ct[i::k]) for i in range(k)) / k
            scores.append((avg, k))
            print(f'  keylen {k:2d}  avgIC={avg:.4f}')
        klens = [max(scores)[1]]
        print(f'\n>>> best key length by IC: {klens[0]}')
    for k in klens:
        key = find_key(ct, k)
        print(f'\nkeylen={k}  KEY={key}')
        print('plaintext head:', decrypt(ct, key)[:200])
