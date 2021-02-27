# keylogger
keylogger with extra features- written with python

this is a code for a keylogger that does a bit more than just document the keys pressed, it also tracks the information of the computer it is ran on (public and private IP, processor, machine, system, and host name),
it also gets the clipboard contents, records the mic and gets a screenshot, the data is collected every chosen amount of time.
it organizes this data and puts it in a file, and furthermore, it sends all of the data it collected to a selected email address,
the program also encrypts the logs detected (in case that the user sees a file on his computer so that he would not be able to recognize that its the keys he pressed),
in order to generate a key and a file to decrypt the data, the cipher used is the fernet symmetric cipher (feel free to read about this specific cipher and about symmetric ciphers in general), the cryptography.fernet module is used is order to implement this encryption.

Note: i also wanted to record the keys in a database, so i used mysql for that and every group of keys that enter the file will also be added to a database with the time that it was entered, for convenience i added both a program with the database implemetation, and a program without it for anyone who does not know how to use mysql (but i incourage you to look for yourselves and learn, you will find out that it is not as frightening as it sounds).

enjoy :)
