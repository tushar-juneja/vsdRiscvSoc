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