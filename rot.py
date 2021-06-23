#!/usr/bin/python2.7

import sys, base64, re
input_base64 = False

def decrypt(key):
  c = ''
  for i in s:
    c += chr(ord(i) ^ key % 256)
  #print "key: ", key
  
  if input_base64: # print plaintext
    print c
    
  else:
    c_64 = base64.b64encode(c)
    print c_64  

def frequencyAnalysisDecrypt():
  #basic idea: look for common characters in ciphertext to map to common characters in plaintext
  #we know 'e' is most common English character, so try to match that with a ciphertext char
  #we also know 'ee' frequently appears in English. Update: need to discount the most frequent character it maps to' ', not an English letter. I discount this b/c not everyone uses '  ' for after periods and to cover a text that has no spaces in English
  
  #NOTE: Checking for repeated chars is not necessary with this text, but just makes the algorithm stronger.
  
  #create dictionary of all characters in ciphertext with count of frequency
  cipherdic = {}
  #repeatdic will hold all two character repetitions and their frequency
  repeatdic = {}
  idx = 0
  #ch will hold each two repeated chars next to each other
  ch = ""
  
  for i in s:
    #i will be key of dictionary
    #if not in dictionary, create entry and set count to 1
    if i not in cipherdic:
      cipherdic[i] = 1
    #else, update increment count
    else:
      cipherdic[i] += 1
    #bounds checking
    if(idx < len(s) - 1):
      #if two adjacent chars are next to each other, add to repeatdic (same way as in cipherdic)
      #use ch as dictionary key for repeatdic
      if (s[idx] == s[idx + 1]):
        ch = s[idx] + s[idx + 1]
        if ch not in repeatdic:
          repeatdic[ch] = 1
        else:
          repeatdic[ch] += 1        
    idx += 1
  #reverse order sort cipherdic and repeatdic to get a list of most frequent chars (most frequent -> least frequent order)
  sorted_dic = sorted(cipherdic.items(), key=lambda x: x[1], reverse=True)
  #remove most frequent character in sorted_dic b/c it will map to ' ' in plaintext.
  sorted_dic.pop(0)
  sorted_repeat_dic = sorted(repeatdic.items(), key=lambda x: x[1], reverse=True)
  
  #both will be a list of all characters that are in the top five frequency that appear in both sorted_dic and sorted_repeat_dic. Just top 5 is used for simplicity (could include more but the letter that maps to 'e' should be among the top 5 most common characters)

  both = []
  #loop counters
  x = 0
  while(x < 6):
    y = 0
    while(y < 6):
      #if there is a single frequency match and a double frequency match, add to list
      if sorted_dic[x][0] == sorted_repeat_dic[y][0][:1]:
        both.append(sorted_dic[x][0])
      y += 1
    x += 1
  #both is naturally sorted using the looping above. This means that it is sorted using precedence of appearing more frequent by itself is more important than frequency of appearing repeated. 
  #remove the first element b/c it will map to ' '

  
  #first element should be mapped to e
  key = ord(both[0]) ^ ord('e') % 256
  decrypt(key)

  return 


'''
if len(sys.argv) != 3:
	exit('usage ./rot.py k f_name')
key = int(sys.argv[1])
f_name = sys.argv[2]
'''
f_name = "ciphertext_rot.txt"
s = open(f_name).read()
#detect base 64
if re.match('^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$', s):
  input_base64 = True
  s = base64.b64decode(s)
#brute force:
#for key in range(0, 256):
#  decrypt(key)

#frequency analysis
frequencyAnalysisDecrypt()
