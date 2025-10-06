
# TRON Wallet API Specification

## Base URL
```
http://0.0.0.0:5000
```

## Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Endpoints

### 1. Authentication

#### POST /auth/register
Register a new user with PIN and optional password.

**Request:**
```json
{
  "pin": "1234",
  "password": "optional-password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user_id": "abc123"
}
```

#### POST /auth/login
Login with PIN and optional password.

**Request:**
```json
{
  "pin": "1234",
  "password": "optional-password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user_id": "abc123"
}
```

---

### 2. Wallet Management

#### POST /wallets/create
Create a new TRON wallet (requires authentication).

**Request:**
```json
{
  "name": "My Main Wallet"
}
```

**Response:**
```json
{
  "wallet_id": "a1b2c3d4",
  "name": "My Main Wallet",
  "address": "TJRabPrwbZy45sbavfcjinPJC18kjpRTv8",
  "created_at": "2024-01-15T10:30:00"
}
```

#### POST /wallets/import
Import existing wallet using private key (requires authentication).

**Request:**
```json
{
  "name": "Imported Wallet",
  "private_key": "a1b2c3d4e5f6..."
}
```

**Response:**
```json
{
  "wallet_id": "x9y8z7w6",
  "name": "Imported Wallet",
  "address": "TJRabPrwbZy45sbavfcjinPJC18kjpRTv8",
  "created_at": "2024-01-15T10:30:00"
}
```

#### GET /wallets
List all wallets for authenticated user.

**Response:**
```json
{
  "wallets": [
    {
      "wallet_id": "a1b2c3d4",
      "name": "My Main Wallet",
      "address": "TJRabPrwbZy45sbavfcjinPJC18kjpRTv8",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

#### GET /wallets/{wallet_id}
Get wallet details.

**Response:**
```json
{
  "wallet_id": "a1b2c3d4",
  "name": "My Main Wallet",
  "address": "TJRabPrwbZy45sbavfcjinPJC18kjpRTv8",
  "created_at": "2024-01-15T10:30:00"
}
```

#### DELETE /wallets/{wallet_id}
Delete a wallet.

**Response:**
```json
{
  "message": "Wallet deleted successfully"
}
```

#### GET /wallets/{wallet_id}/export
Export private key (use with caution!).

**Response:**
```json
{
  "private_key": "a1b2c3d4e5f6...",
  "address": "TJRabPrwbZy45sbavfcjinPJC18kjpRTv8"
}
```

---

### 3. Transactions

#### GET /balance/{address}
Get TRX and USDT-TRC20 balance.

**Response:**
```json
{
  "address": "TJRabPrwbZy45sbavfcjinPJC18kjpRTv8",
  "balances": {
    "TRX": 1500.50,
    "USDT": 5000.00
  },
  "updated_at": "2024-01-15T10:30:00"
}
```

#### POST /send
Send TRX or USDT-TRC20 tokens (requires authentication).

**Request:**
```json
{
  "from_address": "TJRabPrwbZy45sbavfcjinPJC18kjpRTv8",
  "to_address": "TXYZabcdef123456789",
  "amount": 100.50,
  "token_type": "TRX"
}
```

**Response:**
```json
{
  "transaction_id": "abc123def456",
  "from": "TJRabPrwbZy45sbavfcjinPJC18kjpRTv8",
  "to": "TXYZabcdef123456789",
  "amount": 100.50,
  "token": "TRX",
  "status": "broadcasted"
}
```

#### GET /transactions/{address}
Get transaction history.

**Query Parameters:**
- `limit` (optional, default: 20)

**Response:**
```json
{
  "address": "TJRabPrwbZy45sbavfcjinPJC18kjpRTv8",
  "transactions": [...],
  "count": 15
}
```

---

### 4. Utilities

#### GET /qr/{address}
Generate QR code for receiving address.

**Response:**
```json
{
  "address": "TJRabPrwbZy45sbavfcjinPJC18kjpRTv8",
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANS..."
}
```

---

### 5. Demo Mode

#### GET /demo/generate
Generate a realistic demo profile with fake data.

**Response:**
```json
{
  "phone": "+1-555-123-4567",
  "email": "john_doe2024@gmail.com",
  "password": "aB3$xY9z",
  "wallet_address": "TJRabPrwbZy45sbavfcjinPJC18kjpRTv8",
  "balance_trx": 2345.67,
  "balance_usdt": 8901.23
}
```

#### GET /demo/profile
Get a new demo profile each time (same as /demo/generate).

---

## Error Responses

All endpoints return standard HTTP status codes:

- `200 OK` - Success
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required or failed
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error response format:
```json
{
  "detail": "Error message"
}
```
