import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates")
app.secret_key = "yoursecretkey"
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}

# Configure MySQL database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/shaheen_atier'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# Configure SQLite database (changed from MySQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shaheen_atier.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for items
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def init_db():
    with app.app_context():
        db.create_all()
        if not Item.query.first():
            initial_items = [
                Item(title="Item 1", price="₹100", image="images/img6.jpg", section="Popular Items", description="A classic black Abaya with intricate embroidery, perfect for everyday elegance."),
                Item(title="Item 2", price="₹150", image="images/img7.jpg", section="Popular Items", description="Lightweight beige Abaya with modern minimalist design."),
                Item(title="Item 3", price="₹200", image="images/img8.jpg", section="Popular Items", description="Luxurious silk Abaya for special occasions."),
                Item(title="Item 4", price="₹250", image="images/img1.jpg", section="Popular Items", description="Casual navy Abaya with subtle patterns."),
                Item(title="Item 5", price="₹300", image="images/img5.jpg", section="Popular Items", description="Breathable cotton Abaya for daily comfort."),
                Item(title="Item 6", price="₹350", image="images/img3.jpeg", section="Popular Items", description="Elegant grey Abaya with floral accents."),
                Item(title="New Item 1", price="₹400", image="images/img5.jpg", section="New Arrivals", description="Trendy white Abaya with modern cut."),
                Item(title="New Item 2", price="₹450", image="images/img6.jpg", section="New Arrivals", description="Bold red Abaya with contemporary styling."),
                Item(title="New Item 3", price="₹500", image="images/img2.jpg", section="New Arrivals", description="Chic black Abaya with gold detailing."),
                Item(title="New Item 4", price="₹550", image="images/img7.jpg", section="New Arrivals", description="Soft pastel Abaya for a fresh look."),
                Item(title="New Item 5", price="₹600", image="images/img8.jpg", section="New Arrivals", description="Elegant green Abaya with embroidery."),
                Item(title="New Item 6", price="₹650", image="images/img3.jpeg", section="New Arrivals", description="Stylish blue Abaya with modern flair."),
                Item(title="Deal 1", price="₹700", image="images/img5.jpg", section="Best Deals", description="Discounted luxury Abaya with intricate patterns."),
                Item(title="Deal 2", price="₹750", image="images/img6.jpg", section="Best Deals", description="Affordable yet elegant Abaya for all occasions."),
                Item(title="Deal 3", price="₹800", image="images/img1.jpg", section="Best Deals", description="Premium Abaya at a special price."),
                Item(title="Deal 4", price="₹850", image="images/img7.jpg", section="Best Deals", description="Comfortable and stylish Abaya on sale."),
                Item(title="Deal 5", price="₹900", image="images/img8.jpg", section="Best Deals", description="High-quality Abaya with discounted price."),
                Item(title="Deal 6", price="₹950", image="images/img5.jpg", section="Best Deals", description="Exclusive deal on a premium Abaya design."),
            ]
            db.session.bulk_save_objects(initial_items)
            db.session.commit()

@app.route('/')
def home():
    sections = [
        {"title": "Popular Items", "cards": Item.query.filter_by(section="Popular Items").all()},
        {"title": "New Arrivals", "cards": Item.query.filter_by(section="New Arrivals").all()},
        {"title": "Best Deals", "cards": Item.query.filter_by(section="Best Deals").all()}
    ]
    return render_template('home.html', sections=sections)

@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        flash('Thank you for your message! We’ll get back to you soon.', 'success')
    return render_template('about.html')

@app.route('/collection')
def collection():
    return render_template('collection.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    if name and email and message:
        flash('Thank you for your message! We’ll get back to you soon.', 'success')
    else:
        flash('Please fill all fields.', 'error')
    return redirect(url_for('contact'))

@app.route('/signIn')
def signIn():
    return render_template('signIn.html')  # Placeholder; create signIn.html or remove route if not needed

@app.route('/product/<title>')
def product(title):
    item = Item.query.filter_by(title=title).first()
    if item:
        similar_items = Item.query.filter_by(section=item.section).filter(Item.id != item.id).limit(4).all()
        return render_template('product.html', item=item, similar_items=similar_items)
    return "Item not found", 404

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        section = request.form.get('section')
        description = request.form.get('description')
        file = request.files.get('image')
        if title and price and section and description and file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_item = Item(title=title, price=price, image=f'images/{filename}', section=section, description=description)
            db.session.add(new_item)
            db.session.commit()
            flash('Item added successfully!', 'success')
            return redirect(url_for('add_item'))
        else:
            flash('Please fill all fields and upload a valid image.', 'error')
    return render_template('add_item.html')

    init_db()
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)