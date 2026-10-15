# Lab 6: REST vs gRPC

All times are milliseconds per operation. The client was always on an e2-standard-2 VM in us-west1-a, using internal IP addresses.
- Local: server and client on the same VM
- Same-Zone: server on a second VM in us-west1-a
- Different Region: server in europe-west3-a (Frankfurt)

Repetitions: Local and Same-Zone used 1000 for add/dotproduct and 100 for the image calls. Different Region used 100 for add/dotproduct and 20 for the image calls.

| Method | Local | Same-Zone | Different Region |
|---|---|---|---|
| REST add | 2.53 | 3.57 | 349.77 |
| gRPC add | 0.76 | 1.47 | 166.33 |
| REST rawimg | 6.52 | 12.65 | 1465.39 |
| gRPC rawimg | 13.83 | 14.95 | 285.37 |
| REST dotproduct | 3.13 | 3.89 | 353.65 |
| gRPC dotproduct | 0.83 | 1.27 | 167.39 |
| REST jsonimg | 28.91 | 31.04 | 1542.06 |
| gRPC jsonimg | 25.44 | 30.23 | 259.63 |
| PING | 0.053 | 0.387 | 159.85 |

## Observations

For small messages (add, dotproduct), gRPC was faster in every setup: about 3-4x locally and about 2x across regions. The biggest factor is network latency. REST makes a new TCP connection for every query, so a call costs about two round trips (connection setup, then request and response). In Frankfurt, ping was about 160 ms and REST add took about 350 ms, roughly 2.2 round trips. gRPC reuses one connection, so its add took about 166 ms, roughly one round trip. In the same zone, latency is only about 0.4 ms, so the differences are small and the cost is mostly Python and serialization overhead.

For the 1.6 MB image calls, the results were mixed. Locally and in the same zone, gRPC was not faster than REST (for example, local rawimg was 13.8 ms for gRPC and 6.5 ms for REST), and I did not determine why. Across regions, gRPC was about 5x faster (285 ms vs 1465 ms for rawimg), which is likely because each REST request opens a new connection and has to send the large payload over a long-distance path, while gRPC reuses an established connection. The JSON image calls were slower than the raw image calls because base64 encoding makes the payload about a third larger and adds encoding and decoding work. My Frankfurt REST add time (about 350 ms) was higher than the roughly 270 ms mentioned in the assignment, probably because of a longer network path (ping was 160 ms).
