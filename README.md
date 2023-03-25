### Implementing transmitter and receiver in Redis

Write a program that takes $ns as the first argument and file paths as the second and subsequent arguments. The following actions are performed:
1) From the arguments we form a list of files - this is the list of "what remains to be processed".
2) All elements of this list are added to Redis: LPUSH $ns:job $file $file .... By polling this list, the handler learns about the appearance of tasks.
3) If the list of remaining is empty - exit
4) For each of the files in the list of remaining ones, a string key value is requested: MGET $ns:res:$file $ns:res:$file ....
5) If no value is received, use BLPOP $ns:res 3, thus waiting for three seconds for any value to appear in the $ns:res list, then unconditionally go to step 4. There is a nuance here, see the notes below.
6) For everything that could be found, data is output to stdout in the form of $file $res\n, where $res is the received value; at the same time, the corresponding element is removed from the variable that stores the list of those remaining for processing.
7) Go to point 3.
The cmd-cjob key must contain the command to run this program.

`redis-cli set cmd-cjob "python3 /home/user/rds 14_handler.py"`

Write a program that takes $ns as the first argument and works like this:
1) Use BRPOPLPUSH on the $ns:job key to wait for the next $file element.
2) Calculate the sha1 hash of the contents of this file (as a hex string).
3) Write the result to the $ns:res:$file key.
4) Add an element with any value to the list under the $ns:res key: this is a signal to the client that a result has appeared.
5) Use LREM to remove the first found (from left to right) $file element from the $ns:job list.
6) Go to point 1.
The cmd-sjob key must contain the command to run this program.

`redis-cli set cmd-sjob "python3 /home/user/rds 14_receiver.py"`
