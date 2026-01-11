Technical Design Document: Custom Network Proxy Implementation

1. System Overview

This project is a high-performance Forward Proxy Server designed to handle HTTP and HTTPS traffic. It serves as an intermediary gateway, providing a controlled environment for network requests, traffic logging, and domain-level security.

Core Functional Modules:

>TCP Listener: Utilizing the AF_INET family and SOCK_STREAM type to manage low-level TCP handshakes.

>Traffic Parser: Analyzes raw ingress bytes to identify the HTTP method and destination URI.

>Security Filter: Implements a rule-based engine to intercept and terminate unauthorized requests.

>Bi-directional Relay: Facilitates a full-duplex communication channel between the client and the remote host.

2. Concurrency Architecture

The system implements a Multithreaded "Thread-per-Connection" model.

Design Rationale:
To ensure the proxy remains non-blocking, each accepted connection is offloaded to a dedicated worker thread. This ensures that a high-latency response from a remote server (e.g., a slow website) does not impact the throughput of other active clients. The use of Daemon Threads ensures that the background workers are synchronized with the lifecycle of the main server process.

3. Protocol Handling & Tunneling

The proxy supports two distinct modes of data transfer:

A. HTTP Forwarding (Stateless)
For standard HTTP traffic, the proxy acts as a "Request-Response" bridge. It parses the host from the URI and forwards the exact packet headers to the destination on Port 80.

B. HTTPS Tunneling (The CONNECT Method)
Modern encrypted traffic requires an Opaque Tunnel. When a CONNECT request is detected, the proxy establishes a TCP connection to the destination (usually Port 443) and returns a 200 Connection Established status to the client. After this handshake, the proxy transitions into a transparent relay mode, piping encrypted TLS data bidirectionally without modification.

4. Security & Traffic Control

Domain Normalization and Filtering

The filtering engine does not rely on simple string matching, which is easily bypassed. Instead, it performs Host Normalization:

1. Stripping port numbers from the host string.

2. Converting the host to lowercase to ensure case-insensitive matching.

3. Suffix Matching: Using a recursive-style check so that blocking google.com automatically covers all subdomains (e.g., mail.google.com).

Error Resilience
The system implements Socket Timeouts (set to 15 seconds) to prevent resource exhaustion from "half-open" connections or unresponsive remote servers.

5. Logging and Observability
All system activity is recorded via a dual-output Logging Module. This satisfies the requirement for "Traceability."

>Level INFO: Records successful connections and data transfer sizes.

>Level WARNING/ERROR: Captures timeouts, connection resets, and security violations.

>Persistence: Logs are stored in docs/proxy.log with high-resolution timestamps for post-incident analysis.