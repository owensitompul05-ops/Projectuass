from flask import Flask, render_template, abort, jsonify, session, redirect, url_for

app = Flask(__name__)

# KUNCI RAHASIA (Wajib untuk Session Keranjang)
app.secret_key = 'rahasia_kompunesia_123'

# --- DATA PRODUK ---
products = [
    {"id": 1, "name": "NVIDIA GeForce RTX 4090", "category": "Kartu Grafis", "price": "Rp 28.500.000", "image": "vga4090.png", "description": "Kartu grafis monster untuk gaming 8K.", "specs": ["VRAM 24GB", "CUDA 16384"]},
    {"id": 2, "name": "Intel Core i9-13900K", "category": "Processor", "price": "Rp 9.200.000", "image": "i9.jpeg", "description": "Prosesor tercepat untuk gaming.", "specs": ["24 Cores", "5.8 GHz"]},
    {"id": 3, "name": "Asus ROG Strix Z790-E", "category": "Motherboard", "price": "Rp 7.800.000", "image": "strix.jpg", "description": "Motherboard gaming premium.", "specs": ["LGA1700", "WiFi 6E"]},
    {"id": 4, "name": "Corsair Vengeance 32GB", "category": "RAM", "price": "Rp 2.100.000", "image": "veagence.jpeg", "description": "RAM DDR5 Speed Tinggi.", "specs": ["5600MHz", "2x16GB"]},
    {"id": 5, "name": "Samsung 990 Pro 2TB", "category": "Storage", "price": "Rp 3.500.000", "image": "ssdsamsung2.jpg", "description": "SSD NVMe Tercepat.", "specs": ["Read 7450MB/s", "PCIe 4.0"]},
    {"id": 6, "name": "NZXT H9 Flow Case", "category": "Casing", "price": "Rp 2.400.000", "image": "case.jpg", "description": "Casing Dual Chamber.", "specs": ["ATX Support", "4 Fans"]},
    {"id": 7, "name": "Cooling Fan RGB", "category": "Fan", "price": "Rp 500.000", "image": "fan.jpg", "description": "Fan casing tambahan.", "specs": ["120mm", "RGB"]},
    {"id": 8, "name": "PC Rakitan Sultan", "category": "Computer", "price": "Rp 50.000.000", "image": "pcrakit.jpg", "description": "PC Siap Pakai High End.", "specs": ["RTX 4090", "i9 13900K"]},
    {"id": 9, "name": "SSD Samsung 1TB", "category": "Storage", "price": "Rp 1.000.000", "image": "ssdsamsung.jpg", "description": "SSD SATA III Standard.", "specs": ["1TB", "SATA III"]}
]

# --- DATA RAKITAN ---
pc_builds = [
    {
        "id": 1, "name": "Paket Office & Pelajar", "price": "Rp 4.500.000", "image": "pc_pelajar.jpg", "description": "PC Hemat daya untuk kerja.", 
        "components": [{"part": "CPU", "item": "i3-12100"}, {"part": "RAM", "item": "8GB"}]
    },
    {
        "id": 2, "name": "Paket Gamer Mainstream", "price": "Rp 12.800.000", "image": "pc_gaming.jpg", "description": "PC Gaming 1080p Lancar.", 
        "components": [{"part": "CPU", "item": "i5-12400F"}, {"part": "VGA", "item": "RTX 4060"}]
    },
    {
        "id": 3, "name": "Paket Sultan Creator", "price": "Rp 45.000.000", "image": "pc_dewa.jpeg", "description": "Workstation Monster.", 
        "components": [{"part": "CPU", "item": "i9-14900K"}, {"part": "VGA", "item": "RTX 4080"}]
    }
]

# --- FUNGSI BERSIH HARGA ---
def clean_price(price_str):
    return int(price_str.replace("Rp ", "").replace(".", ""))

# --- ROUTE UTAMA ---
@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/produk/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product: return abort(404)
    return render_template('detail.html', product=product)

@app.route('/login')
def login():
    return render_template('login.html')

# --- ROUTE KERANJANG (CART Logic) ---
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product: return abort(404)

    cart = session.get('cart', [])
    found = False
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            found = True
            break
    if not found:
        cart.append({'id': product['id'], 'name': product['name'], 'price': product['price'], 'image': product['image'], 'quantity': 1})
    
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/keranjang')
def cart():
    cart = session.get('cart', [])
    total_amount = sum(clean_price(item['price']) * item['quantity'] for item in cart)
    formatted_total = f"Rp {total_amount:,.0f}".replace(",", ".")
    return render_template('cart.html', cart=cart, total=formatted_total)

# --- ROUTE RAKITAN ---
@app.route('/rakitan')
def rakitan():
    return render_template('rakitan.html', builds=pc_builds)

@app.route('/rakitan/<int:build_id>')
def rakitan_detail(build_id):
    build = next((b for b in pc_builds if b['id'] == build_id), None)
    if not build: return abort(404)
    return render_template('detail_rakitan.html', build=build)

# --- ROUTE YANG TADI ERROR (INI SOLUSINYA) ---
@app.route('/cara-belanja')
def cara_belanja():
    return render_template('cara_belanja.html')

@app.route('/konfirmasi-pembayaran')
def konfirmasi_pembayaran():
    return render_template('konfirmasi.html')

# --- FAKE API ---
@app.route('/api/products')
def api_products():
    return jsonify({'data': products})

@app.route('/api/rakitan')
def api_rakitan():
    return jsonify({'data': pc_builds})

if __name__ == '__main__':
    app.run(debug=True)