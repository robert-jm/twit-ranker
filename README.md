twit-rank
=========

CIS400 Final Project

swn3.txt is the SentiWordNet database file. It cannot be distributed publicly without the permission from its creators.



# Filter

## Accessing the Word Frequency List

To access the word frequency list, you will have to unpickle the file wordfreq.pkl. The list is stored as a dictionary, using the word as the key and WordFreq as the value. WordFreq is a namedtuple and the declaration for it is

`from collections import namedtuple
WordFreq = namedtuple('WordFreq', ['rank','pos', 'frequency', 'dispersion'])`

## Language Identifier

To use the language identifier, simply look at the README in the guess_language folder.


# Ranker

## SentiWordNet

swn3.txt is the SentiWordNet database file. It cannot be distributed publicly without the permission from its creators.

