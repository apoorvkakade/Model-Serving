/*
Load Testing is primarily concerned with assessing the current performance of your system
in terms of concurrent users or requests per second.
When you want to understand if your system is meeting the performance goals, this is the type of test
you'll run.
Run a load test to:
Assess the current performance of your system under typical and peak load
- Make sure you are continuously meeting the performance standards as you make changes to your system
Can be used to simulate a normal day in your business
*/

import http from 'k6/http';
import {check,sleep} from 'k6';

export let options = {
    insecureSkipTLSverify: true,
    noConnectionReuse: false,
    stages: [
        { duration: '5m', target: 100 }, // simulate ramp-up of traffic from 1 to 100 users over 5 minutes
        { duration: '10m', target: 100 }, // stay at 100 users for 10 minutes
        { duration: '5m', target: 0 }, // ramp-down to 0 users
    ],
    thresholds: {
    http_req_duration: ['p(99) <150'], // 99% of requests must complete bel\w 15
    },
};
    export default () => {
    // let response = http.get("https://localhost: 5001/youtube");
    // sleep (1);
    const res = http.get('https://httpbin.test.k6.io/');
    check(res, { 'status was 200': (r) => r.status == 200 });
    sleep(1);
};