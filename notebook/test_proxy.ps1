Write-Host "--- Starting Proxy Tests ---" -ForegroundColor Cyan

# 1. Test standard HTTP forwarding
Write-Host "Test 1: HTTP Forwarding (neverssl.com)..."
curl.exe -I -x 127.0.0.1:8888 http://neverssl.com

# 2. Test HTTPS Tunneling
Write-Host "`nTest 2: HTTPS Tunneling (wikipedia.org)..."
curl.exe -I -x 127.0.0.1:8888 https://www.wikipedia.org

# 3. Test Blocking
Write-Host "`nTest 3: Blacklist Filtering (google.com)..."
curl.exe -I -x 127.0.0.1:8888 https://www.google.com

# 4. Test Malformed Request
Write-Host "`nTest 4: Malformed Request..."
echo "NOT_A_VALID_HTTP_REQUEST" | nc localhost 8888

Write-Host "`n--- Tests Complete. Check docs/proxy.log for results. ---" -ForegroundColor Green