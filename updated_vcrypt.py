#!/usr/bin/python2.7

import sys, base64, re
input_base64 = False

def encr(text, key):
  key_len=len(key)
  l = [text[i:i+key_len] for i in xrange(0,len(text), key_len)]
  r = ''
  for i in l:
    if len(i) < key_len: #padding needed
       i = i + ' '  * (key_len - len(i))
    t=''
    for n, j in enumerate(i):
      t+=chr(ord(j) ^ ord(key[n]))
    assert(len(t) == key_len)
    r+=t 
  return r

#gets a list of factors of a number
def factors(n):
  l = []
  #we don't care about 1, so start at 2
  for i in range(2,n):
    if n % i == 0:
      l.append(i)
  return l

def getKeyLength(s):
  #dic will have: (ch as key, then frequency of appearence in text
  dic = {}
  #factorList will have a list of all factors of the difference in distances between two matching three character strings
  factorList = []
  
  for i in range (0, len(s) - 3):
    #get the first three characters
    ch1 = s[i:i+3]
    #compare those first three to every other set of three
    for j in range(i+1, len(s) - 3):
      ch2 = s[j:j+3]
      if(ch1 == ch2):
        #add the factors of the difference in distance between the character occurences
        factorList.extend(factors(j-i))
  
  #populate dic with the frequency of occurence of each factor calculated above
  for x in factorList:
    if x not in dic:
      dic[x] = 1
    else:
      dic[x] += 1
  
  #sort the dictionary in reverse order so factor, frequency is in descending order
  newList = sorted(dic.items(), key=lambda x: x[1], reverse=True)
  
  #now have a list of: (factors, frequency)
  '''
  use idx to find the index of the list where the value (first element in each i)is no longer a multiple of the previous ones. For example, in this case it goes: 2, 4, 8, 16, 32, 3, 6, etc. This means we want the index of 16 b/c it is a multiple of the previous elements and within 2-20 key length restriction. We could look at the frequency too to be sure.
  '''
  #default key length to the greatest frequency.
  keySize = newList[0][0]
  i = 0
  #while the next value is divisible by the previous
  while (newList[i+1][0] % newList[i][0] == 0):
    #make sure between 2 and 20 characters long
    if (newList[i+1][0] >= 2 and newList[i+1][0] <= 20):
      keySize = newList[i+1][0]
    i += 1
  
  return keySize
    

if len(sys.argv) != 2:
  exit('Usage: ./crypt.py "key" input_file_name')
#key = sys.argv[1]
fname = sys.argv[1]


#fname = "ciphertext_vig.txt"
s = open(fname).read()


#detect base 64
if re.match('^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$', s):
  input_base64 = True
  s = base64.b64decode(s)
keyLength = getKeyLength(s)
print "key length is ", keyLength
'''
c = encr(s, key)

if input_base64: # print plaintext
  print c
else:
  c_64 = base64.b64encode(c)
  print c_64
'''