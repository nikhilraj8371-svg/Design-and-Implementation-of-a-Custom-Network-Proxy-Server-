# Design-and-Implementation-of-a-Custom-Network-Proxy-Server

#Project demonstration

https://www.loom.com/share/2a48aa2fdbc84a8b8b2b23ea68bdafe5

(click on this link to see the video )



# Multi-Threaded Network Proxy Server
A high-performance, concurrent Python proxy server capable of handling HTTP and HTTPS traffic. This project was developed to demonstrate core networking principles, including TCP socket programming, multi-threaded concurrency models, and rule-based traffic filtering.



# Project Overview & Evolution

This project was built from the ground up to solve the challenge of intercepting, analyzing, and relaying network traffic. The development followed a phased engineering approach:


## Socket Foundation: Established a reliable TCP listener using the Python socket library to manage low-level handshakes.

## The Request Brain (Parser): Developed a custom parser to dissect raw HTTP streams. This allows the proxy to identify the destination host and port, even when the client uses different methods like GET or CONNECT.

## Concurrency Model: To prevent the server from "freezing" during long requests, I implemented a Thread-per-Connection architecture. This allows the proxy to handle dozens of users simultaneously by spawning isolated worker threads.

## The Security Guard (Filtering): I built a rule-based engine that performs host normalization and suffix matching. This ensures that if a domain like google.com is blocked, all its subdomains are also automatically restricted.

## HTTPS Tunneling: One of the biggest challenges was handling encrypted traffic. I implemented CONNECT Tunneling, which creates an opaque bi-directional bridge for TLS data, ensuring the proxy works with the modern, encrypted web.

 # Technical Features
 
## Concurrent Processing: Uses threading to ensure high availability and non-blocking I/O.

## Protocol Versatility: Seamlessly handles both standard HTTP (Port 80) and secure HTTPS (Port 443).

## Suffix Matching Logic: A robust security feature that prevents easy bypasses of the blacklist.

## Persistence: Implements a decoupled logging system that tracks timestamps, client IPs, and data transfer sizes.

## Graceful Shutdown: Handles Ctrl+C (SIGINT) to ensure ports are released and resources are cleaned up properly.



