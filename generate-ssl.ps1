# Generate SSL Certificates for Development/Testing
Write-Host "🔐 Generating SSL certificates..." -ForegroundColor Green

# Create ssl directory if it doesn't exist
if (!(Test-Path "ssl")) {
    New-Item -ItemType Directory -Path "ssl"
    Write-Host "Created ssl directory" -ForegroundColor Yellow
}

# Check if OpenSSL is available
try {
    $opensslVersion = openssl version
    Write-Host "✅ OpenSSL found: $opensslVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ OpenSSL not found. Please install OpenSSL for Windows." -ForegroundColor Red
    Write-Host "   Download from: https://slproweb.com/products/Win32OpenSSL.html" -ForegroundColor Yellow
    Write-Host "   Or use Git Bash which includes OpenSSL" -ForegroundColor Yellow
    exit 1
}

# Generate private key
Write-Host "Generating private key..." -ForegroundColor White
openssl genrsa -out ssl/nginx.key 2048

# Generate certificate signing request
Write-Host "Generating certificate signing request..." -ForegroundColor White
openssl req -new -key ssl/nginx.key -out ssl/nginx.csr -subj "/C=BR/ST=RS/L=Novo Hamburgo/O=Cadastro Unificado/CN=10.13.65.37"

# Generate self-signed certificate
Write-Host "Generating self-signed certificate..." -ForegroundColor White
openssl x509 -req -days 365 -in ssl/nginx.csr -signkey ssl/nginx.key -out ssl/nginx.crt

# Clean up CSR file
Remove-Item ssl/nginx.csr -ErrorAction SilentlyContinue

Write-Host "✅ SSL certificates generated successfully!" -ForegroundColor Green
Write-Host "📁 Files created:" -ForegroundColor Yellow
Write-Host "   - ssl/nginx.key (private key)" -ForegroundColor White
Write-Host "   - ssl/nginx.crt (certificate)" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Note: These are self-signed certificates for development only." -ForegroundColor Yellow
Write-Host "   For production, use certificates from a trusted CA." -ForegroundColor Yellow 