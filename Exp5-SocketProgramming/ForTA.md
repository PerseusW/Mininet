# For TA

This is the intellectual property of **171860611, 王麦迪**.

## Overview

I used C++ and OOP to finish this homework.

`HelloWorld` works.

`Bandwidth` works.

## 1 HelloWorld

`HelloWorld` is derived from `Bandwidth`, but only programmed to work locally. The interface that the server is bound to can be changed at the header part of `HelloWorld.cpp` since it is globally defined:

```c++
#define serverInterface "127.0.0.1"(Or another interface like "10.0.0.1" for mininet)
```

Note that client commands will also have to be changed:

```shell
./HelloWorld -c -h 127.0.0.1(Copy the IP interface above) -p 10000
```

To make life easier by not writing other shell scripts, I have written automatic test in `makefile` as well, and you can test my `HelloWorld` with the following commands:

```shell
$ make clean
$ make
$ make helloworld
```

There is nothing else to say.

## 2 Bandwidth

I initially started with a local version, but later realized that testing the local bandwidth has no meaning and I don't know if I've implemented it right or not. So, I'm directly presenting a `Mininet` version, where I can control the bandwidth and compare my results with the kernel `iperf` command.

The automatic testing process is implemented within [Test.py](Test.py), but to be consistent with `HelloWorld`, I've added a wrapper command, you can test via:

```shell
$ make clean
$ make
$ make bandwidth
```

### 2.1 Problems

Listing problems encountered.

#### 2.1.1 Actual `iperf`

The kernel `iperf` doesn't guarantee that bandwidth tested on Server/Client are the same:

<left>
    <img src="images\iperf.png", width=100%>
</left>

But since you said that "The results should be the same", I've added my mechanism to make this happen:

<left>
    <img src="images\myiperf.png", width=100%>
</left>

The server determines the start time and sends it to the client, then it starts sending the data payload. Once the client receives all of the payload, it determines the end time and sends it back to the server. Thus, we can be sure that the both of them have the same `Interval` and `Transfer`, and thus the same `Bandwidth`.

The only problem here is that the time is not entirely accurate:
$$
d(time) = d(transmission) + d(propagation)
$$
The inaccuracy comes from **propagation**. I chose this implementation because I didn't set any delay on the links in `Mininet`, so it shouldn't make a difference.

#### 2.1.2 `<time.h>` and `<chrono>`

Do not use `<time.h>` because it cannot provide the correct time elapse. Use `<chrono>`.