
# TRON Wallet - Mobile App Backend

A complete REST API backend for a TRON cryptocurrency wallet mobile application supporting TRX and USDT-TRC20 tokens.

## Features

✅ **Wallet Management**
- Create new wallets (auto-generate address + private key)
- Import existing wallets via private key
- List, view, and delete wallets
- Export private keys securely

✅ **Transaction Features**
- Send TRX and USDT-TRC20 tokens
- Check real-time balances
- View transaction history
- Generate QR codes for receiving

✅ **Security**
- PIN-based authentication
- Optional password protection
- JWT token-based sessions
- Biometric auth support (mobile integration)

✅ **Demo Mode**
- Auto-generate realistic fake profiles
- USA/UK/Australia phone numbers
- Gmail-style email addresses
- 8-character passwords
- Fake wallet balances

✅ **API Documentation**
- Interactive Swagger UI at `/docs`
- Complete REST/JSON endpoints
- Ready for mobile app integration

## Quick Start

1. **Install dependencies:**
```bash
pip install tronpy fastapi uvicorn pydantic python-multipart qrcode pillow pyjwt passlib faker python-dotenv
```

2. **Run the server:**
```bash
python main.py
```

3. **Access API documentation:**
```
http://0.0.0.0:5000/docs
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login with PIN

### Wallets
- `POST /wallets/create` - Create new wallet
- `POST /wallets/import` - Import wallet with private key
- `GET /wallets` - List all wallets
- `GET /wallets/{id}` - Get wallet details
- `DELETE /wallets/{id}` - Delete wallet
- `GET /wallets/{id}/export` - Export private key

### Transactions
- `GET /balance/{address}` - Get TRX and USDT balance
- `POST /send` - Send TRX or USDT tokens
- `GET /transactions/{address}` - Get transaction history

### Utilities
- `GET /qr/{address}` - Generate QR code

### Demo
- `GET /demo/generate` - Generate demo profile
- `GET /demo/profile` - Get new demo profile

## UI/UX Design

Complete design specifications are available in `UI_DESIGN_SPEC.md`:
- TRON brand colors and gradients
- Screen layouts for all flows
- Component library
- Interaction patterns
- Mobile-first design (iOS/Android)

### Recommended Screens
1. **Auth:** PIN entry, biometric, password setup
2. **Home:** Balance overview, quick actions, recent transactions
3. **Wallet Detail:** Address, QR code, transaction history
4. **Send:** Recipient, amount, confirmation
5. **Receive:** QR code, address display
6. **Create/Import:** New wallet generation, key import
7. **Wallets:** List and manage multiple wallets
8. **Demo:** Generate fake realistic profiles
9. **Settings:** Security, preferences, about

## Tech Stack

**Backend:**
- FastAPI (REST API)
- TronPy (TRON blockchain integration)
- JWT (Authentication)
- Faker (Demo data generation)

**Recommended Frontend:**
- React Native (iOS/Android)
- TypeScript
- React Navigation
- Biometric authentication libraries

## Security Notes

⚠️ **Important:**
- Change `SECRET_KEY` in production
- Use secure storage for private keys (Keychain/Keystore)
- Never expose private keys in logs
- Implement rate limiting in production
- Use HTTPS for all API calls
- Currently uses testnet (Nile) - switch to mainnet for production

## Network Configuration

Currently configured for TRON Nile Testnet. To use mainnet:

1. Change `network='nile'` to `network='mainnet'` in `main.py`
2. Update USDT contract address if needed
3. Test thoroughly before deploying

## Development

Run with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## Deployment on Replit

The app is configured to run on port 5000 and is ready for deployment on Replit.

## License

MIT License - feel free to use for your projects!
