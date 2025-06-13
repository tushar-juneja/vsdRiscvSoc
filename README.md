# Complete Weekly Summary

# Week 1 Summary

# Task-1: Install & Sanity-Check the RISC-V Toolchain

The goal is to download, install and verify the risc-v toolchain on pc.

## Step 1: Download the Toolchain

Download the RISC-V toolchain from the following link:  
[riscv-toolchain-rv32imac-x86_64-ubuntu.tar.gz](https://vsd-labs.sgp1.cdn.digitaloceanspaces.com/vsd-labs/riscv-toolchain-rv32imac-x86_64-ubuntu.tar.gz)

---

## Step 2: Extract the Toolchain

Open a terminal and run:
```bash
cd ~/Downloads
tar -xzf riscv-toolchain-rv32imac-x86_64-ubuntu.tar.gz
```

---

## Step 3: Add Toolchain to PATH

Edit your `~/.bashrc` file and add the toolchain to your PATH:
```bash
vim ~/.bashrc
# Add the following line at the end of the file:
export PATH=$PATH:~/Downloads/riscv-toolchain-rv32imac-x86_64-ubuntu/bin
```
After editing, reload your `.bashrc`:
```bash
source ~/.bashrc
```

---

## Step 4: Verify the Installation

Check if the toolchain is installed correctly:

```bash
riscv32-unknown-elf-gcc --version
```
**Expected Output:**  
![GCC](/Week%201/assets/Task-1/gcc.png)

```bash
riscv32-unknown-elf-objdump --version
```
**Expected Output:**  
![ObjDump](/Week%201/assets/Task-1/objdump.png)

```bash
riscv32-unknown-elf-gdb --version
```
**Expected Output:**  
![GDB](/Week%201/assets/Task-1/gdb.png)

---

## Problem/Issue Faced

```bash
riscv32-unknown-elf-gdb: error while loading shared libraries: libpython3.10.so.1.0: cannot open shared object file: No such file or directory
```
This means the GDB binary is dynamically linked against Python 3.10, but the required library is missing.

---

## Fix

Install the required Python version and development files:
```bash
sudo apt update
sudo apt install python3.10 python3.10-dev
```

---
<br><br>
# Task-2: Compile "Hello, RISC-V"

We will write a very basic hello world kind of program in c and will cross-compile for rv32imc architecture, and verify the output elf file. 

## Step 1: Create the Source File

Create a file named `hello.c`:
```bash
vim hello.c
```

Paste the following code into `hello.c`:
```c
#include <stdio.h>

int main() {
    printf("Hello, RISC-V!");
    return 0;
}
```

---

## Step 2: Compile for RISC-V

Compile the program for the `rv32imac` target:
```bash
riscv32-unknown-elf-gcc -o hello.elf hello.c
```

![Output of program compilation](/Week%201/assets/Task-2/compilation.png)

---

## Step 3: Verify the Output File

Check that the compiled file is an ELF file:
```bash
file hello.elf
```

![Elf file check](/Week%201/assets/Task-2/verification.png)

---
<br><br>
# Task-3: From C to Assembly

In this task, we will generate the assembly file for our simple C program and explain the meaning of **prologue** and **epilogue**.

---

## Step 1: Generate Assembly File

Use the following command to generate the assembly file:
```bash
riscv32-unknown-elf-gcc -S -O0 hello.c
```

![Assembly file command](/Week%201/assets/Task-3/assembly_command.png)

**Flags used:**
- `-S`: Generate assembly instead of object code.
- `-O0`: Disable optimizations to see the raw function structure.

---

## Understanding **Prologue** and **Epilogue**

![Complete assembly code](/Week%201/assets/Task-3/assembly_code.png)

### Prologue

The **prologue** is the code at the start of a function. It:
- Allocates stack space
- Saves callee-saved registers (like `s0`, `ra`)
- Sets up the frame pointer (`s0`)

In our simple C program, the prologue is:
```assembly
addi	sp,sp,-16       # Allocate 16 bytes on the stack
sw	ra,12(sp)       # Save return address
sw	s0,8(sp)        # Save old frame pointer
addi	s0,sp,16        # Set new frame pointer (s0 = old sp)
```

### Epilogue

The **epilogue** is the code at the end of the function. It:
- Restores saved registers
- Deallocates stack
- Returns to the caller

In our program, the epilogue generated in the assembly file is:
```assembly
lw	    ra,12(sp)        # Restore return address
lw	    s0,8(sp)         # Restore old frame pointer
addi	    sp,sp,16         # Deallocate stack frame
jr	    ra               # Jump to return address
```

---
<br><br>
# Task-4: Hex Dump & Disassembly

In this task, we are expected to convert our ELF file into raw hex format and also disassemble it for analysis.

---

## Step 1: Convert to Hex

Use the following command to get a raw hex file from the ELF file:

```bash
riscv32-unknown-elf-objcopy -O ihex hello.elf hello.hex
```

![Convert to hex command](/Week%201/assets/Task-4/convert_to_hex.png)

Content of generated hex file:  
![Hex file content](/Week%201/assets/Task-4/hex_file_content.png)

---

## Step 2: Disassemble

Use the command below to disassemble the ELF file:

```bash
riscv32-unknown-elf-objdump -d hello.elf
```

![Disassemble command](/Week%201/assets/Task-4/disassemble_output.png)

---

## What is meant by **disassembling**?

Disassembling is the process of converting machine code back to human-readable assembly code.  
It’s a powerful tool that helps developers, reverse engineers, and system programmers understand what a compiled program actually does.

It can be especially useful for debugging low-level issues, such as inspecting:
- Which exact instructions ran
- Whether registers and memory were used correctly
- Whether optimizations or compiler bugs introduced side effects

---

## Step 3: Instruction Walkthrough

| Field     | Value           | Meaning                                                                                       |
|-----------|-----------------|-----------------------------------------------------------------------------------------------|
| Address   | `0:`            | The memory offset or virtual address where this instruction is located                        |
| Opcode    | `1141`          | The actual binary instruction in hex (machine code)                                           |
| Mnemonic  | `addi`          | The name of the instruction, i.e., the assembly operation — in this case, "Add Immediate"     |
| Operands  | `sp, sp, -16`   | Arguments or registers used by the instruction: here, subtract 16 from the stack pointer and store the result back in `sp` |

---
<br><br>
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

---
<br><br>
# Task-6: Stepping with GDB

In this section, we'll explore how we can run our elf file on a simulator (could be built in or external like qemu and spike) and also go through the debugging processing by using breakpoints and stepping.

## Step 1: Run Qemu for ELF
Run qemu for the required elf file using the below command.

```bash
qemu-system-riscv32 -M sifive_e -cpu sifive-e31 -nographic -kernel hello.elf -S -gdb tcp::1234
```

![Command for running qemu](/Week%201/assets/Task-6/qemu_command.png)

## Step 2: Enter into GDB prompt
Open another terminal window for entering into the gdb prompt.

```bash
riscv32-unknown-elf-gdb hello.elf
```

## Step 3: Add breakpoints and step

Connect to qemu running on port 1234
```bash
target remote localhost:1234
```

Add breakpoint for main
```bash
break main
```

Run the script
```bash
continue
```

![GDB Commands](/Week%201/assets/Task-6/gdb_window.png)

## Problem faced
The gdb prompt is getting stuck at continue command. Ideally it should break at the specified breakpoint and then return the prompt.

This is occuring when running it with qemu. I also tried it with the built in simulator using the `target sim` and `run` commands.
Apparently, it seems the in-built simulator only supports `rv32i` base instruction set. I tried compiling my c file into this but it gives `multi-lib` error for which the whole riscv toolchain needs to be built again, tried that, no avail.

With qemu, it didn't work either. It just seems to be stuck at ***continuing***. I tried searching for the entry point of the script in the ELF file for adding at the breakpoint but still it doesn't work
```bash
riscv32-unknown-elf-readelf -h hello.elf | grep 'Entry point'
```

I returned `0x100e2` and I tried putting that in the breakpoint but still the same situation.


## Step 4: Info registers and disassemble
![Info register and disassemble](/Week%201/assets/Task-6/disassemble.jpeg)

---
<br><br>
# Running Under an Emulator

This task demonstrates how to boot a bare-metal ELF and print to the UART console using QEMU.

---

## Minimal `hello.c` for Bare-Metal QEMU Run

```c
int main() {
    puts("Hello, RISCV!");
    return 0;
}
```

**Compile it using:**
```bash
riscv32-unknown-elf-gcc -g -march=rv32imac -mabi=ilp32 -o hello.elf hello.c
```

**Run the ELF using QEMU:**
```bash
qemu-system-riscv32 -M sifive_e -cpu sifive-e31 -nographic -kernel hello.elf
```

![QEMU Output](/Week%201/assets/Task-7/qemu.png)

---

## Ideal Behaviour

Ideally, it should print `"Hello, RISCV!"` in the UART console, but it goes blank after starting QEMU.

---

## Steps Done for Troubleshooting

### Custom UART Print Implementation

Created a minimal UART print routine:

```c
#define UART_ADDR 0x10013000

void putchar(char c) {
    *(volatile char*)UART_ADDR = c;
}

void print(const char* s) {
    while (*s) {
        putchar(*s++);
    }
}

void _start() {
    print("hello riscv\n");
    while (1); // don't exit
}
```

---

### Custom Linker Script (`link.ld`)

```ld
SECTIONS
{
  . = 0x80000000;

  .text : {
    *(.text*)
  }

  .data : {
    *(.data*)
  }

  .bss : {
    *(.bss*)
    *(COMMON)
  }
}
```

---

### Compile with Custom Linker Script

```bash
riscv32-unknown-elf-gcc \
  -nostdlib -nostartfiles \
  -march=rv32ima -mabi=ilp32 \
  -Wl,-T,link.ld \
  -o hello.elf hello.c
```

---

### Run with QEMU

```bash
qemu-system-riscv32 \
  -machine sifive_e -nographic \
  -bios none \
  -kernel hello.elf
```

---
<br><br>
# Task-8: Exploring GCC Optimizations

This section highlights the difference in assembly generated by using different optimization flags during compilation.

---

## Code to Analyze

```c
int main() {
    printf("Hello, RISCV!");
    return 0;
}
```

---

## Compilation Using `-O0` (No Optimization) and `-O2` (High Optimization)

```bash
riscv32-unknown-elf-gcc -O0 -S hello.c -o hello_O0.s
riscv32-unknown-elf-gcc -O2 -S hello.c -o hello_O2.s
```

![O0 and O2 optimization compilation](/Week%201/assets/Task-8/o0_o2_compilation.png)

---

## Assembly Differences

### `-O0`: No Optimization

- Full call to `printf` preserved
- Stack frames and return values handled explicitly
- Intermediate values stored in memory

This version is easier to debug but slower and larger.

![O0 assembly](/Week%201/assets/Task-8/O0.png)

---

### `-O2`: High Optimization

- Function calls may be inlined if small (though `printf()` typically isn’t)
- Stack setup might be eliminated if unnecessary
- Constants embedded directly
- Redundant loads/stores removed

![O2 assembly](/Week%201/assets/Task-8/O2.png)

---

## Conclusion

On bare-metal or constrained systems:

- `-O2` gives much better performance and size
- `-O0` is useful only for debugging

---
<br><br>
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

---
<br><br>
# Task-10: Memory-Mapped I/O Demo

In this we are going to write a bare-metal c snippet to toggle a gpio register located at 0x10012000 and we'll also see how we can prevent the compiler from optimizting the store away.

## What do we mean by store away?

Compilers try to optimize by removing code that seems unnecessary.

```c
int* x = (int*)0x10012000;
*x = 42;
*x = 42;
```

Like in this case, it seems that 42 is begin written to x multiple times, and seems redundant. A compiler would remove the first store to optimize the code.

But in embedded programming, this is dangerous because even if the value is the same, the act of writing can trigger a real-world effect — like turning on an LED, sending data over UART, etc. So we need to make sure that compiler doesn't optimize the stores.

---

## Preventing Optimization with `volatile`

We can prevent this by using the `volatile` keyword.

```c
#define GPIO_ADDR 0x10012000

void toggle_gpio() {
    volatile uint32_t* gpio = (volatile uint32_t*)GPIO_ADDR;

    // Toggle (invert) bit 0 of GPIO register
    *gpio ^= 0x1;
}
```

---

## Explanation

- `#define GPIO_ADDR 0x10012000` defines a macro that holds the gpio register address

- `void toggle_gpio()` - function declaration that returns nothing

- `volatile uint32_t* gpio = (volatile uint32_t*)GPIO_ADDR;`
    - `(volatile uint32_t*)` is typecasting the integer stored in GPIO_ADDR macro into a 32-bit unsigned integer data types whose value is volatile
    - `volatile uint32_t* gpio` declares a pointer to gpio of type unsigned integer of 32 bit whose data value is volatile. **Note: The data that this pointer points to is volatile and not the pointer itself. In that case, the code would've been `unint32_t* volatile gpio`**
    - `*gpio ^= 0x1` toggles/flips the value stored in gpio pointer. The operation being performed here is ***read-modify-write***. Here the value of gpio is first read, then it is toggled by doing XOR with 1 and then written back to it.

---

## ALIGNMENT
Memory alignment means storing data at addresses that are multiples of their size.

So a 4-byte variable (like uint32_t) should start at an address divisible by 4
And a 2-byte variable (like unint16_t) should start at an address divisible by 2

This ensures that the code doesn't fail on strict systems like RISCV etc and also the cpu doesn't have to work extra in reading data from multiple blocks, extract the right bytes and reassemble the value.


| Data Type  | Size (bytes) | Common Alignment      |
|------------|--------------|----------------------|
| uint8_t    | 1            | Any address          |
| uint16_t   | 2            | Multiple of 2        |
| uint32_t   | 4            | Multiple of 4        |
| uint64_t   | 8            | Multiple of 8        |


In our code, we are manually ensuring that the address is word-aligned, if it was let's say **0x10012001** then the program might crash.

---
<br><br>
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

---
<br><br>
# Task-12: Start-up Code & crt0

In this section, we'll see what is crt0 file, what role does it play in bare-metal risc-v programs and how can we get one.

---

## What is crt0 and why do we need it?

`crt0` stands for **C runtime 0**. In a typical bare-metal RISC-V program, there is no operating system to initialize the system before our main code runs.

So, we use a startup assembly file (`crt0.s`) that sets up the basic runtime environment for our code. It is the **first code that runs after reset**.

### What does crt0 do?

| Step | What Happens in crt0.S                | Why It Matters                                 |
|------|---------------------------------------|------------------------------------------------|
| 1    | Define `_start` (the entry point)     | The CPU starts here after reset                |
| 2    | Initialize stack pointer              | So the C code (like `main`) can use the stack  |
| 3    | Zero the `.bss` section               | C standard requires uninitialized globals to be 0 |
| 4    | Copy `.data` from Flash to RAM        | So initialized globals work correctly          |
| 5    | Call `main()`                         | This is your actual application logic          |
| 6    | Optionally call exit or hang          | To handle the end of execution cleanly         |

---

## Where can we get one?

- We can write our own based on the example below
- Or we can use one from:
  - Newlib
  - riscv-pk (proxy kernel)
  - Minimal RISC-V templates by SiFive
  - Embedded frameworks like RIOT OS, Zephyr RTOS, etc.

---

## main C program
```c
    int main() {
        while(1) {

        }
        return 0;
    }
```

## Writing `crt0.s`

```assembly
.section .text
.globl _start

_start:
    # Set up stack pointer (end of SRAM)
    la sp, _stack_top

    # Clear .bss section
    la a0, __bss_start
    la a1, __bss_end
    li a2, 0
bss_clear:
    bge a0, a1, bss_done
    sw a2, 0(a0)
    addi a0, a0, 4
    j bss_clear
bss_done:

    # Copy .data section from Flash to RAM
    la a0, _data_lma      # load memory address (Flash)
    la a1, _data_start    # virtual memory address (RAM)
    la a2, _data_end
copy_data:
    bge a1, a2, data_done
    lw t0, 0(a0)
    sw t0, 0(a1)
    addi a0, a0, 4
    addi a1, a1, 4
    j copy_data
data_done:

    # Call main
    call main

hang:
    j hang  # Loop forever
```

---

## Example Linker Script

```ld
ENTRY(_start)

MEMORY
{
    FLASH (rx)  : ORIGIN = 0x00000000, LENGTH = 512K
    SRAM  (rwx) : ORIGIN = 0x10000000, LENGTH = 64K
}

SECTIONS
{
    .text : {
        *(.text*)
        *(.rodata*)
    } > FLASH

    .data : AT (ADDR(.text) + SIZEOF(.text)) {
        _data_lma = LOADADDR(.data);
        _data_start = .;
        *(.data*)
        _data_end = .;
    } > SRAM

    .bss : {
        __bss_start = .;
        *(.bss*)
        *(COMMON)
        __bss_end = .;
    } > SRAM

    .stack (NOLOAD) : {
        . = ALIGN(4);
        _stack_top = . + 0x1000;  /* 4KB stack */
    } > SRAM
}
```

---

- `_start` is the entry point (not `main`). That’s why `ENTRY(_start)` is in the linker script.
- `la sp, _stack_top` sets up the stack manually (no OS to do this).

- `.data` copy and `.bss` zeroing are essential for C runtime correctness.

## Compilation
```bash
riscv32-unknown-elf-gcc -march=rv32imac -mabi=ilp32 -nostartfiles -T link.ld -o program.elf crt0.s main.c
```

## Verifying the ELF
![Reading ELF](/Week%201/assets/Task-12/reading_elf.png)

## Checking the entry point
![Checking Entry point](/Week%201/assets/Task-12/entry_point.png)

## Conclusion
This task simulates a real embedded boot process — where no OS is present, and the CPU starts executing from a fixed address (like Flash). crt0.S prepares the system so main() can safely execute.

---
<br><br>
# Task-13: Interrupt Primer

## Objective
To enable the machine-timer interrupt (MTIP) and write a simple handler in C.


## What is the Machine Timer Interrupt (MTIP)?

The **Machine Timer Interrupt (MTIP)** is a fundamental interrupt in the RISC-V privileged architecture. It is triggered by the machine timer, which uses two special memory-mapped registers:

- **mtime**: A continuously incrementing 64-bit timer register representing the current time.
- **mtimecmp**: A 64-bit comparator register. When `mtime` equals or exceeds `mtimecmp`, the machine timer interrupt is triggered.

These registers are usually implemented in the **CLINT** (Core Local Interruptor) hardware block of the RISC-V system.


## How MTIP Works in this Example

- **Setting up MTIP**:  
  We program `mtimecmp` to `mtime + MTIMECMP_DELAY`. The timer interrupt fires when the current time reaches this threshold.

- **Interrupt generation**:  
  When `mtime` reaches `mtimecmp`, the hardware sets the MTIP bit in the `mip` register, causing the machine-level timer interrupt.

- **Interrupt handler**:  
  Control transfers to the `trap_handler`, which saves registers, calls the C-level `timer_isr()` function, then restores registers and returns using `mret`.

- **Reprogramming the timer**:  
  Inside `timer_isr()`, we print a message and update `mtimecmp` to trigger the next interrupt.

- **Interrupt count limit**:  
  The example limits the number of handled interrupts to 5, using a `count` variable.

---

## MTIP Handler in C

```c
#include <stdint.h>
#include <stddef.h>

#define UART_BASE        0x10000000
#define MSTATUS_MIE      (1 << 3)
#define MIE_MTIE         (1 << 7)
#define MTIMECMP_DELAY   500000

#define CLINT_MTIME      (*(volatile uint64_t *)(0x200bff8))
#define CLINT_MTIMECMP   (*(volatile uint64_t *)(0x2004000))

// UART output helper
void uart_puts(const char *s) {
    volatile char *uart = (volatile char *)UART_BASE;
    while (*s) {
        *uart = *s++;
    }
}

// Timer interrupt handler
volatile int count = 0;

void timer_isr(void) {
    if (count < 5) {
        uart_puts(">> Timer Interrupt Triggered\n");
        count++;
        CLINT_MTIMECMP = CLINT_MTIME + MTIMECMP_DELAY;
    }
}

void main(void) {
    uart_puts("== Timer Interrupt Example ==\n");

    timer_isr();  // Initial test call

    // Set mtvec to point to trap handler
    extern void trap_handler(void);
    uintptr_t trap_addr = (uintptr_t)&trap_handler;
    asm volatile("csrw mtvec, %0" :: "r"(trap_addr));

    // Set first timer interrupt
    CLINT_MTIMECMP = CLINT_MTIME + MTIMECMP_DELAY;

    // Enable machine timer interrupt and global interrupt
    asm volatile("csrs mie, %0" :: "r"(MIE_MTIE));
    asm volatile("csrs mstatus, %0" :: "r"(MSTATUS_MIE));

    while (1) {
        asm volatile("wfi");
    }
}
```
### Linker Script (intr_link.ld)
```ld
OUTPUT_ARCH(riscv)
ENTRY(_start)

MEMORY {
  RAM (rwx) : ORIGIN = 0x80000000, LENGTH = 16M
}

SECTIONS {
  . = 0x80000000;

  .text : {
    *(.text*)
  }

  .rodata : {
    *(.rodata*)
  }

  .data : {
    *(.data*)
  }

  .bss : {
    *(.bss*)
    *(COMMON)
  }

  .trap : {
    *(.trap)
  }

  . = ALIGN(4);
  PROVIDE(_stack_top = ORIGIN(RAM) + LENGTH(RAM));
}
```
### Startup Code (startup_intr.S)
```
.section .text
.globl _start
_start:
    la sp, _stack_top         // Initialize stack pointer
    call main                 // Call main()
1:  wfi                       // Halt if main returns
    j 1b

.section .trap, "ax"
.globl trap_handler
trap_handler:
    addi sp, sp, -16
    sw ra, 12(sp)
    sw t0, 8(sp)
    sw t1, 4(sp)
    sw t2, 0(sp)

    call timer_isr            // Call C handler

    lw ra, 12(sp)
    lw t0, 8(sp)
    lw t1, 4(sp)
    lw t2, 0(sp)
    addi sp, sp, 16
    mret
```

## OUTPUT
![interrupt_primer](/Week%201/assets/Task-13/interrupt_primer.png)

---
<br><br>
# Task 14:  rv32imac vs rv32imc – What’s the “A”? 
## Objective
**To explain the ‘A’ (atomic) extension in rv32imac. What instructions are added and why are they useful?**

## Concept  
- The **‘A’ extension** stands for **Atomic instructions** in the RISC-V ISA, making the difference between `rv32imc` (integer, multiply, compressed) and `rv32imac` (integer, multiply, atomic, compressed).  
- It adds **atomic memory operations** such as:  
  - **`lr.w`** (Load-Reserved Word)  
  - **`sc.w`** (Store-Conditional Word)  
  - **`amoadd.w`** (Atomic Memory Operation: Add Word)  
  - And other atomic operations like `amoswap.w`, `amoxor.w`, `amoand.w`, `amoor.w`, `amomin.w`, `amomax.w`, etc.  
- These instructions allow **atomic read-modify-write sequences** on memory locations without interruption, which is crucial for:  
  - Implementing **lock-free data structures** (queues, stacks)  
  - Writing **OS kernels and synchronization primitives** (mutexes, spinlocks, semaphores)  
  - Ensuring **safe concurrency** on multi-core or multi-threaded processors  
- Without these atomic instructions, software would need to disable interrupts or use heavier synchronization methods, which impact performance and scalability.

---
<br><br>
# Task 15: Atomic Test Program 
## Objective
Demonstrate the use of the RISC-V atomic extension (`A`) to implement a simple spinlock using the Load-Reserved (LR) and Store-Conditional (SC) instructions in a two-thread pseudo-concurrent environment.

## Spinlock Implementation Using LR/SC
The spinlock works by repeatedly attempting to set a lock variable from 0 (unlocked) to 1 (locked). If the lock is already held (value 1), the thread spins until it becomes free.

## Pseudo-threaded C Implementation with Inline Assembly

```c
#include <stdint.h>

#define UART_BASE 0x10000000
volatile char *uart = (volatile char *)UART_BASE;

// UART print helper
void uart_puts(const char *s) {
    while (*s) {
        *uart = *s++;
    }
}

// Simple spinlock using lr/sc
volatile int lock = 0;

void spinlock_acquire(volatile int *lock) {
    int tmp;
    asm volatile(
        "1:\n"
        "lr.w %0, (%1)\n"         // load-reserved from lock
        "bnez %0, 1b\n"           // if lock != 0, spin (busy wait)
        "li %0, 1\n"              // try to set lock = 1
        "sc.w %0, %0, (%1)\n"     // store-conditional to lock
        "bnez %0, 1b\n"           // if store failed, retry
        : "=&r"(tmp)
        : "r"(lock)
        : "memory"
    );
}

void spinlock_release(volatile int *lock) {
    *lock = 0;
}

// Simulate two pseudo-threads trying to acquire lock alternately
void main(void) {
    uart_puts("Starting atomic spinlock test\n");

    for (int i = 0; i < 2; i++) {
        // Pseudo-thread 1
        uart_puts("Thread 1: Waiting for lock...\n");
        spinlock_acquire(&lock);
        uart_puts("Thread 1: Lock acquired!\n");

        // Critical section
        uart_puts("Thread 1: Working...\n");

        spinlock_release(&lock);
        uart_puts("Thread 1: Lock released\n\n");

        // Pseudo-thread 2
        uart_puts("Thread 2: Waiting for lock...\n");
        spinlock_acquire(&lock);
        uart_puts("Thread 2: Lock acquired!\n");

        // Critical section
        uart_puts("Thread 2: Working...\n");

        spinlock_release(&lock);
        uart_puts("Thread 2: Lock released\n\n");
    }

    uart_puts("Test completed.\n");

    while (1) {
        asm volatile("wfi");
    }
}
```

## Commands used for compilation and running qemu
```bash
riscv32-unknown-elf-gcc -march=rv32imac_zicsr -mabi=ilp32 -nostdlib -nostartfiles   -T intr_link.ld -o atomic_test.elf start.S atomic_test.c
qemu-system-riscv32 -machine virt -nographic -bios none -kernel atomic_test.elf
```

---
![Atomic test](/Week%201/assets/Task-15/atomic_test.png)

---

---
<br><br>
# Task 16: Using Newlib printf Without an OS

## Objective
Demonstrate how to use Newlib's printf functionality in a bare-metal RISC-V environment by implementing custom system call stubs and retargeting the `_write` function to output via UART.

## Solution Overview
- Implement `_write(int fd, char* buf, int len)` that loops over bytes to UART_TX
- Provide required syscall stubs for Newlib compatibility
- Link with Newlib while using custom startup code

## Implementation

### Write system call function
```c
// Write system call - this is what printf uses
int _write(int fd, char *buf, int len) {
    // Only handle stdout/stderr
    if (fd == 1 || fd == 2) {
        for (int i = 0; i < len; i++) {
            uart_putc(buf[i]);
        }
        return len;
    }
    return -1;
}
```

### syscalls.c - System Call Implementations
```c
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/fcntl.h>
#include <sys/times.h>
#include <sys/errno.h>
#include <sys/time.h>
#include <stdio.h>

// QEMU virt machine UART base address
#define UART_BASE 0x10000000
#define UART_TX   (*(volatile char*)(UART_BASE + 0))
#define UART_LSR  (*(volatile char*)(UART_BASE + 5))
#define UART_LSR_THRE 0x20  // Transmitter holding register empty

// Simple UART output function
static void uart_putc(char c) {
    // Wait for transmitter to be ready
    while (!(UART_LSR & UART_LSR_THRE));
    UART_TX = c;
}

// Write system call - this is what printf uses
int _write(int fd, char *buf, int len) {
    // Only handle stdout/stderr
    if (fd == 1 || fd == 2) {
        for (int i = 0; i < len; i++) {
            uart_putc(buf[i]);
        }
        return len;
    }
    return -1;
}

// Required syscall stubs for Newlib
int _read(int fd, char *buf, int len) {
    return -1;  // Not implemented
}

int _close(int fd) {
    return -1;  // Not implemented
}

int _lseek(int fd, int offset, int whence) {
    return -1;  // Not implemented
}

int _fstat(int fd, struct stat *st) {
    st->st_mode = S_IFCHR;
    return 0;
}

int _isatty(int fd) {
    return 1;  // Assume all file descriptors are TTY
}

void *_sbrk(int incr) {
    extern char _end;
    static char *heap_end = 0;
    char *prev_heap_end;

    if (heap_end == 0) {
        heap_end = &_end;
    }
    
    prev_heap_end = heap_end;
    heap_end += incr;
    
    return (void *)prev_heap_end;
}

void _exit(int status) {
    while (1) {
        asm volatile("wfi");
    }
}

int _kill(int pid, int sig) {
    return -1;  // Not implemented
}

int _getpid(void) {
    return 1;
}
```

### main.c - Main Program with Printf
```c
#include <stdio.h>
#include <stdint.h>


int main(void) {
    printf("Testing printf with numbers: %d \n", 93);
    printf("Float test: %.2f\n", 69.4931);
    printf("RISC-V bare metal this side!\n");
    

    
    while (1) {
        // Main loop - let interrupts handle the rest
        asm volatile("wfi");
    }
    
    return 0;
}
```

### Updated Linker Script (intr_link.ld)
```ld
OUTPUT_ARCH(riscv)
ENTRY(_start)

MEMORY {
  RAM (rwx) : ORIGIN = 0x80000000, LENGTH = 16M
}

SECTIONS {
  . = 0x80000000;
  
  .text : {
    *(.text.startup)
    *(.text*)
  } > RAM
  
  .rodata : {
    *(.rodata*)
  } > RAM
  
  .data : {
    *(.data*)
  } > RAM
  
  .bss : {
    *(.bss*)
    *(COMMON)
    . = ALIGN(4);
    _end = .;  /* End of BSS for heap */
  } > RAM
  
  .trap : {
    *(.trap)
  } > RAM
  
  . = ALIGN(4);
  PROVIDE(_stack_top = ORIGIN(RAM) + LENGTH(RAM));
}
```

## Commands Used
```bash
# Compile command - Key changes from original:
# Kept -nostartfiles since we provide our own _start

riscv32-unknown-elf-gcc -march=rv32imac_zicsr -mabi=ilp32 \
    -nostartfiles -T intr_link.ld \
    -o main.elf start.S main.c syscalls.c

# Run with QEMU
qemu-system-riscv32 -machine virt -nographic -bios none -kernel main.elf
```
### Note: Uses the same startup assembly (start.S) as the previous tasks

---

## Key Technical Details

### UART Retargeting
- The `_write()` function intercepts all printf output calls
- Uses QEMU virt machine's UART at memory address `0x10000000`
- Implements proper UART status checking before transmitting bytes
- Only handles stdout (fd=1) and stderr (fd=2) file descriptors

### System Call Stubs
- `_sbrk()` provides heap management for printf's internal memory allocation
- `_fstat()` and `_isatty()` ensure proper file descriptor handling
- Other stubs prevent linking errors while indicating non-implementation

### Compilation Changes
- **Removed `-nostdlib` to allow linking with Newlib (required for printf)
- **Added `syscalls.c` to provide system call implementations
- **Kept `-nostartfiles` since custom startup code is provided

---

### OUTPUT

![newlib printf](/Week%201/assets/Task-16/task-16.png)

---
<br><br>
# Task 17: RISC-V Endianness & Struct Packing Analysis

## Objective
Verify RISC-V byte ordering (endianness) using C union tricks and demonstrate struct packing behavior in bare-metal environments.

## Endianness Verification Method

### Union Trick Implementation
The most reliable way to verify endianness is using a union that overlays a 32-bit integer with a 4-byte array:

```c
typedef union {
    uint32_t word;
    uint8_t bytes[4];
} endian_test_t;

void test_endianness(void) {
    endian_test_t test;
    test.word = 0x01020304;  // Store test pattern
    
    printf("Stored value: 0x%08X\n", test.word);
    printf("bytes[0] = 0x%02X (LSB)\n", test.bytes[0]);
    printf("bytes[1] = 0x%02X\n", test.bytes[1]);
    printf("bytes[2] = 0x%02X\n", test.bytes[2]);
    printf("bytes[3] = 0x%02X (MSB)\n", test.bytes[3]);
    
    if (test.bytes[0] == 0x04) {
        printf("Result: LITTLE ENDIAN\n");
        printf("Memory layout: [04][03][02][01]\n");
    }
}
```

### Expected RISC-V Output
```
Stored value: 0x01020304
bytes[0] = 0x04 (LSB)
bytes[1] = 0x03
bytes[2] = 0x02
bytes[3] = 0x01 (MSB)
Result: LITTLE ENDIAN
Memory layout: [04][03][02][01]
```

### Complete Test Program

```c
#include <stdio.h>
#include <stdint.h>

// Union trick to examine byte ordering
typedef union {
    uint32_t word;
    uint8_t bytes[4];
} endian_test_t;

// Struct packing examples
struct packed_struct {
    uint8_t  byte1;
    uint32_t word1;
    uint16_t half1;
    uint8_t  byte2;
} __attribute__((packed));

struct normal_struct {
    uint8_t  byte1;
    uint32_t word1;
    uint16_t half1;
    uint8_t  byte2;
};

// Function to print binary representation
void print_binary(uint32_t value) {
    printf("Binary: ");
    for (int i = 31; i >= 0; i--) {
        printf("%c", (value & (1U << i)) ? '1' : '0');
        if (i % 8 == 0 && i > 0) printf(" ");
    }
    printf("\n");
}

int main(void) {
    printf("RISC-V Endianness & Struct Packing Analysis\n");
    printf("==========================================\n\n");
    
    // === ENDIANNESS TEST ===
    printf("=== RISC-V Endianness Test ===\n");
    
    endian_test_t test;
    test.word = 0x01020304;
    
    printf("Stored value: 0x%08X\n", test.word);
    print_binary(test.word);
    
    printf("Byte-by-byte examination:\n");
    printf("bytes[0] = 0x%02X (LSB)\n", test.bytes[0]);
    printf("bytes[1] = 0x%02X\n", test.bytes[1]);
    printf("bytes[2] = 0x%02X\n", test.bytes[2]);
    printf("bytes[3] = 0x%02X (MSB)\n", test.bytes[3]);
    
    // Determine endianness
    if (test.bytes[0] == 0x04) {
        printf("Result: LITTLE ENDIAN (LSB first)\n");
        printf("Memory layout: [04][03][02][01]\n");
    } else if (test.bytes[0] == 0x01) {
        printf("Result: BIG ENDIAN (MSB first)\n");
        printf("Memory layout: [01][02][03][04]\n");
    } else {
        printf("Result: UNKNOWN ENDIANNESS\n");
    }
    printf("\n");
    
    // === STRUCT PACKING TEST ===
    printf("=== Struct Packing Test ===\n");
    
    struct normal_struct normal = {0xAA, 0x12345678, 0xBCDE, 0xFF};
    struct packed_struct packed = {0xAA, 0x12345678, 0xBCDE, 0xFF};
    
    printf("Normal struct size: %zu bytes\n", sizeof(struct normal_struct));
    printf("Packed struct size: %zu bytes\n", sizeof(struct packed_struct));
    
    // Print memory layout of normal struct
    printf("\nNormal struct memory layout:\n");
    uint8_t *normal_ptr = (uint8_t*)&normal;
    for (size_t i = 0; i < sizeof(normal); i++) {
        printf("Offset %zu: 0x%02X\n", i, normal_ptr[i]);
    }
    
    // Print memory layout of packed struct
    printf("\nPacked struct memory layout:\n");
    uint8_t *packed_ptr = (uint8_t*)&packed;
    for (size_t i = 0; i < sizeof(packed); i++) {
        printf("Offset %zu: 0x%02X\n", i, packed_ptr[i]);
    }
    printf("\n");
    
    // === BIT FIELD TEST ===
    printf("=== Bit Field Test ===\n");
    
    struct bit_field_test {
        uint32_t field1 : 4;   // 4 bits
        uint32_t field2 : 8;   // 8 bits
        uint32_t field3 : 12;  // 12 bits
        uint32_t field4 : 8;   // 8 bits
    } bf;
    
    bf.field1 = 0xF;      // 1111
    bf.field2 = 0xAB;     // 10101011
    bf.field3 = 0x123;    // 000100100011
    bf.field4 = 0xCD;     // 11001101
    
    printf("Bit field struct size: %zu bytes\n", sizeof(bf));
    printf("field1 (4 bits) = 0x%X\n", bf.field1);
    printf("field2 (8 bits) = 0x%02X\n", bf.field2);
    printf("field3 (12 bits) = 0x%03X\n", bf.field3);
    printf("field4 (8 bits) = 0x%02X\n", bf.field4);
    
    // Print raw memory
    printf("Raw memory content:\n");
    uint8_t *bf_ptr = (uint8_t*)&bf;
    for (size_t i = 0; i < sizeof(bf); i++) {
        printf("Byte %zu: 0x%02X\n", i, bf_ptr[i]);
    }
    printf("\n");
    
    // === ALIGNMENT TEST ===
    printf("=== Memory Alignment Test ===\n");
    
    char buffer[16];
    
    // Test different data type alignments
    uint8_t  *ptr8  = (uint8_t*)(buffer + 1);
    uint16_t *ptr16 = (uint16_t*)(buffer + 2);
    uint32_t *ptr32 = (uint32_t*)(buffer + 4);
    
    printf("Buffer base address: %p\n", (void*)buffer);
    printf("uint8_t  pointer: %p (offset: %ld)\n", (void*)ptr8, (char*)ptr8 - buffer);
    printf("uint16_t pointer: %p (offset: %ld)\n", (void*)ptr16, (char*)ptr16 - buffer);
    printf("uint32_t pointer: %p (offset: %ld)\n", (void*)ptr32, (char*)ptr32 - buffer);
    
    // Check alignment
    printf("uint8_t  alignment: %s\n", ((uintptr_t)ptr8 % 1 == 0) ? "OK" : "BAD");
    printf("uint16_t alignment: %s\n", ((uintptr_t)ptr16 % 2 == 0) ? "OK" : "BAD");
    printf("uint32_t alignment: %s\n", ((uintptr_t)ptr32 % 4 == 0) ? "OK" : "BAD");
    printf("\n");
    
    printf("Analysis complete!\n");
    printf("Program will now halt...\n");
    
    // Give time for all output to flush
    for (volatile int i = 0; i < 1000000; i++) {
        // Small delay to ensure output completes
    }
    
    while (1) {
        asm volatile("wfi");
    }
    
    return 0;
}
```

## Commands Used
```bash
riscv32-unknown-elf-gcc -march=rv32imac_zicsr -mabi=ilp32 \
    -nostartfiles -T linker.ld \
    -o endianness.elf start.s endianness.c syscalls.c

qemu-system-riscv32 -machine virt -nographic -bios none -kernel endianness.elf
```

### Note: Uses the same startup assembly (start.S), linker script (intr_link.ld), and syscalls.c from the previous printf example

---

![Output 1](/Week%201/assets/Task-17/task-17_1_new.png)
![Output 2](/Week%201/assets/Task-17/task-17_2.png)


## Key Technical Points

### RISC-V Endianness
- **Default**: Little-endian (LSB stored at lowest memory address)
- **Bi-endian Support**: RISC-V specification allows big-endian implementations, but little-endian is standard
- **Verification**: Union trick reliably detects byte ordering at runtime

### Structure Alignment Rules
- **Natural Alignment**: Data types align to their size boundaries
  - `uint8_t`: 1-byte alignment
  - `uint16_t`: 2-byte alignment  
  - `uint32_t`: 4-byte alignment
- **Padding**: Compiler inserts padding bytes to maintain alignment
- **Packed Attribute**: `__attribute__((packed))` removes padding

### Bit Field Behavior
- Bit fields are allocated in little-endian order within each storage unit
- First declared field occupies least significant bits
- Endianness affects how bit fields map to memory bytes

---
## Key Observations

- **RISC-V is little-endian by default**: The union trick confirms LSB is stored at the lowest memory address
- **Struct padding affects memory efficiency**: Normal structs use 50% more memory due to alignment requirements
- **Packed structs trade performance for space**: Remove padding but may cause unaligned access penalties
- **Endianness impacts multi-byte data interpretation**: Critical for network protocols, file formats, and cross-platform compatibility
- **Union trick is portable**: Works across different architectures and compilers for endianness detection
- **Memory layout visualization**: Direct byte examination reveals how data is actually stored in memory

---

---
<br><br>

