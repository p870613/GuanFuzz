###### tags: `paper`

# Guan Fuzz

## Environment
- OS
```=shell
➜  ~ lsb_release -r 
Release:	20.04
➜  ~ uname -a
Linux lin-System-Product-Name 5.13.0-40-generic #45~20.04.1-Ubuntu SMP Mon Apr 4 09:38:31 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux
```
- clang & llvm version
```=shell
➜  ~ clang -v
clang version 10.0.0-4ubuntu1 
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /usr/bin
Found candidate GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/8
Found candidate GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/9
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/8
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/9
Selected GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/9
Candidate multilib: .;@m64
Selected multilib: .;@m64
```
```=shell
➜  ~ llvm-config --version
10.0.0
```

## Usage
### xml setting
- element
    - ARGV
        - ELEMENT
            - origin parameter
    - PARAMETER
        - MUST
            - true : 100% selected
            - false: 50%
        - ELEMENT
            - parameter
- example
```xml=
<root>
  <ARGV>
      <ELEMENT>./djpeg @@</ELEMENT>
 </ARGV>

  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-colors 8</ELEMENT>
    <ELEMENT>-colors 9</ELEMENT>
    <ELEMENT>-colors 10</ELEMENT>
    <ELEMENT>-colors 50</ELEMENT>
    <ELEMENT>-colors 99</ELEMENT>
  </PARAMETER>	  
  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-fast</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-grayscale</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-rgb</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-rgb565</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-scale 1/7</ELEMENT>
    <ELEMENT>-scale 1/3</ELEMENT>
    <ELEMENT>-scale 2/3</ELEMENT>
    <ELEMENT>-scale 2/1</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-bmp</ELEMENT>
    <ELEMENT>-gif</ELEMENT>
    <ELEMENT>-os2</ELEMENT>
    <ELEMENT>-pnm</ELEMENT>
    <ELEMENT>-targa</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-dct int</ELEMENT>
    <ELEMENT>-dct fast</ELEMENT>
    <ELEMENT>-dct float</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-dither fs</ELEMENT>
    <ELEMENT>-dither none</ELEMENT>
    <ELEMENT>-dither ordered</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-nosmooth</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-onepass</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-maxmemory 1</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>true</MUST>
    <ELEMENT>-outfile /dev/null</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-memsrc</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-skip 0,20</ELEMENT>
    <ELEMENT>-skip 0,21</ELEMENT>
    <ELEMENT>-skip 1,20</ELEMENT>
    <ELEMENT>-skip 1,21</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>false</MUST>
    <ELEMENT>-crop 5x5+3+3</ELEMENT>
  </PARAMETER>
  <PARAMETER>
    <MUST>true</MUST>
    <ELEMENT>@@</ELEMENT>
  </PARAMETER>
</root>
```
        
### how to run
- Meanshift
    ```
        python3 group_argv_file.py 8090 valid invalid
    ```
- Guan-Fuzz
    ```
        ./Guan-fuzz -i in -o out -s ./parameter.xml -m none -d -p 8090 ./djpeg
    ```
    - argument usage like AFL: https://github.com/google/AFL
    - `-p`: connect Meanshift
