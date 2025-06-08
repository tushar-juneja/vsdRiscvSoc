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


