---
layout: post
title: Bare-Metal ARM Cortex-M Firmware Development with GCC and Makefiles
categories: [Embedded Systems,]
tags : [arm cortex-m, gcc, make, tm4c, microcontrollers, linux]
description: This post is a guide to using the GCC package and the GNU Make utility along with basic code organization, to produce usable bare-metal firmware binaries for ARM Cortex-M Microcontrollers.
excerpt_separator: <!--more-->
image: /public/assets/images/J0dAqCM.png
---

{{page.description}}
This guide is based on the TI TM4C123GXL ARM Cortex-M4 microcontrollers, the compiler flags may vary depending on your cortex-m version and manufacturer
<!--more-->
# Why GCC and Make?
Most Embedded Systems courses world-wide are taught using IDE's like Keil or IAR, but these tools, are propreitary with expensive upfront costs for a license, or restrictions on their usage in their trial edition form, they are also complex to setup, and lead to vendor lock-in, also they are Windows-only, with no versions for other operating systems.Which is why i decided to use GCC and Make for firmware development for ARM MCU's, the Make + GCC combination is effective, free, open source, has decent documentation and is the only competent alternative to propreitary IDEs.
GCC, Makefiles, GDB and OpenOCD or J-Link are packaged into a ready made Eclipse IDE, but that is not the topic of this post.

# What is GCC?
GCC stands for GNU Compiler Collection and as its name states is a compiler package for the C and C++ programming languages, and apart from being a compiler, it also has an Assembler GNU `as` and a Linker called GNU `ld`, GCC is the standard compiler package for Linux and BSD variants on x86 PC's , but we will be using the ARM microcontroller specific version in this guide.

# What is Make/makefile ?
GNU Make is a build automation program that is pre-installed on most Linux variants.
We are using Make because it can build an executable binary using GCC and various source and header files in different folder automatically, using the commands specified in a
`makefile`, We can then build our executable simply by calling `make` in the directory of our `makefile`

# Guide

First we install the GCC Package for ARM microcontrollers
```
sudo apt install arm-none-eabi-gcc
```

Next, we create a sane directory structure to organize our C source, C libraries, Header files, Linker Script and Assembly code files( if any ), to make development easier.
```
mkdir libs ld src inc
```
Here ,
- `libs` should have the `*.c` library files for peripheral initialization and utilization by other programs
- `inc` has the `*.h` Header files, containing Register definitions and startup code
- `src` has the main program logic
- `ld` contains the `.ld` linker script specific to this TM4C chip

I already have a github repo containing a ready make directory setup like this with a basic RGB Blinky C Program and the necessary startup code and linker script files, you can get it from github like so.
```
git clone https://github.com/shawn-dsilva/tm4c-linux-template.git
```
Since the focus of this guide is writing a Makefile, delete the makefile from this cloned repo.

# Writing the Makefile

This makefile will be primarily three parts, the variables and macros needed for this makefile, the compiler and linker flags needed for compilation, and the rules needed to build the final binary using these variables.
<br>
# Basic Variables and Macros
First off, we start with basic variables
```
PROJECT = main
MCU = TM4C123GH6PM
```
`PROJECT` is just what you want your final binary to be named, in my case it is just `main`
`MCU` here specifies the part number of your MCU, this is fed to the GCC compiler later on

Next, we move on to setting up the macros pointing to  the directories and files which are used to build the executable.
```
SRCS = $(wildcard src/*.c) \
	  $(wildcard libs/*.c)
OBJ = obj/

OBJS = $(addprefix $(OBJ),$(notdir $(SRCS:.c=.o)))

LD_SCRIPT = ld/$(MCU).ld
```
- `SRCS` here points to a wildcard function, which selects every `.c` file in the `src` and `libs` directories,
- `OBJ` here points to the `obj` directory where our `.o` object files and `.d` dependency files will go
- `OBJS` Is a list of object files, but this leads to a complex function which is divided into two parts, the `$(SRCS:.c=.o)` marco  says that `OBJS` means all `.o` files in `OBJS` have the same name as the `.c` files in the `SRCS` macro,except with the `.o` suffix.
Next, the `addprefix` function here is used to put the new `.o` files into the `obj` folder instead of leaving them in the `src` and `libs` directories
- `INC` is a compiler flag `-I` which points to the `inc` folder containing our `.h` header files.
- `LD_SCRIPT`  points to the linker script for this MCU

The following are just some variables for the compiler and related utilities we will be using in the build-rules later on, these variables reduce unnecessary repetition.

```
CC = arm-none-eabi-gcc # C Compiler
LD = arm-none-eabi-ld #  Linker
OBJCOPY = arm-none-eabi-objcopy # Final Binary Builder
FLASHER = lm4flash # Flashing utility
RM      = rm -rf # Remove recursively command
MKDIR   = @mkdir -p $(@D) # Creates folders if not present
```
Next we move on to our compiler flags.

# Variables of Compiler and Linker flags

Since there are various ARM Cortex-M MCU models,and even more manufacturer variants, there will contain some specific GCC flags related to the TM4C123G this makefile is written for, if you use a different microcontroller, it may be different for you
```
CFLAGS = -ggdb -mthumb -mcpu=cortex-m4 -mfpu=fpv4-sp-d16
```
The flags here tell the compiler to
- add GDB debug symbols( `-ggdb` ),
- compile using the ARM Thumb instruction set( `-mthumb`),
- using the Cortex-M4 microcontroller( `-mcpu=cortex-m4`), and
- specify the floating point unit used in this M4 microcontroller( `-mfpu=fpv4-sp-d16` )

```
CFLAGS += -mfloat-abi=softfp -Os -MD -std=c99 -c
```
We use the `+=` operator here to concatenate these additional commands to the CFLAGS variable, not overwrite them with an `=` sign.
- The first flag `Os` tells the compiler to enable all optimizations that do not increase code size.
- `-MD` created `.d` text files in the `.obj` directory, these are simply text files about the dependencies of each file.
- `-std=c99` tells the compiler to use the C99 standard, and finally,
- `-c` tells it to compile without linking the files, leading to object files instead of an executable.

Now we move on to using `ld` to link all our object files into an excutable

```
LDFLAGS = -T $(LD_SCRIPT) -e Reset_Handler
```
- `-T ` tells the compiler to use the `.ld` linker script specified after it, in this case it is the variable $(LD_SCRIPT),
- ` -e Reset_Handler` stands for program entry point, which is pointed to the Reset_Handler function in the interrupt vector table, this means that the program runs upon reseting of the microcontroller.


# Build Rules

Now we are on the final stage, where we use our defined macros and variables to build our executable
The rules work in a simple fashion, a `target` on the left side of the colon `:` is built using the `dependencies` on the right side of the colon

```
all: bin/$(PROJECT).bin
```
`all` is the default target, which runs when you type `make` in your shell.
to complete `all`, it needs the `bin/$(PROJECT).bin` file, which will be made using the below
rules.


```
$(OBJ)%.o: src/%.c
	$(MKDIR)
	$(CC) -o $@ $^ $(INC) $(CFLAGS)

$(OBJ)%.o: libs/%.c
	$(MKDIR)
	$(CC) -o $@ $^ $(INC) $(CFLAGS)
```

The `%.c` here  means that for every `.c` source file in the `src` and `libs` directories, an object file is being created in the `obj` directory with the same name,
`$@` refers to the left side of the colon, that is the target name, and `$^` refers to the right side of the colon that is the dependencies
for example this `$(CC) -o $@ $^ $(INC) $(CFLAGS)` line expands to
` arm-none-eabi-gcc -o main.o main.c -Iinc -ggdb -mthumb -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -Os -MD -std=c99 -c  `
in the shell, assuming `main.c` is the file being compiled here
the `$(MKDIR)`  here creates an `obj` directory if it isn't already present


```
bin/$(PROJECT).elf: $(OBJS)
	$(MKDIR)
	$(LD) -o $@ $^ $(LDFLAGS)
```
This is the stage where we build the executable with GDB debug symbols attached( `*.elf`) by Linking our Object files.
The `$(OBJS)` variable as desribed earlier is a list of objects in the `obj` folder, which will all be linked to make our `$(PROJECT.elf)` binary in the `bin` folder.
the `$(MKDIR)`  here creates a `bin` directory if it isn't already present

```
bin/$(PROJECT).bin: bin/$(PROJECT).elf
	$(OBJCOPY) -O binary $@ $<
```
This is the last stage, where another executable is made, stripped of all the GDB debug symbols, this is the binary that will be flashed to our ARM microcontroller
The `$<` means to select the first element of the dependencies on the right side of the colon, and since we have only one dependency, this is the expression we use here.

```
clean:
	-$(RM) obj
	-$(RM) bin
```
This command removes the `obj` and `bin` folders, leaving only our source code folders and header files intact, for fresh compilation

```
.PHONY: all clean
```
The `.PHONY` macro here specifies that the elements to the right of the colon are not actual targets to be built, but pseudo targets, this enables to use `all` and `clean` as commands with `make` ,
rather than having any executable build for `all` and `clean`


```
flash:
	$(FLASHER) -S $(DEV) bin/$(PROJECT).bin
```

This is an optional `make flash` command that uses the unofficial `lm4tools` flashing utility for the TM4C123G microcontrollers, other brands like STM have the `st-link` utility, altough i recommend OpenOCD for flashing.You can read my guide to flashing using OpenOCD <a href="https://www.shawndsilva.com/2019/02/14/Flashing-Firmware-to-ARM-microcontrollers-and-Debugging-using-OpenOCD/">here</a>.

The complete `Makefile` should look like this

```
PROJECT = main
# SRCS: all source files from src directory
SRCS = $(wildcard src/*.c) \
	  $(wildcard libs/*.c)
OBJ = obj/
# OBJS: list of object files
OBJS = $(addprefix $(OBJ),$(notdir $(SRCS:.c=.o)))

#Flag points to the INC folder containing header files
INC = -Iinc

# LD_SCRIPT: linker script
LD_SCRIPT = ld/$(MCU).ld


#UTILITY VARIABLES
CC = arm-none-eabi-gcc #compiler
LD = arm-none-eabi-ld #linker
OBJCOPY = arm-none-eabi-objcopy #final executable builder
FLASHER = lm4flash #flashing utility
RM      = rm -rf
MKDIR   = @mkdir -p $(@D) #creates folders if not present

#GCC FLAGS
CFLAGS = -ggdb -mthumb -mcpu=cortex-m4 -mfpu=fpv4-sp-d16
CFLAGS += -mfloat-abi=softfp -Os -MD -std=c99 -c

#LINKER FLAGS
LDFLAGS = -T $(LD_SCRIPT) -e Reset_Handler

# Rules to build bin
all: bin/$(PROJECT).bin

$(OBJ)%.o: src/%.c
	$(MKDIR)
	$(CC) -o $@ $^ $(INC) $(CFLAGS)

$(OBJ)%.o: libs/%.c
	$(MKDIR)
	$(CC) -o $@ $^ $(INC) $(CFLAGS)

bin/$(PROJECT).elf: $(OBJS)
	$(MKDIR)
	$(LD) -o $@ $^ $(LDFLAGS)

bin/$(PROJECT).bin: bin/$(PROJECT).elf
	$(OBJCOPY) -O binary $< $@

#Flashes bin to TM4C
flash:
	$(FLASHER) -S $(DEV) bin/$(PROJECT).bin

#remove object and bin files
clean:
	-$(RM) obj
	-$(RM) bin

.PHONY: all clean
```