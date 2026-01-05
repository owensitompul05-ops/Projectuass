from flask import Flask, render_template, abort, jsonify, session, redirect, url_for
import requests # IMPORT BARU UNTUK AMBIL DATA DARI INTERNET

app = Flask(__name__)
app.secret_key = 'rahasia_kompunesia_123'

# --- FUNGSI AMBIL DATA DARI FAKESTORE API ---
def get_products_from_api():
    try:
        # Menghubungi server FakeStore API
        response = requests.get('https://fakestoreapi.com/products')
        data = response.json()
        return data
    except:
        return []

# KITA PANGGIL DATA SEKALI SAJA SAAT APLIKASI NYALA
# Agar tidak loading terus setiap kali klik halaman
products = get_products_from_api()

# --- UPDATE LOGIKA KERANJANG (Karena API harganya Angka/Dollar) ---
# Kita tidak butuh lagi clean_price yang rumit karena data API sudah bersih (integer/float)

@app.route('/')
def home():
    # Refresh data jika kosong (opsional)
    global products
    if not products:
        products = get_products_from_api()
    return render_template('index.html', products=products)

@app.route('/produk/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product: return abort(404)
    return render_template('detail.html', product=product)

@app.route('/login')
def login():
    return render_template('login.html')

# --- ROUTE API KERANJANG (AJAX) ---
@app.route('/api/add_to_cart/<int:product_id>')
def api_add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'status': 'error', 'message': 'Produk tidak ditemukan'}), 404

    cart = session.get('cart', [])
    
    found = False
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            found = True
            break
    
    if not found:
        # PERUBAHAN DISINI: Menyesuaikan Key API (title & image)
        cart.append({
            'id': product['id'],
            'name': product['title'],     # API pakai 'title' bukan 'name'
            'price': product['price'],    # Harga langsung angka (Dollar)
            'image': product['image'],    # Gambar langsung URL Link
            'quantity': 1
        })
    
    session['cart'] = cart
    return jsonify({
        'status': 'success', 
        'total_items': len(cart),
        'message': f"{product['title']} berhasil ditambahkan!"
    })

# --- ROUTE KERANJANG ---
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/keranjang')
def cart():
    cart = session.get('cart', [])
    
    # Hitung total (Langsung dikali karena data API sudah angka)
    total_amount = sum(item['price'] * item['quantity'] for item in cart)
    
    # Format Dollar ($)
    formatted_total = f"$ {total_amount:,.2f}" 
    
    return render_template('cart.html', cart=cart, total=formatted_total)

# Route Rakitan (Pakai data lokal saja karena FakeStore gak punya rakitan PC)
pc_builds = [
    {"id": 1, "name": "Paket Hemat", "price": "Rp 3.000.000", "components": []}
]

@app.route('/rakitan')
def rakitan():
    return render_template('rakitan.html', builds=pc_builds)

@app.route('/cara-belanja')
def cara_belanja(): return render_template('cara_belanja.html')

@app.route('/konfirmasi-pembayaran')
def konfirmasi_pembayaran(): return render_template('konfirmasi.html')

if __name__ == '__main__':
    app.run(debug=True)