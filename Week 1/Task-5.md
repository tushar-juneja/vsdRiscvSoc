# Task-5: ABI & Register Cheat-Sheet

This is a complete list of the 32 integer registers in RISC-V RV32 architecture, with their:

- Register numbers (x0 to x31)
- ABI (Application Binary Interface) names
- Typical role under the standard calling convention

---

## Step 1: All 32 Integer Registers

| Register | ABI Name   | Role / Calling Convention                                      |
|----------|------------|---------------------------------------------------------------|
| x0       | zero       | Constant zero (always 0) — reads return 0, writes are ignored |
| x1       | ra         | Return address (used by call / ret)                           |
| x2       | sp         | Stack pointer                                                 |
| x3       | gp         | Global pointer                                                |
| x4       | tp         | Thread pointer                                                |
| x5       | t0         | Temporary (caller-saved)                                      |
| x6       | t1         | Temporary (caller-saved)                                      |
| x7       | t2         | Temporary (caller-saved)                                      |
| x8       | s0 or fp   | Saved register or frame pointer (callee-saved)                |
| x9       | s1         | Saved register (callee-saved)                                 |
| x10      | a0         | Argument 0 / return value                                     |
| x11      | a1         | Argument 1 / return value                                     |
| x12      | a2         | Argument 2                                                    |
| x13      | a3         | Argument 3                                                    |
| x14      | a4         | Argument 4                                                    |
| x15      | a5         | Argument 5                                                    |
| x16      | a6         | Argument 6                                                    |
| x17      | a7         | Argument 7                                                    |
| x18      | s2         | Saved register (callee-saved)                                 |
| x19      | s3         | Saved register (callee-saved)                                 |
| x20      | s4         | Saved register (callee-saved)                                 |
| x21      | s5         | Saved register (callee-saved)                                 |
| x22      | s6         | Saved register (callee-saved)                                 |
| x23      | s7         | Saved register (callee-saved)                                 |
| x24      | s8         | Saved register (callee-saved)                                 |
| x25      | s9         | Saved register (callee-saved)                                 |
| x26      | s10        | Saved register (callee-saved)                                 |
| x27      | s11        | Saved register (callee-saved)                                 |
| x28      | t3         | Temporary (caller-saved)                                      |
| x29      | t4         | Temporary (caller-saved)                                      |
| x30      | t5         | Temporary (caller-saved)                                      |
| x31      | t6         | Temporary (caller-saved)                                      |

---

## Step 2: Calling Convention Summary

- **Caller-saved** (`t0–t6`, `a0–a7`): Must be saved by the calling function if needed after a call.
- **Callee-saved** (`s0–s11`): Must be preserved by the called function.
- **sp**: Stack pointer — managed according to stack frame layout.
- **ra**: Stores return address for function calls (`jalr`).
- **zero**: Hardwired to 0 — always safe to read.