# Kraft Store - Concierge E-Commerce Dashboard

## 1. Project Overview

**Project Name:** Kraft Store
**Type:** Full-stack E-Commerce Dashboard (Concierge Model)
**Core Functionality:** A dark-themed retail dashboard where customers browse curated categories and submit "Order Requests" instead of making payments. The admin fulfills orders manually from third-party suppliers.
**Target Users:** High-end retail customers seeking curated products; Store owner (Admin)

---

## 2. UI/UX Specification

### Layout Structure

**Customer Frontend:**
- **Header:** Logo (KRAFT), Navigation (Home, Categories dropdown), Cart icon with count
- **Hero Section:** Featured banner with tagline
- **Category Grid:** 3-column grid (desktop), 2-column (tablet), 1-column (mobile)
- **Product Grid:** 4-column (desktop), 2-column (tablet), 1-column (mobile)
- **Footer:** Minimal with copyright

**Admin Panel:**
- **Sidebar:** Navigation (Orders, Products)
- **Main Content:** Order table with status actions

### Responsive Breakpoints
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

### Visual Design

**Color Palette:**
- Background Primary: `#0a0a0a` (near black)
- Background Secondary: `#141414` (card backgrounds)
- Background Tertiary: `#1f1f1f` (hover states)
- Accent Primary: `#d4af37` (gold - luxury feel)
- Accent Secondary: `#8b7355` (bronze)
- Text Primary: `#f5f5f5` (off-white)
- Text Secondary: `#a3a3a3` (muted gray)
- Success: `#22c55e` (green)
- Warning: `#f59e0b` (amber)
- Error: `#ef4444` (red)
- Border: `#2a2a2a`

**Typography:**
- Headings: "Playfair Display", serif (elegant, luxury)
- Body: "Inter", sans-serif (clean, readable)
- Font Sizes:
  - H1: 3rem (48px)
  - H2: 2rem (32px)
  - H3: 1.5rem (24px)
  - Body: 1rem (16px)
  - Small: 0.875rem (14px)

**Spacing System:**
- Base unit: 4px
- Margins: 16px, 24px, 32px, 48px
- Paddings: 8px, 16px, 24px

**Visual Effects:**
- Card shadows: `0 4px 20px rgba(0,0,0,0.5)`
- Hover transitions: 300ms ease
- Gold accent glow: `0 0 20px rgba(212,175,55,0.3)`

### Components

**Product Card:**
- Image container (aspect-ratio 1:1)
- Title (truncate after 2 lines)
- Price display (gold color)
- "Order Now" button (gold background)
- Hover: slight scale (1.02) + shadow increase

**Category Card:**
- Large image background
- Overlay with category name
- Hover: overlay lightens

**Order Modal:**
- Centered modal with dark backdrop
- Form fields: Full Name, Phone, Address
- Product summary preview
- Submit button

**Admin Order Row:**
- Order ID, Customer Name, Product, Status
- Action buttons: Buy from Supplier, Update Status
- Status badges with colors

---

## 3. Functionality Specification

### Core Features

**Customer Frontend:**
1. **View Switching:**
   - Home: Hero + Featured Categories
   - Category View: Products in selected category
   - Product Detail: Full product info + Order button

2. **Product Catalog (JSON-based):**
   - id, title, price, description, image, category, supplier_url

3. **Order Request Form:**
   - Fields: fullName, phone, address
   - Bundles: User data + Product data + Supplier URL
   - POST to backend API

4. **Notifications:**
   - Console log (simulated email/WhatsApp)
   - Format: "New Order Request for [Product Name]. User: [Name]. Address: [Address]. Purchase Link: [Supplier URL]"

**Admin Backend:**
1. **Order Management:**
   - List all orders (sorted by date)
   - Filter by status

2. **One-Click Ordering:**
   - "Buy from Supplier" button opens supplier_url in new tab

3. **Status Tracking:**
   - Statuses: Pending, Purchased, Shipped, Delivered
   - Click to change status

### User Interactions

1. Click category → Show products in that category
2. Click product card → Show product detail
3. Click "Order Now" → Open modal form
4. Submit form → Save order + notify admin + show success
5. Admin clicks "Buy from Supplier" → Opens AliExpress/Amazon link
6. Admin clicks status → Cycles through statuses

### Data Handling

**Product Catalog (products.json):**
```json
[
  {
    "id": "1",
    "title": "Premium Wireless Headphones",
    "price": 299.99,
    "description": "High-fidelity audio with noise cancellation",
    "image": "/images/product1.jpg",
    "category": "electronics",
    "supplier_url": "https://aliexpress.com/item/..."
  }
]
```

**Order Schema:**
```json
{
  "id": "order_123",
  "productId": "1",
  "productName": "Premium Wireless Headphones",
  "productPrice": 299.99,
  "supplierUrl": "https://aliexpress.com/item/...",
  "customerName": "John Doe",
  "customerPhone": "+1234567890",
  "customerAddress": "123 Main St, City",
  "status": "pending",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

### Edge Cases
- Empty category: Show "No products available"
- Form validation: All fields required
- Network error: Show error message
- Admin: Empty orders list shows "No orders yet"

---

## 4. Acceptance Criteria

### Visual Checkpoints
- [ ] Dark theme with gold accents applied throughout
- [ ] Product cards display in grid layout
- [ ] Category cards show with image backgrounds
- [ ] Modal appears centered with form
- [ ] Admin panel shows order table

### Functional Checkpoints
- [ ] View switching works (Home → Category → Product)
- [ ] Order form submits and saves order
- [ ] Admin can view all orders
- [ ] "Buy from Supplier" opens correct URL
- [ ] Status can be updated
- [ ] Notification appears in console on order

### Technical Checkpoints
- [ ] Frontend serves on localhost:3000
- [ ] Backend API serves on localhost:5000
- [ ] Products load from JSON
- [ ] Orders persist in database

---

## 5. Technology Stack

- **Frontend:** React 18 + Vite
- **Styling:** Tailwind CSS
- **Backend:** Node.js + Express
- **Database:** SQLite (simple, file-based)
- **Notifications:** Console log (simulated)

