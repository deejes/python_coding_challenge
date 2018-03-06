### Architecture
This is the second iteration of my solution to part 2.
Here, the first layer of workers has been removed. Instead, the second layer now both executes a request and appends a new request to the request_queue, which is now a priority queue.

We are able now to receive the request before the scheduled time of the query, and have time to do precomputation and launch the query closer to the exact scheduled time. We can also adjust the time of the next query, allowing us to distribute request more evenly along the timeline, and consequently use our resources more efficiently by avoiding bunching.

### Limitations
In this setup, both scheduling and querying are being handled by the same worker, and if one were to encounter unexpected errors we could go off schedule for a particular url.
We are also still unable to see the utilisation rate of the resources, or to dynamically add or remove workers.
Also, while I have tested individual sections of code myself, comprehensive testing is glaringly lacking.

### Unresolved Issues
Both issues from the previous implementation remain unresolved.
In addition, there is a very not neat time.sleep() at the end of the main script.