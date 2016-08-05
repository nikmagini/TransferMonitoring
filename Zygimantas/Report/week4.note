# week 4

## 2016-07-18
- Upgrading to DCAFPilot 0.1.26 

## 2016-07-19

### Prolog
File of ~20 MB size with transfer data contains 10000 records and has around 60 atributes. In hadoop cluster, transfer log for 1 day is between 1-5GB, making there is about 500 000 - 2 500 000 records for 1 day. A lot of unique strings

### Work
Decided to think better solution to stringToHash(string) function. It looks like a simple problem, but not so simple solved.
Training algorithms from DCAFPilot package takes values as float32, while the following line produce 68 numeral long _double_ :
```python
int(hashlib.md5(string).hexdigest(), 16)
```  
What I need is to shorten outputed hash value so it can be stored in float32. 

This would typecast to _inf_ float32 and crash ML algorithms. Short workaround would be just to  shorter the number, however, around 2/3 of data hash is lost *from one place* making hash colusions very posible. 
```python
int(hashlib.md5(string).hexdigest()[:18], 16)
```

I had few sugestions to solve this problem:
- Take this long number and use log() function on it - this will simply reduce the size proportonaly to original number;
- For every distinct _string_ assign unique number and track them in seperate dictonary. Basicly write my own hash function. However, with milions of records, this may get compiuting intensive, and I still need to store dictonary with {string:value} somewhere. Not practical.
- use simple build in hash() function. This will return _int32_ on 32 bit systems, and _int32_ on 64bit. Both can be typecasted to _float32_. Since i use 64 bit VM, I see that I can get fairly big   

Diceding between 1st and 3rd option I diceded to bencmark time of both solutions and see the outcome:

```python
>>> import time
>>> import hashlib
>>> import math
>>> string1="very long string"
>>> 
>>> start = time.time()
>>> print hash(string1)
1702804156704783893
>>> end = time.time()
>>> print(end - start)
0.000827074050903
>>> 
>>> start = time.time()
>>> math.log10(int(hashlib.md5(string1).hexdigest(), 16))
38.42663567937796
>>> end = time.time()
>>> print(end - start)
0.00196099281311

``` 

```python
>>> import time
>>> import hashlib
>>> import math
>>> 
>>> string = """
... I had few sugestions to solve this problem:
... - Take this long number and use log() function on it - this will simply reduce the size proportonaly to original number;
... - For every distinct _string_ assign unique number and track them in seperate dictonary. Basicly write my own hash function. However, with milions of records, this may get compiuting intensive, and I still need to store dictonary with {string:value} somewhere. Not practical.
... - use simple build in hash() function. This will return _int32_ on 32 bit systems, and _int32_ on 64bit. Both can be typecasted to _float32_.
... """
>>> 
>>> start = time.time()
>>> print hash(string)
3043140891630325632
>>> end = time.time()
>>> print(end - start)
0.000776052474976
>>> 
>>> start = time.time()
>>> math.log10(int(hashlib.md5(string).hexdigest(), 16))
38.14445811227407
>>> end = time.time()
>>> print(end - start)
0.00212597846985

```

The difference is about 2-3 times in favor of hash() fucntion.

At first I was concerned that by converting _int_ to _float32_ I may lose some data and I can get some unexpected results, however since I don't have to wory about converting hash values back to strings and I only care to seperate strings from each other, this seems good enough solution.

*Update*

- It looks like it is just a trivial problem, meaning however I solve it I can get the same outcome. Most of the time if the hash digest ( the output) is to long to store in, it is simple trunktated(for example default python _hash()_ function). It is the same probability the have hash clash if the values are trunktated or shortened using different algorithms since simple i will have smaller amount of numbers. 

## 2016-07-20

- Hadoop tutorial

## 2016-07-21

- Create a script csvSplit.py to nicely split csv file to train and test data. Wrote in such a way that it should be able to process huge file. 

## 2016-07-21

- checkPredictions.py added