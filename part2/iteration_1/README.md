### Architecture
This is my first solution to this problem.
The architecture here consists of 3 independant layers of worker, that share data through 2 queues. The independant layers mean that resources can be scaled up or down to eliminate bottlenecks, and that failures can be contained to the layer where they occur.
It also makes the code modular, and easy to debug.

The first layer has a worker for each url. It’s only job is to send a request object to the first queue (request_queue) every interval seconds, meaning that scheduling is maintained accurately, regardless of any events that happen later.

The second layer of workers are doing the bulk of the work, taking jobs from the request_queue and making requests. Regardless of the success of the request, they send a response objects to the second queue (response_queue). I tried to keep them as lean as possible, because they do the heavy lifting, are time sensitive, and are likely where most of the resources would go if the application was to be scaled.

The third layer takes response objects and puts them into the appropriate database. I chose to the results of successful queries separatley from those that had errors to keep the tables neat, which also made for easier querying.

Finally, there is a single worker logging stats on the state of the application.

### Limitations
There are however, two major drawback to this architecture.

First, if the list of inputs were to become quite large, there would be a worker for each url to be queried. If a large number of requests needed to be issued at the same time, the context switching required to manage all these independant processes might produce significant delays.
The exact scope of this issue would depend on the number of url to be queried, and how often a number of them need to be queried at the same time.
For example, if all the workers in the first layer were intialised at the same time, this problem would be particularly acute if the intervals had a low LCM, and would be less problematic if there were many prime number intervals producing a high LCM, and thus less frequently requiring all the workers to act at the same time.

This leads us to the second problem, which is that in this architecture, there is no mechanism to stagger the work of either of the first two layers. In the worst case, if all the inputs had the same interval and the first layer of workers was intialised at the same time, all the workers would sit idle for the duration of the interval, and then a large number of requests would come due at the same time. This is a serious concern and in the second solution I am going to implement, I will try to address this concern with a priority queue and some version of exponential backoff to balance out the work.

Ideally I would want to incorporate a mechanism to monitor the usage of resources and dynamically adjust the number of workers, though I doubt I will be able to implement it at present.

I would also choose more scalable queueing systems (like RabbitMq) and databases(like Cassandra) in
an actual implementation, here I chose to go with quick and easy solutions to produce a working prototype.

Unresolved Issues
There are two issues in this solution that I aware of but am unable to address at present.

The first is fairly obvious, when logging the urls currently being checked, the acutal urls are replaced by the string “url”. Trying to put the actual url into that multiprocess array was causing errors and the program to crash, for reasons I am yet to fully comprehend.
The second is more serious and evident in the printed logs as well, the Longest response time in the last 5 mintues was at times larger than the maximum wait time for a page to respond. I looked into this breifly but was unable to see why it was happening, and time permitting I will go back and investigate more thoroughly.
