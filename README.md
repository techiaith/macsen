MACSEN
======


Mae Macsen yn feddalwedd cynorthwyydd personol digidol Cymraeg cod agored. Mae'n rhedeg ar y Raspberry Pi. Yma ceir ffeiliau a sgriptiau yn ogystal â dogfennaeth ar gyfer gosod ac addasu Macsen eich hunain.

## Gosod Macsen ar eich Raspberry Pi

```
$ mkdir src
$ cd src
$ git clone https://github.com/techiaith/macsen.git
$ cd macsen
$ ./setup-rpi.sh
```

## Rhedeg Macsen am y tro cyntaf

Mae angen proffil creu proffil ar gyfer Macsen cyn ei redeg am y tro cyntaf, er mwyn iddo wybod eich enw a.y.b.  Rhedwch y sgript ganlynol ac atebwch y cwestiynau 

```
$ python client/populate.py
```

Ar ôl ateb pob cwestiwn, mae modd cychwyn Macsen drwy rhedeg

```
$ python jasper.py  
``` 

## Manylion Macsen

Datblygwyd Macsen ar sail gwaith adnabod lleferydd Cymraeg Uned Technolegau Iaith, Prifysgol Bangor – julius-cy  - a Jasper. 
