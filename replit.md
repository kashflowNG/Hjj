# TRON Wallet Application

## Overview

This is a full-stack TRON cryptocurrency wallet application with a REST API backend and web-based demo UI. The application enables users to manage TRON (TRX) and USDT-TRC20 wallets, perform transactions, and test functionality through a demo mode with realistic fake profiles. The backend is built with FastAPI (Python) and uses PostgreSQL for data persistence, while the frontend provides an interactive web interface for testing and demonstrations.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

**October 6, 2025 - PostgreSQL Database Integration Completed**
- ✅ Connected to PostgreSQL database using Supabase (DATABASE_URL configured)
- ✅ Implemented secure authentication with SESSION_SECRET for JWT tokens (mandatory, no fallback)
- ✅ Created database schema with `app_users` and `app_wallets` tables (renamed to avoid Supabase conflicts)
- ✅ Replaced in-memory storage with SQLAlchemy ORM for persistent data
- ✅ All endpoints tested and verified working with database
- ✅ Fixed security issues: DemoProfile import, mandatory SESSION_SECRET, proper table naming
- ✅ Server running successfully on port 5000 with auto-reload enabled

## System Architecture

### Backend Architecture

**Framework Choice: FastAPI**
- **Rationale**: FastAPI provides automatic OpenAPI/Swagger documentation, async support, and built-in request validation
- **Pros**: Fast development, automatic API documentation, modern Python async/await support, built-in dependency injection
- **Cons**: Smaller ecosystem compared to Flask/Django

**Authentication & Authorization**
- **Solution**: JWT (JSON Web Tokens) with Bearer authentication
- **Implementation**: PIN-based authentication (4-6 digits) with optional password protection
- **Security Layer**: Passlib bcrypt hashing for credentials, HTTPBearer security scheme
- **Token Management**: Configurable expiration times via `ACCESS_TOKEN_EXPIRE_MINUTES`
- **Rationale**: Stateless authentication suitable for mobile apps and REST APIs

**Data Models**
- **Users**: Store authentication credentials (PIN hash, optional password hash)
- **Wallets**: Multi-wallet support with address, private key, and metadata
- **Demo Profiles**: Fake profiles for testing with phone, email, password, and wallet address
- **Relationships**: One-to-many relationship between Users and Wallets with cascade delete

**API Design Pattern**
- **Style**: RESTful JSON API
- **Documentation**: Auto-generated Swagger/OpenAPI specification
- **CORS**: Fully enabled for cross-origin requests (mobile app integration)
- **Response Format**: Consistent JSON responses with appropriate HTTP status codes

### Database Architecture

**Solution: PostgreSQL with SQLAlchemy ORM**
- **Rationale**: Relational data model fits wallet-user relationships, SQLAlchemy provides database-agnostic abstraction
- **Schema Design**: 
  - Users table (`app_users`) for authentication
  - Wallets table (`app_wallets`) for wallet storage with foreign key to users
  - Demo profiles table (`demo_profiles`) for test data
- **Key Features**: Declarative Base models, relationship mapping, cascade deletes
- **Connection**: Environment-based DATABASE_URL configuration

### Blockchain Integration

**TRON Network Integration**
- **Library**: TronPy for blockchain interactions
- **Network Support**: Configurable mainnet/testnet via `TRON_NETWORK` environment variable
- **Wallet Operations**: 
  - Private key generation and import
  - Address derivation from private keys
  - Transaction signing and broadcasting
- **Token Support**: Native TRX and USDT-TRC20 tokens
- **Key Management**: Encrypted private key storage in database

### Frontend Architecture

**Technology Stack**: Vanilla HTML/CSS/JavaScript
- **Rationale**: Simple demo UI without framework overhead, easy to understand and modify
- **Design System**: TRON-branded color palette (signature red #FF0013), dark theme
- **Components**: Card-based layout with responsive design
- **Styling**: Inline CSS with CSS variables for theming, gradient backgrounds

**Demo Mode Features**
- **Faker.js Integration**: Generate realistic test profiles
- **Profile Generation**: USA/UK/Australia phone numbers, Gmail-style emails, 8-character passwords
- **Test Data**: Fake wallet balances for demonstrations
- **Use Case**: Testing, presentations, and UI development without real blockchain interaction

### Security Considerations

**Credential Protection**
- **Password Hashing**: Bcrypt via Passlib (industry-standard, resistant to rainbow tables)
- **PIN Hashing**: Same bcrypt treatment as passwords
- **Secret Key Management**: Environment variable `SESSION_SECRET` for JWT signing
- **Problem Addressed**: Prevent credential exposure in database breaches

**Private Key Storage**
- **Current Approach**: Encrypted storage in database
- **Risk**: Database compromise exposes private keys
- **Future Enhancement**: Hardware security module (HSM) or client-side encryption

**Token Security**
- **JWT Expiration**: Configurable timeout to limit token lifetime
- **Stateless Design**: No server-side session storage, tokens are self-contained

### Transaction Management

**Transaction Flow**
- **Balance Checking**: Real-time balance queries via TRON network
- **Transaction Creation**: Sign transactions with stored private keys
- **Broadcasting**: Submit signed transactions to TRON network
- **History Tracking**: Query transaction history from blockchain
- **Confirmation**: Monitor transaction status

**QR Code Generation**
- **Library**: qrcode (Python)
- **Use Case**: Generate QR codes for receiving addresses
- **Format**: Base64-encoded PNG images for easy frontend display

## External Dependencies

### Blockchain Services

**TRON Network**
- **Purpose**: Blockchain interaction for wallet operations and transactions
- **Integration**: TronPy library for Python
- **Networks**: Mainnet (production), Nile testnet (development)
- **API Endpoints**: TRON node endpoints for balance queries, transaction broadcasting

### Database

**PostgreSQL**
- **Purpose**: Persistent storage for users, wallets, and demo profiles
- **Connection**: SQLAlchemy ORM with connection string from `DATABASE_URL`
- **Schema Management**: Declarative models with automatic table creation

### Third-Party Python Libraries

**Core Framework**
- **FastAPI**: Web framework for REST API
- **Uvicorn**: ASGI server for running FastAPI

**Blockchain**
- **TronPy**: TRON blockchain integration
- **tronpy.keys.PrivateKey**: Cryptographic key management

**Database**
- **SQLAlchemy**: ORM for database operations
- **psycopg2**: PostgreSQL adapter (implied by PostgreSQL usage)

**Authentication & Security**
- **PyJWT**: JWT token generation and validation
- **Passlib**: Password hashing with bcrypt
- **python-dotenv**: Environment variable management

**Utilities**
- **Faker**: Generate fake test data for demo mode
- **qrcode**: QR code generation for wallet addresses
- **Pillow**: Image processing (dependency of qrcode)

### Frontend Dependencies

**Minimal External Dependencies**
- Static HTML/CSS/JavaScript served via FastAPI StaticFiles
- No build process or package manager required
- Future mobile integration ready (React Native, Flutter)

### Environment Variables

**Required Configuration**
- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_SECRET`: Secret key for JWT signing (critical security requirement)
- `TRON_NETWORK`: Network selection (mainnet/nile)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time (default: 30)

### API Documentation

**Swagger/OpenAPI**
- **Auto-generated**: FastAPI automatically creates interactive API documentation
- **Access**: Available at `/docs` endpoint
- **Format**: OpenAPI 3.0 specification
- **Purpose**: Developer reference and API testing interface