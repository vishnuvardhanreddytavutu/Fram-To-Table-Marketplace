from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from datetime import datetime
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong, secure secret key
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# MongoDB setup
app.config['MONGO_URI'] = "mongodb://localhost:27017/ecommerce_db"  # MongoDB connection
mongo = PyMongo(app)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Store the user in MongoDB
        mongo.db.users.insert_one({
            'username': username,
            'password': password,  # For security, consider hashing passwords
            'role': role
        })

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = mongo.db.users.find_one({'username': username})

        if user and user['password'] == password:
            session['username'] = user['username']
            session['role'] = user['role']

            flash('Login successful!')

            # Redirect based on role
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')

# Admin Dashboard Route
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'role' in session and session['role'] == 'admin':
        products = mongo.db.products.find()
        feedbacks = mongo.db.feedbacks.find()  # Fetch all feedbacks
        return render_template('admin_dashboard.html', products=products, feedbacks=feedbacks)
    else:
        flash('Unauthorized access.')
        return redirect(url_for('login'))

# Add Product Route (Admin Only)
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'role' in session and session['role'] == 'admin':
        if request.method == 'POST':
            category = request.form['category']
            product_name = request.form['product_name']
            quantity = request.form['quantity']
            quality = request.form['quality']
            price = request.form['price']

            # Handle image upload
            image_url = None
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_url = url_for('static', filename='uploads/' + filename)

            # Insert product into the database
            mongo.db.products.insert_one({
                'category': category,
                'product_name': product_name,
                'quantity': quantity,
                'quality': quality,
                'price': price,
                'image_url': image_url
            })

            flash('Product added successfully!')
            return redirect(url_for('admin_dashboard'))
        return render_template('add_product.html')
    else:
        flash('Unauthorized access.')
        return redirect(url_for('login'))

# Edit Product Route (Admin Only)
@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'role' in session and session['role'] == 'admin':
        product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
        if request.method == 'POST':
            # Handle image upload
            image_url = product['image_url']
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_url = url_for('static', filename='uploads/' + filename)

            # Update the product
            mongo.db.products.update_one({'_id': ObjectId(product_id)}, {
                "$set": {
                    'product_name': request.form['product_name'],
                    'quantity': request.form['quantity'],
                    'quality': request.form['quality'],
                    'price': request.form['price'],
                    'image_url': image_url
                }
            })
            flash('Product updated successfully.')
            return redirect(url_for('admin_dashboard'))
        return render_template('edit_product.html', product=product)
    else:
        flash('Unauthorized access.')
        return redirect(url_for('login'))

# Delete Product Route (Admin Only)
@app.route('/delete_product/<product_id>', methods=['POST'])
def delete_product(product_id):
    if 'role' in session and session['role'] == 'admin':
        mongo.db.products.delete_one({"_id": ObjectId(product_id)})
        flash('Product deleted successfully.')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Unauthorized access.')
        return redirect(url_for('login'))

# Delete Feedback Route (Admin Only)
@app.route('/delete_feedback/<feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    if 'role' in session and session['role'] == 'admin':
        mongo.db.feedbacks.delete_one({"_id": ObjectId(feedback_id)})
        flash('Feedback deleted successfully.')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Unauthorized access.')
        return redirect(url_for('login'))

# User Dashboard Route
@app.route('/user_dashboard')
def user_dashboard():
    if 'role' in session and session['role'] == 'user':
        products = mongo.db.products.find()
        return render_template('user_dashboard.html', products=products)
    else:
        flash('Unauthorized access.')
        return redirect(url_for('login'))

# View Product (User Only)
@app.route('/product/<product_id>')
def view_product(product_id):
    if 'role' in session and session['role'] == 'user':
        product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
        return render_template('view_product.html', product=product)
    else:
        flash('Unauthorized access.')
        return redirect(url_for('login'))

@app.route('/order/<product_id>', methods=['GET', 'POST'])
def order_product(product_id):
    if request.method == 'POST':
        # Fetch form data
        name = request.form['name']
        contact = request.form['contact']
        address = request.form['address']
        quantity = int(request.form['quantity'])
        quality = request.form['quality']
        price_per_item = float(request.form['price'])
        payment_utr = request.form['payment_UTR']

        # Calculate total price
        total_price = price_per_item * quantity

        # Fetch the product data
        product = mongo.db.products.find_one({"_id": ObjectId(product_id)})

        if product:
            # Create order dictionary to insert in MongoDB
            order = {
                "product_id": product_id,
                "product_name": product['product_name'],
                "name": name,
                "contact": contact,
                "address": address,
                "quantity": quantity,
                "quality": quality,
                "price_per_item": price_per_item,
                "total_price": total_price,
                "utr_number": payment_utr,
                "date_ordered": datetime.now(),
                "status": "Pending"
            }

            # Insert order into MongoDB
            mongo.db.orders.insert_one(order)

            # Redirect to dashboard.html after successful order
            flash("Order placed successfully!", "success")
            return redirect(url_for('user_dashboard'))

    # If it's a GET request, render the product page
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    if product:
        return render_template('view_product.html', product=product)
    else:
        flash("Product not found!", "danger")
        return redirect(url_for('home'))


# Submit Feedback (User)
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        product_id = request.form['product_id']
        feedback_text = request.form['feedback']
        rating = request.form['rating']
        name = request.form['name']
        contact = request.form['contact']
        address = request.form['address']

        # Save feedback to the database
        mongo.db.feedbacks.insert_one({
            'product_id': product_id,
            'feedback': feedback_text,
            'rating': rating,
            'name': name,
            'contact': contact,
            'address': address
        })

        flash('Feedback submitted successfully.')
        return redirect(url_for('user_dashboard'))  # Redirect after successful submission
    else:
        # For GET requests, provide product list to the feedback form
        products = mongo.db.products.find()
        return render_template('feedback.html', products=products)

# Contact Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Save contact message to the database
        mongo.db.contact_messages.insert_one({
            'name': name,
            'email': email,
            'message': message
        })

        flash('Message sent successfully.')
        return redirect(url_for('home'))
    
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash('Logout successfully.')
    return redirect(url_for('home'))

@app.route('/logoutt', methods=['POST'])
def logoutt():
    # Clear the session
    session.clear()
    # Redirect to home or login page after logout
    flash('Logout successfully.')
    return redirect(url_for('home'))



@app.route('/admin/orders')
def orders():
    
        orders = mongo.db.orders.find()
        return render_template('orders.html', orders=orders)
    
@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    order_id = request.form['order_id']
    new_status = request.form['status']

    # Validate status
    if new_status not in ['Pending', 'Completed', 'Declined']:
        flash("Invalid status!", "danger")
        return redirect(url_for('orders'))

    # Update the order status in the database
    result = mongo.db.orders.update_one(
        {'_id': ObjectId(order_id)},
        {'$set': {'status': new_status}}
    )

    if result.modified_count > 0:
        flash("Order status updated successfully!", "success")
    else:
        flash("Failed to update order status!", "danger")

    return redirect(url_for('orders'))

if __name__ == '__main__':
 app.run(debug=True)