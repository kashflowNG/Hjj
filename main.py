
import os
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, List
from faker import Faker
import qrcode
from io import BytesIO
import base64

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
import jwt
from passlib.context import CryptContext
from tronpy import Tron
from tronpy.keys import PrivateKey
from sqlalchemy.orm import Session
from database import get_db, init_db, User, Wallet, DemoProfile as DemoProfileModel

init_db()

app = FastAPI(title="TRON Wallet API", version="1.0.0")
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake = Faker()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
SECRET_KEY = os.getenv("SESSION_SECRET")
if not SECRET_KEY:
    raise ValueError("SESSION_SECRET environment variable must be set for secure JWT token generation")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
TRON_NETWORK = os.getenv("TRON_NETWORK", "nile")

# Pydantic Models
class UserRegister(BaseModel):
    pin: str
    password: Optional[str] = None

class UserLogin(BaseModel):
    pin: str
    password: Optional[str] = None

class WalletCreate(BaseModel):
    name: str = "My Wallet"

class WalletImport(BaseModel):
    name: str
    private_key: str

class TransactionSend(BaseModel):
    from_address: str
    to_address: str
    amount: float
    token_type: str = "TRX"

class DemoProfile(BaseModel):
    phone: str
    email: str
    password: str
    wallet_address: str
    balance_trx: float
    balance_usdt: float

# Helper Functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def generate_demo_profile() -> DemoProfile:
    """Generate realistic demo profile with fake data"""
    countries = ["en_US", "en_GB", "en_AU"]
    fake_locale = Faker(fake.random.choice(countries))
    
    password = ''.join(fake.random.choices(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$', 
        k=8
    ))
    
    username = fake_locale.user_name()
    email = f"{username}@gmail.com"
    phone = fake_locale.phone_number()
    
    tron = Tron(network=TRON_NETWORK)
    account = tron.generate_address()
    
    balance_trx = round(fake.random.uniform(10, 5000), 2)
    balance_usdt = round(fake.random.uniform(100, 10000), 2)
    
    return DemoProfile(
        phone=phone,
        email=email,
        password=password,
        wallet_address=account['base58check_address'],
        balance_trx=balance_trx,
        balance_usdt=balance_usdt
    )

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# API Endpoints

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/api")
async def api_info():
    return {
        "message": "TRON Wallet API",
        "version": "1.0.0",
        "database": "PostgreSQL (Connected)",
        "endpoints": {
            "auth": "/docs#/Auth",
            "wallets": "/docs#/Wallets",
            "transactions": "/docs#/Transactions",
            "demo": "/docs#/Demo"
        }
    }

# Auth Endpoints
@app.post("/auth/register", tags=["Auth"])
async def register(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new user with PIN and optional password"""
    user_id = hashlib.sha256(user.pin.encode()).hexdigest()[:16]
    
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_pin = pwd_context.hash(user.pin)
    hashed_password = pwd_context.hash(user.password) if user.password else None
    
    new_user = User(
        id=user_id,
        pin_hash=hashed_pin,
        password_hash=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    
    access_token = create_access_token(
        data={"sub": user_id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_id
    }

@app.post("/auth/login", tags=["Auth"])
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login with PIN and optional password"""
    user_id = hashlib.sha256(user.pin.encode()).hexdigest()[:16]
    
    stored_user = db.query(User).filter(User.id == user_id).first()
    if not stored_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not pwd_context.verify(user.pin, stored_user.pin_hash):
        raise HTTPException(status_code=401, detail="Invalid PIN")
    
    if user.password and stored_user.password_hash:
        if not pwd_context.verify(user.password, stored_user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid password")
    
    access_token = create_access_token(
        data={"sub": user_id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_id
    }

# Wallet Endpoints
@app.post("/wallets/create", tags=["Wallets"])
async def create_wallet(wallet: WalletCreate, user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Create a new TRON wallet with Gmail, phone, and password"""
    tron = Tron(network=TRON_NETWORK)
    account = tron.generate_address()
    
    # Generate realistic credentials
    countries = ["en_US", "en_GB", "en_AU"]
    fake_locale = Faker(fake.random.choice(countries))
    
    username = fake_locale.user_name()
    gmail = f"{username}@gmail.com"
    phone = fake_locale.phone_number()
    password = ''.join(fake.random.choices(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$', 
        k=8
    ))
    
    wallet_id = secrets.token_hex(8)
    new_wallet = Wallet(
        id=wallet_id,
        user_id=user_id,
        name=wallet.name,
        address=account['base58check_address'],
        private_key=account['private_key'],
        hex_address=account.get('hex_address', '')
    )
    
    db.add(new_wallet)
    db.commit()
    db.refresh(new_wallet)
    
    return {
        "wallet_id": new_wallet.id,
        "name": new_wallet.name,
        "address": new_wallet.address,
        "private_key": new_wallet.private_key,
        "gmail": gmail,
        "phone": phone,
        "password": password,
        "created_at": new_wallet.created_at.isoformat()
    }

@app.post("/wallets/import", tags=["Wallets"])
async def import_wallet(wallet: WalletImport, user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Import an existing wallet using private key"""
    try:
        priv_key = PrivateKey(bytes.fromhex(wallet.private_key))
        address = priv_key.public_key.to_base58check_address()
        
        wallet_id = secrets.token_hex(8)
        new_wallet = Wallet(
            id=wallet_id,
            user_id=user_id,
            name=wallet.name,
            address=address,
            private_key=wallet.private_key
        )
        
        db.add(new_wallet)
        db.commit()
        db.refresh(new_wallet)
        
        return {
            "wallet_id": new_wallet.id,
            "name": new_wallet.name,
            "address": new_wallet.address,
            "created_at": new_wallet.created_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid private key: {str(e)}")

@app.get("/wallets", tags=["Wallets"])
async def list_wallets(user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    """List all wallets for the authenticated user"""
    wallets = db.query(Wallet).filter(Wallet.user_id == user_id).all()
    
    return {
        "wallets": [
            {
                "wallet_id": w.id,
                "name": w.name,
                "address": w.address,
                "is_used": w.is_used if hasattr(w, 'is_used') else False,
                "created_at": w.created_at.isoformat()
            }
            for w in wallets
        ]
    }

@app.get("/wallets/{wallet_id}", tags=["Wallets"])
async def get_wallet(wallet_id: str, user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Get wallet details"""
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    if wallet.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return {
        "wallet_id": wallet.id,
        "name": wallet.name,
        "address": wallet.address,
        "created_at": wallet.created_at.isoformat()
    }

@app.delete("/wallets/{wallet_id}", tags=["Wallets"])
async def delete_wallet(wallet_id: str, user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Delete a wallet"""
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    if wallet.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    db.delete(wallet)
    db.commit()
    
    return {"message": "Wallet deleted successfully"}

@app.get("/wallets/{wallet_id}/export", tags=["Wallets"])
async def export_private_key(wallet_id: str, user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Export private key (use with caution!)"""
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    if wallet.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return {
        "private_key": wallet.private_key,
        "address": wallet.address
    }

@app.patch("/wallets/{wallet_id}/mark-used", tags=["Wallets"])
async def mark_wallet_used(wallet_id: str, used: bool, user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Mark wallet as used or unused"""
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    if wallet.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    wallet.is_used = used
    db.commit()
    
    return {
        "wallet_id": wallet.id,
        "is_used": wallet.is_used,
        "message": f"Wallet marked as {'used' if used else 'unused'}"
    }

# Balance & Transaction Endpoints
@app.get("/balance/{address}", tags=["Transactions"])
async def get_balance(address: str):
    """Get TRX and USDT-TRC20 balance for an address"""
    try:
        tron = Tron(network=TRON_NETWORK)
        
        trx_balance = tron.get_account_balance(address)
        
        usdt_contract = os.getenv("USDT_CONTRACT", "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
        
        try:
            contract = tron.get_contract(usdt_contract)
            usdt_balance = contract.functions.balanceOf(address) / 1_000_000
        except:
            usdt_balance = 0
        
        return {
            "address": address,
            "balances": {
                "TRX": trx_balance,
                "USDT": usdt_balance
            },
            "updated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching balance: {str(e)}")

@app.post("/send", tags=["Transactions"])
async def send_transaction(tx: TransactionSend, user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Send TRX or USDT-TRC20 tokens"""
    try:
        wallet = db.query(Wallet).filter(
            Wallet.address == tx.from_address,
            Wallet.user_id == user_id
        ).first()
        
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found or access denied")
        
        tron = Tron(network=TRON_NETWORK)
        priv_key = PrivateKey(bytes.fromhex(wallet.private_key))
        
        if tx.token_type == "TRX":
            txn = (
                tron.trx.transfer(tx.from_address, tx.to_address, int(tx.amount * 1_000_000))
                .memo("TRON Wallet Transaction")
                .build()
                .sign(priv_key)
            )
            result = txn.broadcast()
            
            return {
                "transaction_id": result.get('txid'),
                "from": tx.from_address,
                "to": tx.to_address,
                "amount": tx.amount,
                "token": "TRX",
                "status": "broadcasted"
            }
        else:
            usdt_contract = os.getenv("USDT_CONTRACT", "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
            contract = tron.get_contract(usdt_contract)
            
            txn = (
                contract.functions.transfer(tx.to_address, int(tx.amount * 1_000_000))
                .with_owner(tx.from_address)
                .fee_limit(100_000_000)
                .build()
                .sign(priv_key)
            )
            result = txn.broadcast()
            
            return {
                "transaction_id": result.get('txid'),
                "from": tx.from_address,
                "to": tx.to_address,
                "amount": tx.amount,
                "token": "USDT-TRC20",
                "status": "broadcasted"
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Transaction failed: {str(e)}")

@app.get("/transactions/{address}", tags=["Transactions"])
async def get_transaction_history(address: str, limit: int = 20):
    """Get transaction history for an address"""
    try:
        tron = Tron(network=TRON_NETWORK)
        transactions = tron.get_account_transactions(address, limit=limit)
        
        return {
            "address": address,
            "transactions": transactions,
            "count": len(transactions)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching transactions: {str(e)}")

# QR Code Generation
@app.get("/qr/{address}", tags=["Utilities"])
async def generate_qr_code(address: str):
    """Generate QR code for receiving address"""
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(address)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            "address": address,
            "qr_code": f"data:image/png;base64,{img_base64}"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating QR code: {str(e)}")

# Demo Mode
@app.get("/demo/generate", tags=["Demo"])
async def generate_demo(db: Session = Depends(get_db)):
    """Generate a realistic demo profile"""
    profile = generate_demo_profile()
    
    demo_id = secrets.token_hex(8)
    demo_record = DemoProfileModel(
        id=demo_id,
        phone=profile.phone,
        email=profile.email,
        password=profile.password,
        wallet_address=profile.wallet_address,
        balance_trx=profile.balance_trx,
        balance_usdt=profile.balance_usdt
    )
    
    db.add(demo_record)
    db.commit()
    
    return profile

@app.get("/demo/profile", tags=["Demo"])
async def get_demo_profile():
    """Get a new demo profile each time"""
    return generate_demo_profile()

# Health check
@app.get("/health", tags=["System"])
async def health_check(db: Session = Depends(get_db)):
    """Check API and database health"""
    try:
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "api": "running"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
