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
