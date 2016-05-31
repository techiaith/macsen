MACSEN
======

Macsen is software that provides an open source Welsh language personal digital assistant. Mascen is based on the Jasper project. It can run on a Raspberry Pi. Here you will find code, scripts and documentation on how you can install and customize Mascen yourself. 

## Installing Macsen on the Raspberry Pi

```
$ mkdir src
$ cd src
$ git clone https://github.com/techiaith/macsen.git
$ cd macsen
$ ./setup-rpi.sh
```

## Running Macsen for the first time

You will need to create a profile before you run Macsen for the first time so that he can get to know you a little first, e.g. know your first name etc.  Run the following script and answer its questions

```
$ python client/populate.py
```

After you've answered every question, you can start Macsen by :

```
$ python jasper.py  
``` 

## Macsen -

Macsen depends on the work done by Bangor University's Language Technologies Unit to develop Welsh language speech recognition  see – [julius-cy](https://github.com/techiaith/julius-cy)
