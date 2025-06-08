
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