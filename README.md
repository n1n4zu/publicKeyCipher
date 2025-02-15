# Public Key Cipher
#### Author: n1n4zu
#### Copyright: Copyright (C) 2025 n1n4zu
#### License: MIT license
This program was created to help you keep your data safe. With this program you can 
generate the pair of public and private keys and encrypt and decrypt data using them.
You can encrypt any file you want with any extension. The encrypted file will be stored
in a binary file that is called **encrypted.bin** in default.
## How to run
#### Remember to keep all files in the same directory.
### Windows
Run the **publicKeyCipher.exe** file.
### Linux
1. Open the terminal
2. Go to the directory where the program is located
3. Run the following command:
```commandline
$ ./publicKeyCipher
```
## How to use
### Creating keys
```commandline
Input key name:
> example_key_filename
```
### Encryption
```commandline
Input file name:
> example.pdf

Choose mode (encrypt/decrypt):
> encrypt

Input public key filename:
> example.pub
```
### Decryption
```commandline
Input file name:
> encrypted.bin

Choose mode (encrypt/decrypt):
> decrypt

Input public key filename:
> example
```
I hope it will help you keep your data safe.