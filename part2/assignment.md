## Assignment B

We want to check a list of urls at regular intervals, to make sure these are reachable and that we can get their content. Create a program that you can feed with a list of URLs and check intervals. For instance:
```
    [
      { "url": ‘http://cnn.com’, "interval": 100},
      { "url: 'http://google.ca’, "interval": 200},
      { "url": ‘http://cnn.com’, "interval": 150},
      { "url": ‘http://httpbin.org/delay/20’, "interval": 150}
    ]
```
where in each dictionary, _url_ is the url to be checked and _interval_ is the _number of seconds between checks_.

Provide a solution that performs such task and, as output, provides **timestamp**,  **url** and **length of the body**. 
Eg:
```
    13/11/17 11:18:20 - http://cnn.com - 231274 Bytes
    13/11/17 11:18:27 - http://google.ca - 55609 Bytes
    13/11/17 11:18:30 - http://cnn.com - 231274 Bytes
    13/11/17 11:18:47 - http://google.ca - 55609 Bytes
            …
```

Be mindful, in your implementation, that we need to respect _as much as possible_ the defined schedule. This means you have to think of a solution that isn't affected by the time a single URL takes, nor by the fact that some URLs fail. Consider the best design pattern for this, and keep in mind a certain degree of delay in the check is acceptable, the important thing is to avoid skipping checks.

 A few things we expect to see in this solution:
    - Error handling in case a URL returns a code different than `200` (consider some URLs migh be permanently unreachable but some other might just have a temporary glitch..);
    - data on the status of the system should be logged every minute:
        - how many URLs have been checked so far;
        - what URLS are currently being checked;
        - top 5 HTTP codes returned across all urls;
        - URL that took the longest to check in the past 5 minutes;
    - consider that there might be a _huge_ list of urls, but our system has only limited resources (workers) for checking them. Plan accordingly and consider the fact we can scale out and increase the resources for these checks or the fact all workers might be busy at some time;
    - a small delay on the scheduled time when checking the urls is acceptable;
    - we'd like to see some test cases for your implementation, checking the main features we outlined in the description of the problem (no need to test everything!);
    - consider cornercases that might arise from this implementation and tackle them accordingly;
    - feel free to add any other functionality you want and explain it to us!

An example list of urls is provided in `urls.json`. Feel free to enchance it with your own.
