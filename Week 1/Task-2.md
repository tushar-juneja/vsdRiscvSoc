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
