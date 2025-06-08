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
