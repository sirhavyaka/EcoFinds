# EcoFinds - Second Hand E-commerce Platform Setup Guide

## Overview
EcoFinds is a Django-based e-commerce platform for buying and selling second-hand products with Firebase authentication.

## Features
- 🔐 Firebase Authentication (Google OAuth + Email/Password)
- 🛍️ Product catalog with categories and search
- 🛒 Shopping cart functionality
- 📦 Order management system
- 👤 User profiles and seller accounts
- 💬 AI-powered chatbot support
- 📱 Responsive design

## Prerequisites
- Python 3.8+
- pip
- Firebase project (for authentication)

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Firebase Configuration

#### Step 1: Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project named "EcoFinds"
3. Enable Authentication and select Google and Email/Password providers

#### Step 2: Get Firebase Configuration
1. Go to Project Settings > General
2. Scroll down to "Your apps" section
3. Click "Add app" and select Web
4. Copy the Firebase configuration object

#### Step 3: Update Django Settings
1. Replace the Firebase configuration in `templates/base.html`:
```javascript
const firebaseConfig = {
    apiKey: "your-api-key",
    authDomain: "your-project.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "123456789",
    appId: "your-app-id"
};
```

#### Step 4: Firebase Admin SDK (Optional)
1. Go to Project Settings > Service Accounts
2. Click "Generate new private key"
3. Save the JSON file as `firebase_credentials.json` in the project root
4. Update `FIREBASE_CREDENTIALS_PATH` in `settings.py` if needed

### 5. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the application.

## Project Structure

```
EcoFinds/
├── EcoFinds/                 # Main Django project
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── ...
├── firebase_auth/           # Firebase authentication app
├── main/                    # Main app (home, product listing)
├── products/                # Product management
├── cart/                    # Shopping cart
├── orders/                  # Order management
├── user_profile/            # User profiles and addresses
├── chatbot/                 # AI chatbot
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
└── requirements.txt         # Python dependencies
```

## Key URLs

- **Home**: `/`
- **Products**: `/products/`
- **Login**: `/auth/login/`
- **Register**: `/auth/register/`
- **Cart**: `/cart/`
- **Profile**: `/profile/`
- **Admin**: `/admin/`

## API Endpoints

### Authentication
- `POST /auth/api/login/` - Firebase login
- `POST /auth/api/logout/` - Logout
- `GET /auth/api/user/` - Get user info

### Products
- `GET /products/` - List products
- `GET /products/<slug>/` - Product detail
- `POST /products/<id>/review/` - Add review
- `POST /products/<id>/wishlist/` - Toggle wishlist

### Cart
- `GET /cart/` - View cart
- `POST /cart/add/` - Add to cart
- `POST /cart/remove/` - Remove from cart
- `POST /cart/update/` - Update quantity

### Orders
- `GET /orders/` - List orders
- `POST /orders/create/` - Create order
- `GET /orders/<id>/` - Order detail

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
FIREBASE_CREDENTIALS_PATH=firebase_credentials.json
```

## Database Models

### Products
- **Category**: Product categories
- **Product**: Main product model
- **ProductImage**: Product images
- **ProductReview**: User reviews
- **Wishlist**: User wishlist

### Cart & Orders
- **Cart**: User shopping cart
- **CartItem**: Cart items
- **Order**: Order information
- **OrderItem**: Order line items
- **OrderTracking**: Order status tracking

### User Management
- **UserProfile**: Extended user profile
- **Address**: User addresses
- **SellerProfile**: Seller information

## Customization

### Adding New Product Categories
1. Go to Django Admin (`/admin/`)
2. Navigate to Products > Categories
3. Add new categories

### Styling
- Modify `templates/base.html` for global styles
- Update Bootstrap theme in the base template
- Add custom CSS in `static/css/`

### Firebase Authentication
- Modify `firebase_auth/views.py` for custom auth logic
- Update `firebase_auth/authentication.py` for token validation

## Deployment

### Production Settings
1. Set `DEBUG = False`
2. Configure `ALLOWED_HOSTS`
3. Set up proper database (PostgreSQL recommended)
4. Configure static file serving
5. Set up SSL certificates
6. Configure Firebase for production domain

### Environment Variables for Production
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/dbname
```

## Troubleshooting

### Common Issues

1. **Firebase Authentication Not Working**
   - Check Firebase configuration in `base.html`
   - Verify Firebase project settings
   - Check browser console for errors

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_URL` and `STATIC_ROOT` settings

3. **Database Errors**
   - Run `python manage.py makemigrations`
   - Run `python manage.py migrate`

4. **Import Errors**
   - Check if all dependencies are installed
   - Verify Python path and virtual environment

## Support

For issues and questions:
1. Check the Django documentation
2. Review Firebase documentation
3. Check the project's GitHub issues

## License

This project is licensed under the MIT License.
