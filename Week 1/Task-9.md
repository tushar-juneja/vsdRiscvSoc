# Task-9: Inline Assembly Basics

We have to write a c program that reads the cycle count of RISCV cycle counter using CSR (control status and register) using inline assembly

## Step 1: Write c code
```bash
vim read_cycle.c

unsigned int read_cycle() {
     unsigned int cycle;
     asm volatile("csrr %0, cycle": "=r"(cycle));
     return cycle;
}
```

## Generation of assembly
```bash
riscv32-unknown-elf-gcc -o read_cycle.s -S read_cycle.c
```
![Generated assembly file](/Week%201/assets/Task-9/inline_assembly.png)

In this file, we can see that our riscv instruction is intact:
`csrr a5, cycle`

## Explanation

`unsigned int read_cycle()` defines a function named read_cycle that returns an unsigned integer value containing the cycle counter value

`unsigned int cycle` we declare an unsigned integer to store the cycle counter value read from the csr register

`asm` allows to write inline assembly in c

`volatile` tells the compiler not to make any optimizations or reorder this block. It's important because this reads from a hardware register

`csrr %0, cycle`
- csrr stand for control and status register read. This instruction is used to read from csr.
- ***cycle*** is an alias for CSR 0xC00, cycle counter.
- %0 is a placeholder for output register

`=r`
- `=` is the output operand
- `r` tells the compiler to store the value returned from csr in a general purpose register
- `r(cycle)` tells the compiler to copy/store the value stored in register into c, `cycle` variable