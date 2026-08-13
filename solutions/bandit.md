# Bandit — Linux Playground (levels 0 → 8)

**Connect:** `ssh bandit0@bandit.labs.overthewire.org -p 2220`
Level 0 password: `bandit0`. Each level's password logs into the next user
(`banditN`). Run each command *after* logging into the matching user.

> These need an interactive SSH session on port 2220, which my sandbox can't
> open (HTTPS-only egress, host not allowlisted). Commands below are exact —
> run them from your own terminal.

---

## Level 0 → 1
Log in, read the readme.
```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220     # password: bandit0
cat readme
```

## Level 1 → 2  (file literally named `-`)
A bare `-` means stdin to most tools, so path-qualify it.
```bash
cat ./-
```

## Level 2 → 3  (spaces in the filename)
Quote it or escape the spaces.
```bash
cat "spaces in this filename"
# or: cat spaces\ in\ this\ filename
```

## Level 3 → 4  (hidden file)
Password is a dotfile inside `inhere/`.
```bash
ls -la inhere/
cat "inhere/....Hiding-From-You"     # use the exact dotfile name ls shows
```

## Level 4 → 5  (only human-readable file)
`inhere/` holds `-file00 … -file09`; only one is ASCII text.
```bash
file inhere/-file*
cat inhere/-file07                   # whichever `file` reports as ASCII text
```

## Level 5 → 6  (find by properties)
Human-readable, exactly 1033 bytes, not executable.
```bash
find inhere/ -type f -size 1033c ! -executable -readable
cat <that path>
```

## Level 6 → 7  (find across the whole system)
Owned by user `bandit7`, group `bandit6`, 33 bytes.
```bash
find / -type f -user bandit7 -group bandit6 -size 33c 2>/dev/null
cat <that path>
```

## Level 7 → 8  (grep next to a word)
Password sits beside the word `millionth` in `data.txt`.
```bash
grep millionth data.txt
```

---
**Tip:** the classic gotchas here are (1) `-` and spaces need path/quoting, and
(2) `find` with `-size Nc`, `-user`, `-group`, `! -executable`, `-readable`,
and `2>/dev/null` to silence permission noise.
