#!/usr/bin/python2.7
import sys

def oneTimePad(otp, file):
    #read contents from file
    f = open(file, "r")
    contents = f.read()
    print(contents)
    
    #if the key is shorter than the filename, repeat the key until it is the same size
    while(len(otp) < len(contents)):
        otp += otp
    #call the encryp function, it returns the encrypted text
    ciphertext = encrypt(contents, otp)
    print(ciphertext)
     #to test, xor the key with the ciphertext, this should result in the original plaintext content
    plaintext = encrypt(ciphertext, otp)
    print(plaintext)
   
    
#key has already been mutated to have the size necessary to compute
def encrypt(text, key):
    
    #get the integer ASCII value for each character in the file and for each character in the key      
    text_array = []
    key_array = []
    for each in text:
        text_array.append(ord(each))

    for each in key:
        key_array.append(ord(each))    
        
    #for the length of the file encrypting, xor the characters at the same index of the file content and the key
    ciphertextarray = []
    idx = 0
    while(idx < len(text_array)):
        ciphertextarray.append(text_array[idx] ^ key_array[idx])
        idx += 1
    #ciphertextarray now stores the xored int values  
    
    #convert each element in ciphertextarray to a character, then concatenate into string
    ciphertext = ""
    for each in ciphertextarray:
        ciphertext += str(unichr(each))
    return ciphertext
    
#key = "avxjdsldkfjehsdfjlsdkrlhnvsfdojsldfsifysdfjosduhfpofjpwehjbksdjfbksf"
#filename = "one_time_pad_file_to_encrypt.txt"
if len(sys.argv) != 3:
	exit('usage ./rot.py k f_name')
key = sys.argv[1]
print(key)
filename = sys.argv[2]
oneTimePad(key, filename)


