
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
