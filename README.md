# 🛍️ ENNC Shop - E-commerce Platform

A modern, full-stack e-commerce platform built with React, Django, and featuring international shipping, multiple payment methods, and smooth animations.

![ENNC Shop](https://img.shields.io/badge/ENNC-Shop-blue?style=for-the-badge)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat&logo=django)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=flat&logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC?style=flat&logo=tailwind-css)

## ✨ Features

### 🛒 **E-commerce Core**
- **Product Catalog**: 9 categories with featured products
- **Shopping Cart**: Add, remove, update quantities
- **Checkout Flow**: Multi-step checkout with validation
- **Order Management**: Complete order tracking system
- **Inventory**: Stock quantity management

### 🌍 **International Support**
- **200+ Countries**: Comprehensive country support with flags
- **Smart Shipping Zones**: 4 shipping zones with different rates
- **Currency Conversion**: USD to GHS for MoMo payments
- **International Addresses**: Flexible address formats
- **Customs Notices**: International shipping warnings

### 💳 **Payment Methods**
- **Stripe Integration**: International credit/debit cards
- **MTN MoMo**: Mobile money with GHS conversion
- **Real-time Rates**: Live USD to GHS exchange rates
- **Payment Status**: Real-time payment tracking

### 🎨 **User Experience**
- **Smooth Animations**: Framer Motion throughout
- **Responsive Design**: Mobile-first approach
- **Fast Performance**: Optimized loading and caching
- **Accessibility**: WCAG compliant components

### 🔧 **Technical Features**
- **REST API**: Django REST Framework backend
- **Database**: SQLite with Django ORM
- **Caching**: Exchange rate caching
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed logging system

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and npm/pnpm
- **Python** 3.12+ and pip
- **Git**

### 1. Clone Repository
```bash
git clone https://github.com/bassy1992/enontino.git
cd enontino
```

### 2. Backend Setup (Django)
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py populate_shop_data
python manage.py create_superuser
python manage.py runserver 8000
```

### 3. Frontend Setup (React)
```bash
cd frontend
npm install
npm run dev
```

### 4. Access Application
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/ (admin/admin123)

## 📁 Project Structure

```
enontino/
├── frontend/                 # React frontend
│   ├── client/
│   │   ├── components/       # Reusable components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── data/           # Static data & types
│   │   └── context/        # React context
│   ├── public/             # Static assets
│   └── package.json
├── backend/                 # Django backend
│   ├── shop/               # Main app
│   │   ├── models.py       # Database models
│   │   ├── views.py        # API views
│   │   ├── payment_views.py # Payment endpoints
│   │   └── currency_service.py # Currency conversion
│   ├── myproject/          # Django settings
│   └── manage.py
└── docs/                   # Documentation
```

## 🛍️ Shop Features

### **Categories**
- T-Shirts
- Polos  
- Hoodies / Crewnecks
- Sweatshirts
- Tracksuits
- Jackets
- Shorts
- Headwear
- Accessories

### **Products**
- 13+ sample products with realistic data
- High-quality product images
- Detailed descriptions
- Stock quantity tracking
- Featured/new/bestseller tags

### **Shopping Experience**
- Product browsing and filtering
- Category-based navigation
- Search functionality
- Shopping cart management
- Wishlist (coming soon)

## 💳 Payment Integration

### **Stripe (International)**
- Credit/debit card processing
- Secure checkout sessions
- Webhook support
- Multi-currency support

### **MTN MoMo (Ghana)**
- Mobile money integration
- USD to GHS conversion
- Real-time exchange rates
- Phone number validation

### **Currency Conversion**
- Live exchange rates from multiple APIs
- 1-hour caching for performance
- Fallback rates for reliability
- Transparent conversion display

## 🌍 International Features

### **Shipping Zones**
- **🇬🇭 Domestic (Ghana)**: Free over $75, $9.99 standard
- **🌍 West Africa**: Free over $150, $29.99 standard
- **🌍 Africa**: Free over $200, $39.99 standard
- **🌎 International**: Free over $250, $49.99 standard

### **Address Support**
- Flexible international address formats
- Country selection with flags
- State/province support
- Postal code validation

## 🔧 API Endpoints

### **Shop API**
```
GET  /api/shop/products/              # List products
GET  /api/shop/products/featured/     # Featured products
GET  /api/shop/categories/            # List categories
GET  /api/shop/categories/featured/   # Featured categories
GET  /api/shop/search/?q=query        # Search products
```

### **Payment API**
```
POST /api/payments/stripe/create-checkout-session/  # Stripe checkout
POST /api/payments/momo/initiate/                   # MoMo payment
GET  /api/payments/momo/status/{ref}/               # Payment status
GET  /api/payments/exchange-rate/                   # Current USD/GHS rate
POST /api/payments/create-order/                    # Create order
```

## 🧪 Testing

### **Payment Testing**
- Open `frontend/test-payments.html` for payment API testing
- Test phone numbers:
  - `+233XXXXXXX1111` - Success after 5 seconds
  - `+233XXXXXXX2222` - Failure after 3 seconds
  - `+233XXXXXXX0000` - Stays pending

### **Stripe Test Cards**
- `4242 4242 4242 4242` - Visa (success)
- `4000 0000 0000 0002` - Card declined
- `4000 0000 0000 9995` - Insufficient funds

## 🔐 Environment Variables

### **Backend (.env)**
```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Exchange Rate APIs (optional)
FIXER_API_KEY=your-fixer-key
CURRENCY_API_KEY=your-currency-key

# MTN MoMo (production)
MOMO_SUBSCRIPTION_KEY=your-momo-key
MOMO_API_USER=your-api-user
MOMO_API_KEY=your-api-key
```

## 📱 Mobile Support

- **Responsive Design**: Works on all screen sizes
- **Touch Optimized**: Large tap targets
- **Fast Loading**: Optimized for mobile networks
- **Offline Support**: Basic offline functionality

## 🎨 Design System

- **Colors**: Custom brand colors (red/blue gradient)
- **Typography**: Inter font family
- **Components**: Shadcn/ui component library
- **Icons**: Lucide React icons
- **Animations**: Framer Motion

## 🚀 Deployment

### **Frontend (Vercel/Netlify)**
```bash
npm run build
# Deploy dist/ folder
```

### **Backend (Railway/Heroku)**
```bash
pip install -r requirements.txt
python manage.py collectstatic
python manage.py migrate
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Shadcn/ui** for the component library
- **Framer Motion** for smooth animations
- **Tailwind CSS** for styling
- **Django REST Framework** for the API
- **Stripe** for payment processing

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/bassy1992/enontino/issues)
- **Discussions**: [GitHub Discussions](https://github.com/bassy1992/enontino/discussions)
- **Email**: [Contact Support](mailto:support@ennc.com)

---

**Built with ❤️ for the global e-commerce community**

🌟 **Star this repo if you found it helpful!**