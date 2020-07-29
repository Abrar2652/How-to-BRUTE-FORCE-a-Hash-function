#!/usr/bin/env python
# coding: utf-8

# ## How to BRUTE-FORCE a Hash function
# ### *Md. Abrar Jahin*
# #### 2nd year, Khulna University of Engineering and Technology
# To be a good Hash Function H(x), where y is the Hash value:
# 1. H must be efficient to compute
# 2. H must be deterministic
# 3. y must be random looking
# 4. H must be resistant to forgery
#    * It should be very time consuming to find collisions
#    * y should depend in every bit of the origin

# Using the standard library hashlib module I computed the MD5, SHA1 and SHA256 (that's SHA2 with a hash size of  n=256 ) of the string "Hello, world!"

# In[100]:


import hashlib

md=hashlib.md5()

md.update(b"Hello, world!")

sha1=hashlib.sha1()

sha1.update(b"Hello, world!")

sha2= hashlib.sha256()

sha2.update(b"Hello, world!")

print(md.hexdigest())

print(sha1.hexdigest())

print(sha2.hexdigest())


# I implemented a hash function `simple_hash` that given a string `s`, computes its hash as follows: it starts with r = 7, and for every character in the string, multiplies r by 31, adds that character to r, and keeps everything modulo  216 .

# In[101]:


def simple_hash(s):
    r = 7
    for c in s:
        r = (r * 31 + ord(c)) % 2**16
    return r


# I'll now Brute-force the hash function that I've just written in the above cell!
# 
# I've implemented a function `crack` that given a string s, loops until it finds a different string that collides with it, and returns the different string.

# In[102]:


import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
def crack(s):
    hash1=simple_hash(s)

    for i in range(10*2**16):
        s2 = get_random_string(4) # log(2^16)/log(26) ~ 4
        if simple_hash(s2)==hash1:
            break

    # print(i)
    return s2    # return s2 such that s != s2 and simple_hash(s) == simple_hash(s2)

print(crack('hello'))


# The function `weak_md5` is a "weaker" version of MD5, using only the first 5 bytes of the MD5 hash. This means its hashing size is  n=40  and it can be brute forced rather easily.
# 
# I implemented a function `find_collisions` that loops over all the possible strings until it finds an arbitrary collision - that is, two different strings whose hash is the same - and returns them (as a tuple).

# In[103]:


import hashlib
import itertools 
from itertools import product 
import string

def weak_md5(s):
    return hashlib.md5(s).digest()[:5]


def find_collisions():
    chars = string.ascii_letters + '1234567890' 
    d = {}  
    for i in range(40): 
        generator = itertools.product(chars, repeat = i) 
    for password in generator: 
        password = ''.join(password)
        h1 = weak_md5(password.encode('utf-8')) 
        if h1 not in d: 
            d[h1] = password 
        else: 
            return (password, d[h1])
     # return (s1, s2) such that s1 != s2 and weak_md5(s1) == weak_md5(s2)


# To see how hard it is to brute force a real hash function, I tried running the function that I wrote in the previous cell, but using the full MD5. 

# In[104]:


import hashlib


def md5(s):
    return hashlib.md5(s).digest()


def find_collisions():
    chars = string.ascii_letters + '1234567890' 
    d = {}  
    for i in range(40): 
        generator = itertools.product(chars, repeat = i) 
    for password in generator: 
        password = ''.join(password)
        h1 = weak_md5(password.encode('utf-8')) 
        if h1 not in d: 
            d[h1] = password 
        else: 
            return (password, d[h1])

