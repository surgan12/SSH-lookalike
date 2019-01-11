# SSH-lookalike
SSH protocol implemented using python (without paramiko).

***Description:***


Through this a client can securely connect to host , run terminal commands ,get files and have safe communication.
Using symmetric encryption to make the connection secure.


***Things used:***

1.Sockets for connection between clients and host.

2.Multithreading for handling of multiple clients at host side.

3.DIFFIE-HELLMAN key exchange algorithm for secure and encrypted connection.

4.AES encryption for authentication,communication.
 
links:

https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange

https://en.wikipedia.org/wiki/Advanced_Encryption_Standard

To run this :

Default port is set for host as 6002
Since the user on connection with host will go directly to the home directory of host, so change that to your respective 
directories.
