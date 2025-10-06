
# 🚀 TRON Wallet - Complete Mobile App Backend + Demo UI

A full-stack TRON cryptocurrency wallet with REST API backend and interactive web demo. Supports TRX and USDT-TRC20 tokens with complete wallet management, transactions, and demo mode.

## ✨ Features

### 🔐 Authentication & Security
- PIN-based authentication (4-6 digits)
- Optional password protection
- JWT token-based sessions
- Ready for biometric integration (mobile)
- Secure private key management

### 💼 Wallet Management
- ✅ Create new wallets (auto-generate address + private key)
- ✅ Import existing wallets via private key
- ✅ List, view, and delete wallets
- ✅ Export private keys securely
- ✅ Multi-wallet support

### 💸 Transactions
- ✅ Send TRX and USDT-TRC20 tokens
- ✅ Check real-time balances
- ✅ View transaction history
- ✅ Generate QR codes for receiving
- ✅ Transaction confirmation flows

### 🎭 Demo Mode
- ✅ Auto-generate realistic fake profiles
- ✅ USA/UK/Australia phone numbers
- ✅ Gmail-style email addresses
- ✅ 8-character passwords
- ✅ Fake wallet balances
- ✅ Perfect for testing and presentations

### 📱 Mobile-Ready API
- ✅ Complete REST/JSON endpoints
- ✅ Interactive Swagger documentation
- ✅ CORS enabled for mobile apps
- ✅ Ready for React Native/Flutter integration

## 🚀 Quick Start

### 1. Run the Application

Click the **Run** button at the top of the Repl, or use:

```bash
python main.py
```

### 2. Access the Demo UI

The demo interface will automatically open at:
```
https://<your-repl-name>.<your-username>.repl.co
```

### 3. Explore the API

Interactive API documentation:
```
https://<your-repl-name>.<your-username>.repl.co/docs
```

## 📖 How to Use

### Demo Mode (No Auth Required)

1. Click **"Demo Mode"** tab
2. Click **"Generate Demo Profile"**
3. Get realistic fake data:
   - Email (Gmail-style)
   - Phone (USA/UK/Australia)
   - Password (8 characters)
   - Wallet address
   - Fake TRX/USDT balances

### Authentication

1. Go to **"Auth"** tab
2. **Register:**
   - Enter a PIN (4-6 digits)
   - Optionally add a password
   - Click "Register"
3. **Login:**
   - Enter your PIN
   - Enter password (if set)
   - Click "Login"

### Wallet Management

1. **Login first** (Auth tab)
2. Go to **"Wallets"** tab
3. **Create Wallet:**
   - Enter wallet name
   - Click "Create New Wallet"
   - Address and private key generated automatically
4. **View Wallets:**
   - Click "Refresh Wallets"
   - See all your wallets with addresses

### Check Balances & QR Codes

1. Go to **"Transactions"** tab
2. **Check Balance:**
   - Paste a TRON address
   - Click "Check Balance"
   - View TRX and USDT balances
3. **Generate QR Code:**
   - Paste a TRON address
   - Click "Generate QR Code"
   - Share for receiving funds

## 🔧 API Endpoints

### Authentication
```
POST /auth/register - Register new user
POST /auth/login    - Login with PIN
```

### Wallets
```
POST   /wallets/create       - Create new wallet
POST   /wallets/import       - Import wallet with private key
GET    /wallets              - List all wallets
GET    /wallets/{id}         - Get wallet details
DELETE /wallets/{id}         - Delete wallet
GET    /wallets/{id}/export  - Export private key
```

### Transactions
```
GET  /balance/{address}        - Get TRX and USDT balance
POST /send                     - Send TRX or USDT tokens
GET  /transactions/{address}   - Get transaction history
```

### Utilities
```
GET /qr/{address}      - Generate QR code
GET /demo/generate     - Generate demo profile
```

Full API documentation: [API_SPEC.md](API_SPEC.md)

## 🎨 UI/UX Design

Complete design specifications for mobile app (iOS/Android):

- **Design System:** TRON brand colors, gradients, typography
- **Screens:** 10+ mobile screens (Auth, Home, Wallets, Send, Receive, Settings)
- **Components:** Buttons, cards, inputs, navigation
- **Interactions:** Animations, transitions, haptic feedback

See [UI_DESIGN_SPEC.md](UI_DESIGN_SPEC.md) for complete mobile design guide.

## 📱 Mobile App Integration

### React Native Example

```javascript
// Login
const response = await fetch('https://your-api.repl.co/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ pin: '1234', password: 'optional' })
});
const { access_token } = await response.json();

// Create Wallet
const wallet = await fetch('https://your-api.repl.co/wallets/create', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access_token}`
  },
  body: JSON.stringify({ name: 'My Wallet' })
});

// Check Balance
const balance = await fetch(`https://your-api.repl.co/balance/${address}`);
const data = await balance.json();
console.log(`TRX: ${data.balances.TRX}, USDT: ${data.balances.USDT}`);
```

## 🛠 Tech Stack

**Backend:**
- FastAPI (Python web framework)
- TronPy (TRON blockchain integration)
- JWT (Authentication)
- Faker (Demo data generation)
- QRCode (QR code generation)
- Passlib (Password hashing)

**Frontend:**
- Vanilla JavaScript (Demo UI)
- HTML5/CSS3
- Responsive design

**Recommended Mobile Stack:**
- React Native or Flutter
- TypeScript
- Biometric authentication
- Secure storage (Keychain/Keystore)

## 🔒 Security Notes

⚠️ **Important for Production:**

1. **Change SECRET_KEY** in `.env` file
2. **Use HTTPS** for all API calls
3. **Never expose private keys** in logs or UI
4. **Implement rate limiting**
5. **Use secure storage** for private keys (Keychain/Keystore)
6. **Enable biometric authentication** in mobile app
7. **Switch to mainnet** (currently using Nile testnet)

### Switching to Mainnet

In `main.py`, change:
```python
tron = Tron(network='nile')  # Testnet
```
to:
```python
tron = Tron(network='mainnet')  # Production
```

## 📁 Project Structure

```
TRON-Wallet/
├── main.py                 # FastAPI backend
├── static/
│   └── index.html         # Demo web UI
├── API_SPEC.md            # Complete API documentation
├── UI_DESIGN_SPEC.md      # Mobile UI/UX design guide
├── README.md              # This file
├── .env.example           # Environment variables template
└── pyproject.toml         # Python dependencies
```

## 🌐 Deployment on Replit

This application is already configured for Replit Deployments:

1. **Development:** Running on port 5000 (current workspace)
2. **Production:** Ready for Autoscale or Reserved VM deployment

To deploy:
1. Click the **Deploy** button in Replit
2. Choose deployment type (Autoscale recommended)
3. Configure custom domain (optional)
4. Deploy!

## 📊 Testing the API

### Using curl:

```bash
# Generate demo profile
curl https://your-api.repl.co/demo/generate

# Register user
curl -X POST https://your-api.repl.co/auth/register \
  -H "Content-Type: application/json" \
  -d '{"pin":"1234","password":"mypass"}'

# Check balance
curl https://your-api.repl.co/balance/TJRabPrwbZy45sbavfcjinPJC18kjpRTv8
```

### Using the Swagger UI:

Visit `/docs` for interactive API testing with built-in UI.

## 🎯 Use Cases

- **Personal Crypto Wallet:** Store and manage TRX/USDT
- **Mobile App Backend:** API for iOS/Android apps
- **Demo/Testing:** Generate fake profiles for testing
- **Educational:** Learn TRON blockchain integration
- **Prototype:** Quick prototype for crypto wallet features

## 📝 License

MIT License - Free to use for your projects!

## 🤝 Contributing

This is a complete, production-ready template. Feel free to:
- Fork and customize
- Add new features
- Improve security
- Enhance UI/UX
- Add more token support

## 📞 Support

- **API Docs:** `/docs`
- **Design Guide:** `UI_DESIGN_SPEC.md`
- **API Reference:** `API_SPEC.md`

---

Made with ❤️ using Replit | TRON Blockchain | FastAPI

**Ready to build your mobile TRON wallet!** 🚀
