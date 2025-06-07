# Task-3: From C to Assembly

In this task, we will generate assembly file for our simple C program and also explain the meaning of **prologue** and **epilogue**.

## Step - 1
Generate assembly file using the following command:
```bash
riscv32-unknown-elf-gcc -S -O0 hello.c
```

![Assembly file command](./assets/Task-3/assembly_command.png)

Flags used:
```bash
    -S: This flag is used to tell the compiler to generate assembly instead of object code
    -O0: disables optimizations so you can see the raw function structure.
```

---

## Understanding **Prologue** and **Epilogue**


![Complete assembly code](./assets/Task-3/assembly_code.png)


### Prologue
It is the code at the start of a function. It:

Allocates stack space

Saves callee-saved registers (like s0, ra)

Sets up the frame pointer (s0)

In our simple c program, this is the proglogue:
```bash
addi	sp,sp,-16       # Allocate 16 bytes on the stack
sw	    ra,12(sp)        # Save return address
sw	    s0,8(sp)         # Save old frame pointer
addi	s0,sp,16         # Set new frame pointer (s0 = old sp)
```

### Epilogue
The epilogue is the code at the end of the function. It:

Restores saved registers

Deallocates stack

Returns to the caller

In our program, this is the epilogue generated in assembly file:
```bash
lw	    ra,12(sp)        # Restore return address
lw	    s0,8(sp)         # Restore old frame pointer
addi	sp,sp,16         # Deallocate stack frame
jr	    ra               # Jump to return address
```

