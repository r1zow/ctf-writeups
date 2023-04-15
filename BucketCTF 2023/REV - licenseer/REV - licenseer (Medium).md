> Help! I tried writing my new authentication server in go, and I forgot the password!
> 
> nc dev.fyrehost.net 54321

Load the downloaded executable file into the IDA. The first thing we do is analyze the functions that the IDA detected. Find the two functions main_main and main_verifyKey.

![](BucketCTF%202023/REV%20-%20licenseer/1.png)

Let's see what's in the main function of the program. We see that the loop reads user input and passes it to the main_verifyKey function. If the function returns true, then the flag from env is read and output. Let's see what happens in the main_verifyKey function.

![](BucketCTF%202023/REV%20-%20licenseer/2.png)

In the main_verifyKey function we see that the MD5 hash of the data entered by the user is counted. Then this hash is compared with another hash. 

![](BucketCTF%202023/REV%20-%20licenseer/3.png)

Let's try to connect via nc and enter this hash. The program gave out a password - **passWord1234!!**.
Next, we connect to the container of the task, pass the received password and get the flag!

 > Flag: **bucket{HASH1NG_IS_S0_FUN_2f47d31e7c28d}**
