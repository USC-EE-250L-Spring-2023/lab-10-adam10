# Lab 10
[Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repo and clone it to your machine to get started!

## Team Members
- Adam Lewczuk

## Lab Question Answers

Question 1: Under what circumstances do you think it will be worthwhile to offload one
or both of the processing tasks to your PC? And conversely, under what circumstances
will it not be worthwhile?

Answer: Because offloading tasks to hardware signifantly speeds up a given process
compared to using packets, this should be used for computationally to speed up 
computationally expensive processes such as analog conversion, graphics processing, and 
machine learning. If the task requires less computation such that distributed computing
does not speed up the process, offloading may not be worthwhile in this instance.


Question 2: Why do we need to join the thread here?

Answer: This function is called for the program to stop execution until that thread
terminates. This is so that no new thread is called later in the program while the
previous thread is still occupying a portion of the CPUs memory, which could eventually
cause an overflow in the stack given enough thread instantiations.

Question 3: Are the processing functions executing in parallel or just concurrently?
What is the difference?

Answer: Concurrency is when multiple tasks start, run, and complete in 
overlapping time periods, in no specific order. Parallelism is when multiple tasks 
literally run at the same time on a piece of hardware. The code is running concurrently 
because the CPU is switching between multiple threads to execute tasks instead of 
running 2 tasks at once.

Source: https://freecontent.manning.com/concurrency-vs-parallelism/

Question 4: What is the best offloading mode? Why do you think that is?

Answer: The based offloading mode is often when both processes are multithreaded 
because both are sent to the PC which runs code significantly faster than the RPI,
a low-level embedded device.

Question 5: What is the worst offloading mode? Why do you think that is?

Answer: The worst offloading mode is often when no processes are threaded because 
they have to run sequentialy instead of distributing some of the computation to an 
alternative device to allow for simultaneous computation.

Question 6: The processing functions in the example aren't very likely to be used 
in a real-world application. 
What kind of processing functions would be more likely to be used in a real-world 
application?
When would you want to offload these functions to a server?

Answer: Functions that are far more computationally expensive such as graphics 
processing or user request processing for example are more likely to have 
multithreading implemented. Because a server has far more powerful computational 
power than a standard CPU, distributed computing in this instance should be used 
for the most intensive processing such as ML or running database software for 
example.