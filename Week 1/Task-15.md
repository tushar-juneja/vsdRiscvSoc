
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