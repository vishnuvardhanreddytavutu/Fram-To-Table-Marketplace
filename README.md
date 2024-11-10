# FarmFresh Market 🌾

A web-based e-commerce platform connecting farmers directly with consumers, built with Flask, JavaScript, and CSS. This platform empowers farmers to showcase and sell their agricultural products online.

## Features ✨

### For Farmers 👨‍🌾
- **Product Management**
  - Add/edit/delete products
  - Upload product images
  - Set prices and stock levels
  - Mark items as organic/non-organic
  - Seasonal product indicators
  
- **Dashboard**
  - Sales analytics
  - Order management
  - Inventory tracking
  - Revenue reports
  - Customer feedback view

- **Profile Management**
  - Farm details
  - Location information
  - Contact details
  - Farming practices
  - Certifications upload

### For Customers 🛒
- **Shopping Experience**
  - Browse products by category
  - Search functionality
  - Filter by location/price/type
  - Shopping cart
  - Wishlist feature

- **Order Management**
  - Order tracking
  - Order history
  - Digital receipts
  - Delivery status updates

- **User Features**
  - User registration/login
  - Review & rating system
  - Saved addresses
  - Payment method management

## Tech Stack 🛠️

- **Backend**
  - Flask (Python)
  - Flask-Login
  - Flask-Mail

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript
  - jQuery
  - Bootstrap

- **Database**
  - SQLite (Development)
  - PostgreSQL (Production)

- **Payment Integration**
  - Stripe/Razorpay API

## Installation 🚀

1. Clone the repository:
https://github.com/vishnuvardhanreddytavutu/Fram-To-Table-Marketplace.git

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r (requirements as per App.py)
   ```

4. Set up environment variables:
   Create `.env` file:
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   DATABASE_URL=your_database_url
   SECRET_KEY=your_secret_key
   STRIPE_API_KEY=your_stripe_key
   ```

5. Initialize Mongo database:
![db](https://github.com/user-attachments/assets/ab2b288c-dbd6-476d-9958-67d482023d95)
6. Run the application:
   ```bash
   flask run
   ```

## Screenshots 📸

### Farmer Login
![login](https://github.com/user-attachments/assets/1f5f2a73-a428-4146-bd12-da0ec418fc34)


## Security Features 🔒

- Password hashing
- CSRF protection
- DB injection prevention

- v1.0.0
  - Initial release
  - Basic e-commerce functionality
- v1.1.0
  - Added analytics dashboard
  - Improved order tracking
  - Mobile responsiveness
