# Solutions — Team 4 "Traffic Jam Ninjas" CTF doc

The doc covers three OverTheWire wargame tracks. Full per-level walkthroughs:

| Track | Category | Levels | File |
|-------|----------|--------|------|
| **Natas**   | Web Security | 0 → 10 | [natas.md](natas.md) |
| **Bandit**  | Linux        | 0 → 8  | [bandit.md](bandit.md) |
| **Krypton** | Crypto       | 0 → 6  | [krypton.md](krypton.md) |

## Important: why the passwords aren't filled in

I run inside a sandbox whose network egress is locked to an allowlist
(package registries + Anthropic only). Every `*.labs.overthewire.org` host is
blocked, and there's no SSH client/port, so I **cannot reach the live servers**
to chain through the levels and capture the rotating passwords. Routing around
an org egress policy isn't permitted.

So each file gives the **exact technique + copy-paste command** for every
level. Run them from your own machine (which can reach OTW), and feed each
recovered password into the next step.

## Solved fully offline (no server needed)

| Challenge | Answer | How |
|-----------|--------|-----|
| **Krypton 0 → 1** | `KRYPTONISGREAT` | `base64 -d` of `S1JZUFRPTklTR1JFQVQ=` |
| **Natas 8 secret** | `oubWYf2kBq` | reverse `bin2hex(strrev(base64_encode(x)))` |

(The Natas 8 *secret* is offline-solvable; submitting it to the live server is
what returns the natas9 password.)

## If you want me to actually run these live

Two options:
1. **Paste the live page/file contents here** — e.g. run the natas0 curl on
   your side, paste the HTML, and I'll extract the password and hand you the
   next exact command, level by level. Effectively I drive, you're the network.
2. **Ask your admin to allowlist** `*.labs.overthewire.org` for this session's
   egress (and enable SSH to port 2220/2231) — then I can chain them end to end.
