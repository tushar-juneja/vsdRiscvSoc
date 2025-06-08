# Task-11: Linker Script 101

In this section, we'll be writing a linker script that will specify from which address the program's code and data would be stored and where. Also we'll discuss why the flash and sram have different addresses. 

## What is Linker Script and why do we need it?

It is a file that specifies how the program's code and data are arranged in memory when the program is compiled and linked. In a typical OS environment, the OS handles
- how and where the program code is loaded
- where the data is loaded
- what is going to be the entry point (typically main)

But in bare-metal or embedded programming everything we have to manage everything ourselves. If the program access the wrong memory location, it could either do nothing or crash.

A linker script helps us to specify:
- where to store the program code (.text)
- where to store program data (.data)
- where to reserve space for uninitialized variables (.bss)
- what is going to be the entry point

---

## Linker Script
The below linker script places .text at 0x00000000 (flash) and .data at 0x10000000 (ram) for RV32IMC

```ld
ENTRY(_start)

SECTIONS
{
  /* Code section (flash) */
  .text 0x00000000 : {
    *(.text*)
    *(.rodata*)     /* Include read-only data like string literals */
  }

  /* Initialized data section (RAM) */
  .data 0x10000000 : {
    *(.data*)
  }

  /* Uninitialized data (BSS) */
  .bss (ALIGN(4)) : {
    *(.bss*)
    *(COMMON)
  }
}
```

---

## Explanation

`ENTRY(_start)`  
Tells the linker to begin execution at the _start symbol (your program’s entry point, typically in assembly or C).

`.text 0x00000000`  
Puts all code (.text*) and read-only data (.rodata*) starting at 0x00000000.

This is typically your flash memory or ROM.

`.data 0x10000000`  
Initialized data (like global variables with initial values) starts at 0x10000000, assumed to be RAM.

`.bss`  
This is for uninitialized global/static variables (they are zero-initialized at runtime).

It follows the .data section and is 4-byte aligned for safe access.

---

## Why FLASH AND SRAM addresses differ?

**Flash vs SRAM:**

| Memory Type | Purpose                        | Key Feature                |
|-------------|-------------------------------|----------------------------|
| Flash       | Store program code (non-volatile) | Retains data on power-off  |
| SRAM        | Store runtime data (RAM)          | Fast and volatile          |

RISC-V / Microcontroller Memory Map

| Region | Typical Address Range        | Purpose                           |
|--------|-----------------------------|------------------------------------|
| Flash  | 0x00000000 to 0x0FFFFFFF    | Code & constants (read-only)       |
| SRAM   | 0x10000000 to 0x1FFFFFFF    | Variables, stack, heap (read/write)|