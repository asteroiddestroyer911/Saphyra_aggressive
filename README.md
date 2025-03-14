# Saphyra Aggressive


Overview: Saphyra Aggressive is a Python-based HTTP flooder designed for stress testing web servers. This tool simulates a high volume of HTTP requests to evaluate the performance and resilience of web applications under heavy load. It is intended for educational purposes and should only be used in environments where you have explicit permission to conduct such tests.


## Features:

• Multi-threaded Requests: Launches up to 1000 concurrent threads to maximize request throughput.

• Randomized User Agents: Utilizes a list of common user agents to mimic real user traffic and evade basic detection mechanisms.

• Dynamic Referers: Generates random referer headers to further disguise the nature of the requests.

• Error Handling: Implements robust error handling for HTTP errors, including rate limiting (HTTP 429) and connection failures.

• Request Monitoring: Tracks the number of requests sent and provides real-time feedback on the attack progress.

• Configurable Parameters: Allows users to specify the target URL and port for the attack.


## Usage: To use Saphyra Aggressive, run the following command in your terminal:

```bash
python Saphyra_aggressive.py <url> <port>
```

Replace with the target URL (must start with http:// or https://).

Optionally specify (default is 80).

# Requirements:

1. Python 3.x

2. urllib library (included in standard Python library)
