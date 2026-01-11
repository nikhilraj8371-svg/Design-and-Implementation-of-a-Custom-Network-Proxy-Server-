# Proxy Usage Demonstration

## 1. Starting the Server
Run the following command in the terminal:
`python src/main.py`
*Expected Output:* `2026-01-06 01:15:34,784 - Proxy Server running on 127.0.0.1:8888`

## 2. Standard HTTP Request
Command: `curl.exe -x 127.0.0.1:8888 http://neverssl.com`
Result: The terminal displays the HTML source code of the website.

## 3. HTTPS Tunneling
Command: `curl.exe -x 127.0.0.1:8888 https://www.wikipedia.org`
Result: The proxy logs show `200 Connection Established` and data is relayed successfully.

## 4. Security Filtering (Blacklist)
Command: `curl.exe -x 127.0.0.1:8888 http://google.com`
Result:The client receives `403 Forbidden` and the proxy logs the security block.