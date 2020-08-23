---
layout: post
title: Writing the Startup Code and Linker Script for the TM4C ARM Microcontroller from scratch
categories: [Embedded Systems,]
tags : [arm cortex-m, C, tm4c, microcontrollers, linux]
description: Nearly every ARM Cortex-M needs needs a **startup code** file to define it's  Main Stack Pointer, Reset Handler and Vector Table and a linker script telling it to place which sections into which parts of memory,
excerpt_separator: <!--more-->

---

{{page.description}} these two files are crucial,without which even a simple blinky program cannot be run. Usually,the vendor provided versions of these files are sufficient,but the TI provided ones require a ~500MB download,and registration on the TI website,labyrnthine folder structure with very little documentation of what goes where or how is the project structured<br>
<!--more-->
To top it all off,nearly every file in the TI package has this license in it :

> Texas Instruments (TI) is supplying this software for use solely and
> exclusively on TI's microcontroller products. The software is owned by
> TI and/or its suppliers, and is protected under applicable copyright
> laws. You may not combine this software with "viral" open-source
> software in order to form a larger program.

Which is why i decided to write my own **Open Source** Startup code and Linker Script,and document how both of them work on this blog.


<br>


Startup Code
==============

First we start off with the Startup code,which has two main functions
1. Initializing the Vector Table with the `Main Stack Pointer`
2. Implementing the `Reset_Handler` function,which consists of,
- Copying `.data` sections of the memory from Internal Flash to Internal SRAM
- Setting `.bss` values to 0
- And finally pointing to the `main()` function of your program,after these initialization tasks are done
<br>

## Writing  Startup.h
The Vector Table is an array of `void` functions which is placed into a section in the memory,namely
`.vector_table` in this case,this name has to also be reflected in the linker script.
<br>
The functions each map to an Interrupt index-wise,which is hardcoded into the microcontroller itself,
the interrupt vector table is defined in the TM4C123GH6PM data sheet, pages 147-149, and we will be using it to write our own vector table.
<br>
We will be having around ~120 or so function prototypes in our vector table, so we need to aliase undefined function prototypes to a default handler function, we do this by defining a macro in our
`startup.h` file like so
<br>
```c
#define DEFAULT __attribute__((weak, alias("Default_Handler")))
```
This macro, `DEFAULT` will expand to `__attribute__((weak, alias("Default_Handler")))` which is a command to the GNU GCC compiler to aliase a given function to the `Default_Handler` if it is not defined
<br>
For example,we are going to explicitly define the `Reset_Handler` function prototype in the `startup.c` file, but not the `NMI_Handler` or other functions for now, so we mark them as `DEFAULT`

```c
void Reset_Handler(void);
DEFAULT void NMI_Handler(void);
DEFAULT void SVC_Handler(void);
DEFAULT void DebugMonitor_Handler(void);
DEFAULT void PendSV_Handler(void);
DEFAULT void SysTick_Handler(void);
```
We then start writing the ISR function prototypes
```c
DEFAULT void GPIOPortA_ISR(void);
DEFAULT void GPIOPortB_ISR(void);
DEFAULT void GPIOPortC_ISR(void);
DEFAULT void GPIOPortD_ISR(void);
DEFAULT void GPIOPortE_ISR(void);
DEFAULT void UART0_ISR(void);
DEFAULT void UART1_ISR(void);
DEFAULT void SPI0_ISR(void);
DEFAULT void I2C0_ISR(void);
DEFAULT void PWM0Fault_ISR(void);
DEFAULT void PWM0Generator0_ISR(void);
.........
```
The rest of the ISR prototypes can be viewed on my [Github Repo(tm4c-linux-template)](https://github.com/shawn-dsilva/tm4c-linux-template.git), these prototypes conform to the **Interrupt
Vector Table** interrupts from the datasheet

<br>
These function prototypes are of return type `void`, and standard arrays cannot be declared as void, so we need to define new types for these
```c
typedef void (*element_t)(void);
```
Here, `*element_t` is a pointer passed to void function and cast as void

<br>

next we define a `union` for our main stack pointer and our ISRs
```c
typedef union {
    element_t isr;
    void *stack_top;
} vector_table_t;
```
`void *stack_top` is a pointer to the top of the stack,and the 0th element of the vector table.
<br>
`element_t isr` stands for the void functions that will be added to the vector table

<br>
Lastly,we have to declare external variables,mainly the sections,and the `main()` program entry point
```c
extern int main(void);

extern uint32_t _stack_ptr;
extern uint32_t _etext;
extern uint32_t _data;
extern uint32_t _edata;
extern uint32_t _bss;
extern uint32_t _ebss;
```
Here the `extern` keyword simply tells to compiler to look for these keywords in another file external to this,the `uint32_t` means an unsigned,32 bit integer,to dispel ambiquity of int sizes on different architectures.<br>
`int main(void)` is the entry point to your `main()` program.<br>
`_stack_ptr` is the pointer to the top of the stack,i.e the last address of RAM,this is defined in the linker script.<br>
`_data` is the start of the `.data` section,and `_edata` is the end of the `.data` section,same convention applies to the other section variables too.


## Writing Startup.c

We start by including our `startup.h` header file with out definitions and the `<stdint.h>`
```c
#include <stdint.h>
#include "startup.h"
```
Next we direct the compiler to place the following vector table into the section `.vector_table`
in the `.data` segment
```c
__attribute__((section(".vector_table")))
```
<br>

Now we define our vector table like so
```c
const vector_table_t vectors[] = {
{.stack_top = &_stack_ptr},
Reset_Handler,
NMI_Handler,
HardFault_Handler,
MemManageFault_Handler,
BusFault_Handler,
UsageFault_Handler,
0,
0,
0,
0,
SVC_Handler,
DebugMonitor_Handler,
0,
PendSV_Handler,
SysTick_Handler,
GPIOPortA_ISR,
GPIOPortB_ISR,
GPIOPortC_ISR,
GPIOPortD_ISR,
GPIOPortE_ISR,
UART0_ISR,
UART1_ISR,
SPI0_ISR,
    /*MORE ISRS FOLLOW FROM HERE */
};
```
Here,
- The 0th element,`{.stack_top = &_stack_ptr}` assigns the  Main Stack Pointer defined in the Linker Script, `_stack_ptr`
to the union element `.stack_top` defined in `vector_table_t`
- The 1st element is the `Reset_Handler`, that is called when the <RESET> Button on the microcontroller is pressed,or the reset flag is set
<br>

Finally we define the `Reset_Handler` and `Default_Hanlder`
```c
void Reset_Handler(void)
{

  uint32_t *src, *dest;


  src = &_etext;
  for (dest = &_data; dest < &_edata;)
  {
    *dest++ = *src++;
  }


  for (dest = &_bss; dest < &_ebss;)
  {
    *dest++ = 0;
  }

  main();
}
```
In this function,
- Two pointers are declared, `*src` and `*dest`
- `*src` is set to the address of `_etext`,and in the first loop `*dest`
is set to the address of `_data`
- Till `dest` reaches the end of `edata` it will loop and copy the contents of `*src` into it
- This is copying the data from `.data` residing on the Flash,to the RAM
- `dest` is now set to the address of `_bss` and every element of `dest`,i.e `_bss` is now being set to `0`
- Lastly,your `main()` is called,and control handed over to it
<br>

`Default_Handler` is also defined here,and it just infinitely loops when called
```c
void Default_Handler(void)
{
  while (1)
  {}
}
```

**With this,we are finally done writing the startup code**

The rest of the code can be viewed on my [Github Repo(tm4c-linux-template)](https://github.com/shawn-dsilva/tm4c-linux-template.git)