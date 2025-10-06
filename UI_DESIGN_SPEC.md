
# TRON Wallet Mobile App - UI/UX Design Specification

## Design System

### Color Palette (TRON Brand)
```
Primary Red: #FF0013 (TRON signature red)
Primary Gradient: linear-gradient(135deg, #FF0013 0%, #E50914 100%)
Secondary Gradient: linear-gradient(135deg, #2E2E2E 0%, #1A1A1A 100%)

Background Dark: #0D0D0D
Background Card: #1A1A1A
Background Elevated: #2E2E2E

Text Primary: #FFFFFF
Text Secondary: #B3B3B3
Text Muted: #666666

Success Green: #00D66F
Warning Yellow: #FFB800
Error Red: #FF0013
Info Blue: #0099FF

Border Color: #333333
Divider: #2E2E2E
```

### Typography
```
Heading 1: SF Pro Display Bold, 32px
Heading 2: SF Pro Display Semibold, 24px
Heading 3: SF Pro Display Semibold, 20px
Body Large: SF Pro Text Regular, 18px
Body: SF Pro Text Regular, 16px
Body Small: SF Pro Text Regular, 14px
Caption: SF Pro Text Regular, 12px

Letter Spacing: -0.5px for headings, 0px for body
Line Height: 1.5x for body text, 1.2x for headings
```

### Spacing Scale
```
xs: 4px
sm: 8px
md: 16px
lg: 24px
xl: 32px
xxl: 48px
```

### Corner Radius
```
Small: 8px (buttons, input fields)
Medium: 12px (cards, modals)
Large: 16px (bottom sheets)
Full: 999px (pills, badges)
```

### Shadows
```
Card Shadow: 0px 4px 12px rgba(0, 0, 0, 0.3)
Modal Shadow: 0px 8px 24px rgba(0, 0, 0, 0.5)
Button Shadow: 0px 2px 8px rgba(255, 0, 19, 0.4)
```

---

## Screen Specifications

### 1. Splash / Launch Screen
**Layout:**
- Full screen TRON logo (animated)
- Gradient background (#0D0D0D to #1A1A1A)
- Version number at bottom
- Loading indicator

**Interaction:**
- Auto-navigate to Auth or Home after 2 seconds
- Check authentication status

---

### 2. Authentication Screens

#### 2.1 PIN Setup/Login
**Layout:**
- Title: "Enter Your PIN" (Heading 2)
- Subtitle: "4-6 digit PIN for quick access" (Body Small, Text Secondary)
- PIN input dots (large, animated)
- Numeric keypad (3x4 grid)
- "Use Biometric" button (if available)
- "Forgot PIN?" link (Text Secondary)

**Components:**
- PIN Dots: Filled (#FF0013) / Empty (#333333)
- Keypad Buttons: 60px diameter, #2E2E2E background
- Biometric Button: Fingerprint/Face ID icon

**Interaction:**
- Haptic feedback on each key press
- Shake animation on wrong PIN
- Auto-submit on 6 digits

#### 2.2 Biometric Auth
**Layout:**
- Biometric icon (large, centered)
- "Touch to Unlock" or "Look to Unlock" text
- "Use PIN Instead" button

**Interaction:**
- Native biometric prompt
- Fallback to PIN on failure

#### 2.3 Password Setup (Optional)
**Layout:**
- "Add Extra Security" (Heading 2)
- Password input field
- Confirm password field
- Password strength indicator
- "Skip" and "Continue" buttons

---

### 3. Home Screen

**Layout:**
```
┌─────────────────────────────────┐
│  👤 Profile    TRON Wallet    ⚙️  │
├─────────────────────────────────┤
│                                 │
│   Total Balance (USD)           │
│   $8,234.56                     │
│   ↑ +2.45% (24h)                │
│                                 │
│  ┌──────────┐  ┌──────────┐    │
│  │  📤 Send │  │  📥 Receive│   │
│  └──────────┘  └──────────┘    │
│                                 │
│  Assets                    View All│
│  ┌──────────────────────────┐  │
│  │ TRX  1,234.56  $2,345.67 │  │
│  │ [TRON icon]              │  │
│  └──────────────────────────┘  │
│  ┌──────────────────────────┐  │
│  │ USDT 5,678.90  $5,678.90 │  │
│  │ [USDT icon]              │  │
│  └──────────────────────────┘  │
│                                 │
│  Recent Transactions             │
│  ┌──────────────────────────┐  │
│  │ ↑ Sent TRX    -50.00     │  │
│  │ To: TXab...  2h ago      │  │
│  └──────────────────────────┘  │
│                                 │
└─────────────────────────────────┘
 [Home] [Wallets] [Activity] [Settings]
```

**Components:**
- Header: Fixed, gradient background
- Balance Card: Large, gradient, with chart icon
- Quick Action Buttons: Horizontal, equal width
- Asset Cards: List, with icons and amounts
- Transaction Items: List with icons and timestamps

**Interaction:**
- Pull to refresh balances
- Tap asset to view details
- Swipe cards for more options

---

### 4. Wallet Detail Screen

**Layout:**
- Wallet name (editable)
- Address (with copy button)
- QR code (collapsible)
- Balance breakdown (TRX, USDT)
- Send/Receive buttons
- Transaction history
- "Export Private Key" (danger button)
- "Delete Wallet" (danger button)

**Components:**
- Address Display: Monospace font, truncated with "..."
- Copy Button: Icon with success animation
- QR Code: Large, centered, with border
- Balance Cards: Separate for each token

---

### 5. Send Flow

#### 5.1 Send - Recipient Entry
**Layout:**
- "Send TRX/USDT" (Heading 2)
- Token selector (dropdown)
- "To Address" input field
- QR scanner button
- Recent recipients list
- "Continue" button

**Components:**
- Token Selector: Pills with icons
- Address Input: Monospace, with paste button
- Scanner Button: Camera icon, circular

#### 5.2 Send - Amount Entry
**Layout:**
- "How much?" (Heading 2)
- Large amount input
- Token symbol (TRX/USDT)
- USD equivalent (calculated)
- Available balance display
- "Max" button
- Fee estimate
- "Review Transaction" button

**Components:**
- Amount Input: Extra large font (48px)
- Balance Text: "Available: 1,234.56 TRX"
- Fee Card: Small, with info icon

#### 5.3 Send - Confirmation
**Layout:**
- "Review Transaction" (Heading 2)
- Summary card:
  - From: [Your address]
  - To: [Recipient address]
  - Amount: [Amount + Token]
  - Fee: [Fee amount]
  - Total: [Amount + Fee]
- "Slide to Send" slider
- "Cancel" button

**Components:**
- Summary Card: Elevated, with all details
- Slide to Confirm: Custom slider with arrow animation

#### 5.4 Send - Success
**Layout:**
- Success checkmark animation
- "Transaction Sent!" (Heading 2)
- Transaction ID (with copy)
- "View on Explorer" link
- "Done" button

---

### 6. Receive Screen

**Layout:**
- "Receive TRX/USDT" (Heading 2)
- Large QR code
- Wallet address (with copy)
- "Share Address" button
- Optional amount request input
- Token selector

**Components:**
- QR Code: Large (300x300px), centered
- Share Button: System share sheet
- Amount Input: Optional, to generate QR with amount

**Interaction:**
- Generate new QR on token change
- Copy address with haptic feedback
- Share via native share sheet

---

### 7. Create/Import Wallet Screens

#### 7.1 Create New Wallet
**Layout:**
- "Create New Wallet" (Heading 2)
- Wallet name input
- "Generate Wallet" button
- Security notice

**Post-Creation:**
- Success message
- Display address
- "Backup Private Key" (important notice)
- Option to view/export key

#### 7.2 Import Wallet
**Layout:**
- "Import Wallet" (Heading 2)
- Wallet name input
- Private key input (secure, masked)
- "Show/Hide" toggle
- "Import" button
- QR scanner option

**Components:**
- Private Key Input: Monospace, secure text entry
- Warning: Red banner about key security

---

### 8. Wallets Management

**Layout:**
```
┌─────────────────────────────────┐
│  ← Wallets             + Add    │
├─────────────────────────────────┤
│  My Wallets (3)                 │
│                                 │
│  ┌──────────────────────────┐  │
│  │ 💼 Main Wallet           │  │
│  │ TRX: 1,234.56            │  │
│  │ USDT: 5,678.90           │  │
│  │ TJRab...Tv8              │  │
│  └──────────────────────────┘  │
│                                 │
│  ┌──────────────────────────┐  │
│  │ 💰 Trading Wallet        │  │
│  │ TRX: 500.00              │  │
│  │ USDT: 1,200.00           │  │
│  │ TXYZa...w6h              │  │
│  └──────────────────────────┘  │
│                                 │
└─────────────────────────────────┘
```

**Components:**
- Wallet Cards: Swipeable (swipe left to delete)
- Add Button: Floating action button or header button
- Empty State: "Create your first wallet" illustration

**Interaction:**
- Tap card to view details
- Swipe left to reveal delete
- Long press for more options
- Pull down to refresh balances

---

### 9. Demo Mode

#### 9.1 Demo Generator Modal
**Layout:**
- "Demo Profile" (Heading 2)
- "Generate Fake Profile" button
- Display generated data:
  - 📧 Email: [fake email]
  - 📱 Phone: [fake phone]
  - 🔑 Password: [8-char password]
  - 💼 Wallet: [address]
  - 💰 TRX: [amount]
  - 💵 USDT: [amount]
- "Copy All" button
- "Generate New" button
- "Close" button

**Components:**
- Data Cards: Copyable fields with icons
- Generate Button: Primary, with loading state
- Copy Buttons: Individual + "Copy All"

**Interaction:**
- Tap "Generate" to create new profile
- Tap individual copy icons to copy field
- "Copy All" formats as JSON
- Show toast on copy

---

### 10. Settings Screen

**Layout:**
```
┌─────────────────────────────────┐
│  ← Settings                     │
├─────────────────────────────────┤
│  Security                       │
│  › Change PIN                   │
│  › Biometric Login       [ON]   │
│  › Password Protection   [OFF]  │
│                                 │
│  Preferences                    │
│  › Currency (USD)               │
│  › Language (English)           │
│  › Network (Mainnet)            │
│                                 │
│  About                          │
│  › Version 1.0.0                │
│  › Terms of Service             │
│  › Privacy Policy               │
│                                 │
│  🚪 Logout                      │
└─────────────────────────────────┘
```

**Components:**
- List Items: With disclosure indicators
- Toggles: iOS/Android native
- Logout Button: Danger style

---

## Component Library

### Buttons
```
Primary Button:
- Background: Gradient (#FF0013 to #E50914)
- Text: White, Semibold
- Height: 48px
- Radius: 8px
- Shadow: 0px 2px 8px rgba(255, 0, 19, 0.4)

Secondary Button:
- Background: #2E2E2E
- Text: White, Semibold
- Height: 48px
- Radius: 8px

Ghost Button:
- Background: Transparent
- Text: #FF0013, Semibold
- Border: 1px solid #FF0013
```

### Input Fields
```
Text Input:
- Background: #1A1A1A
- Border: 1px solid #333333 (normal), #FF0013 (focus)
- Text: White, 16px
- Height: 48px
- Radius: 8px
- Padding: 12px 16px
```

### Cards
```
Standard Card:
- Background: #1A1A1A
- Radius: 12px
- Padding: 16px
- Shadow: 0px 4px 12px rgba(0, 0, 0, 0.3)

Elevated Card:
- Background: #2E2E2E
- Radius: 12px
- Padding: 16px
- Shadow: 0px 8px 24px rgba(0, 0, 0, 0.5)
```

### Navigation
```
Bottom Tab Bar:
- Height: 56px + safe area
- Background: #1A1A1A with blur
- Active: #FF0013
- Inactive: #666666
- Icons: 24x24px
```

---

## Animations & Transitions

1. **Screen Transitions:** Slide from right (300ms, easeOutCubic)
2. **Modal Presentations:** Slide from bottom (250ms, easeOut)
3. **Button Press:** Scale 0.95 (100ms)
4. **Success States:** Checkmark draw animation (500ms)
5. **Loading States:** Shimmer effect or spinner
6. **Balance Updates:** Number count-up animation (800ms)
7. **Pull to Refresh:** Native platform behavior

---

## Accessibility

1. **Color Contrast:** WCAG AA compliant
2. **Touch Targets:** Minimum 44x44px
3. **Screen Reader:** Full VoiceOver/TalkBack support
4. **Font Scaling:** Support dynamic type
5. **Haptic Feedback:** On all interactions

---

## Platform-Specific Guidelines

### iOS
- Use SF Symbols for icons
- Follow Human Interface Guidelines
- Native navigation patterns
- Face ID/Touch ID integration

### Android
- Use Material Icons
- Follow Material Design 3
- Native navigation patterns
- Fingerprint API integration

---

## Figma File Structure

```
📁 TRON Wallet
├── 🎨 Design System
│   ├── Colors
│   ├── Typography
│   ├── Components
│   └── Icons
├── 📱 Screens
│   ├── Auth Flow
│   ├── Main App
│   ├── Wallet Management
│   └── Settings
├── 🔄 Flows
│   ├── Onboarding
│   ├── Send Transaction
│   └── Create Wallet
└── 📐 Prototypes
    ├── iOS Prototype
    └── Android Prototype
```

---

## Implementation Notes

1. **State Management:** Use React Context or Redux
2. **Secure Storage:** Keychain (iOS), Keystore (Android)
3. **Biometric Auth:** react-native-biometrics
4. **QR Scanner:** react-native-camera
5. **Animations:** react-native-reanimated
6. **Navigation:** react-navigation
7. **Charts:** react-native-svg-charts
