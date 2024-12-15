from flask import Flask, jsonify, send_from_directory
from flask_mysqldb import MySQL
from flask import request
from flask_cors import CORS  # Impor CORS
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
# import bcrypt
import os
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from werkzeug.utils import secure_filename

load_dotenv()
app = Flask(__name__)

CORS(app)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

mysql = MySQL(app)

UPLOAD_FOLDER = r'D:\SAKINAH RAHMAHWATI\Semester 5\Proyek praktek\Proyek_Semester5\backend\uploads\images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def hash_password(password):
#     return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# def verify_password(password, hashed_password):
#     return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Middleware untuk memeriksa peran
# def role_required(allowed_roles):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             # Contoh: Ambil role dari header permintaan (bisa disesuaikan dengan token auth)
#             role = request.headers.get('Role')
#             if role not in allowed_roles:
#                 return jsonify({'error': 'Unauthorized access'}), 403
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator

# Login
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT pengguna_id, password_hash, role FROM pengguna WHERE username = %s", (username,))
        user = cursor.fetchone()
        print("User found:", user)

        if user:
            # Debug: Print hash dan password
            print("Hash from database:", user[1])
            print("Password from input:", password)

            if check_password_hash(user[1], password):
                print("Password match!")  # Debug: Password cocok
                # Generate JWT token
                token = jwt.encode({
                    'user_id': user[0],
                    'role': user[2],
                    'exp': datetime.now(timezone.utc) + timedelta(hours=1)  # Token kadaluarsa dalam 1 jam
                }, app.config['SECRET_KEY'], algorithm='HS256')

                return jsonify({
                    'message': 'Login successful',
                    'token': token,
                    'role': user[2]
                }), 200
            else:
                print("Password does not match.")  # Debug: Password tidak cocok

        return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'error': f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()


@app.route('/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    print(f"Authorization header received: {auth_header}")

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Invalid or missing token'}), 400

    token = auth_header.split(' ')[1]  # Ambil token setelah 'Bearer'
    print(f"Token received: {token}")

    return jsonify({'message': 'Logout successful'}), 200
    
# Reset Password
@app.route('/reset-password', methods=['POST'])
def reset_password():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')

    if not username or not new_password:
        return jsonify({'error': 'Username and new_password are required'}), 400

    # Hash the new password using werkzeug.security
    password_hash = generate_password_hash(new_password)

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE pengguna SET password_hash = %s WHERE username = %s", (password_hash, username))
        mysql.connection.commit()

        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

# Daftar Pengguna
@app.route('/daftarpengguna', methods=['GET','POST'])
def list_pengguna():    
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pengguna")
        column_names = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names,row)))

        cursor.close()
        return jsonify (data)

# Insert Pengguna Baru
@app.route('/kelola_akun', methods=['GET','POST', 'PUT', 'DELETE'])
def kelola_akun():
    if request.method == 'GET':
        pengguna_id = request.args.get('pengguna_id')  # Mengambil ID pengguna dari parameter query string
        if not pengguna_id:
            return jsonify({'error': 'pengguna_id is required'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pengguna WHERE pengguna_id = %s", (pengguna_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'Pengguna tidak ditemukan'}), 404

        column_names = [i[0] for i in cursor.description]
        data = dict(zip(column_names, user))
        cursor.close()
        return jsonify(data)
    elif request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')  # Ambil password mentah (plain text)
        role = data.get('role')
        nama_pengguna = data.get('nama_pengguna')
        no_telp = data.get('no_telp')

        # Validasi input
        if not username or not password or not role:
            return jsonify({'error': 'Username, password, and role are required'}), 400
        if role not in ['Admin', 'Kepala Toko', 'Staff']:
            return jsonify({'error': 'Invalid role'}), 400

        # Periksa apakah username sudah ada
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pengguna WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400

        # Hash password sebelum menyimpan
        hashed_password = generate_password_hash(password)

        cursor.execute("INSERT INTO pengguna (username, password_hash, role, nama_pengguna, no_telp) VALUES (%s, %s, %s, %s, %s)",
                       (username, hashed_password, role, nama_pengguna, no_telp))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Pengguna berhasil ditambahkan'})
    
    elif request.method == 'PUT':
        data = request.get_json()
        pengguna_id = data.get('pengguna_id')
        nama_pengguna = data.get('nama_pengguna')
        no_telp = data.get('no_telp')
        username = data.get('username')
        password_hash = data.get('password_hash')
        role = data.get('role')

        # Validasi input
        if not pengguna_id:
            return jsonify({'error': 'pengguna_id is required'}), 400

        # Periksa apakah pengguna ada sebelum update
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pengguna WHERE pengguna_id = %s", (pengguna_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'Pengguna tidak ditemukan'}), 404

        # Buat query update dinamis
        update_fields = []
        update_values = []

        if username is not None:  # Memeriksa apakah username ada dalam permintaan
            update_fields.append("username = %s")
            update_values.append(username)

        if password_hash is not None:  # Memeriksa apakah password_hash ada dalam permintaan
            update_fields.append("password_hash = %s")
            update_values.append(password_hash)

        if role is not None:  # Memeriksa apakah role ada dalam permintaan
            if role not in ['Admin', 'Kepala Toko', 'Staff']:
                return jsonify({'error': 'Invalid role'}), 400
            update_fields.append("role = %s")
            update_values.append(role)

        # Jika tidak ada field yang ingin diupdate
        if not update_fields:
            return jsonify({'error': 'No fields to update'}), 400

        # Menambahkan pengguna_id ke akhir update_values
        update_values.append(pengguna_id)

        # Menyusun query update
        query = f"UPDATE pengguna SET {', '.join(update_fields)} WHERE pengguna_id = %s"
        cursor.execute(query, update_values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Pengguna berhasil diupdate'})

    elif request.method == 'DELETE':
        pengguna_id = request.args.get('pengguna_id')  # Mengambil ID pengguna dari parameter query string

        # Validasi input
        if not pengguna_id:
            return jsonify({'error': 'pengguna_id is required'}), 400

        # Periksa apakah pengguna ada sebelum delete
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pengguna WHERE pengguna_id = %s", (pengguna_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'Pengguna tidak ditemukan'}), 404

        cursor.execute("DELETE FROM pengguna WHERE pengguna_id = %s", (pengguna_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Pengguna berhasil dihapus'})

@app.route('/dashboard', methods=['GET'])
def dashboard():
    cursor = mysql.connection.cursor()
    
    # Ambil jumlah perbaikan dari tabel 'perbaikan'
    cursor.execute("SELECT COUNT(*) FROM perbaikan WHERE status LIKE '%Selesai%'")
    jumlahPerbaikan = cursor.fetchone()[0]
    
    # Ambil jumlah pelanggan dari tabel 'pelanggan'
    cursor.execute('SELECT COUNT(*) FROM pelanggan')
    jumlahPelanggan = cursor.fetchone()[0]
    
    # Ambil jumlah stok material dari tabel 'bahan'
    # cursor.execute('SELECT SUM(stok) FROM bahan')
    cursor.execute('SELECT COUNT(*) FROM bahan')
    jenisBahan = cursor.fetchone()[0]
    
    # Ambil jumlah perbaikan per bulan berdasarkan 'created_at'
    cursor.execute("""
        SELECT DATE_FORMAT(created_at, '%Y-%m') AS month, COUNT(*) 
        FROM perbaikan
        WHERE status LIKE '%Selesai%'            
        GROUP BY month
        ORDER BY month ASC
    """)
    perbaikan_per_bulan = cursor.fetchall()
    
    # Menyusun data untuk grafik
    labels = [row[0] for row in perbaikan_per_bulan]  # Bulan (format: 2024-11)
    data = [row[1] for row in perbaikan_per_bulan]    # Jumlah perbaikan per bulan
    
    cursor.close()
    
    # Mengembalikan data dalam format JSON
    return jsonify({
        'jumlah Perbaikan': jumlahPerbaikan,
        'jumlah Pelanggan': jumlahPelanggan,
        'jenis Bahan': jenisBahan,
        'chartData': {
            'labels': labels,
            'data': data
        }
    })

@app.route('/daftarbahan', methods=['GET','POST'])
def bahan_list():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT bahan.*, pemasok.nama_pemasok
            FROM bahan
            JOIN pemasok ON bahan.pemasok_id = pemasok.pemasok_id
        """)
        column_names = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names,row)))

        cursor.close()
        return jsonify (data)
    
    elif request.method == 'POST':
        # Mengambil data dari form
        nama_bahan = request.form.get('nama_bahan')
        harga_satuan = request.form.get('harga_satuan')
        satuan = request.form.get('satuan')
        stok = request.form.get('stok')
        pemasok_id = request.form.get('pemasok_id')
        tanggal_masuk = request.form.get('tanggal_masuk')

        # Validasi file gambar
        if 'gambar' not in request.files or not request.files['gambar']:
            return jsonify({'error': 'File gambar harus diunggah'}), 400
        gambar = request.files['gambar']
        if not allowed_file(gambar.filename):
            return jsonify({'error': 'File gambar tidak valid'}), 400
        
        # Buat direktori jika belum ada
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Simpan file gambar
        filename = secure_filename(gambar.filename)
        gambar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        gambar_path = filename

        # Validasi pemasok
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT pemasok_id FROM pemasok WHERE pemasok_id = %s", (pemasok_id,))
        pemasok_exists = cursor.fetchone()

        if not pemasok_exists:
            return jsonify({'error': 'Pemasok dengan ID tersebut tidak ditemukan'}), 400

        # validasi bila ada data yang duplikat
        #     cursor.execute("""
        #     SELECT * FROM bahan 
        #     WHERE nama_bahan = %s AND harga_satuan = %s AND satuan = %s AND stok = %s
        # """, (nama_bahan, harga_satuan, satuan, stok))
        # existing_bahan = cursor.fetchone()
        
        # if existing_bahan:
        #     return jsonify({'error': 'Data dengan semua informasi yang sama sudah ada'}), 400
        sql = """
        INSERT INTO bahan (nama_bahan, harga_satuan, satuan, stok, pemasok_id, tanggal_masuk, gambar)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nama_bahan, harga_satuan, satuan, stok, pemasok_id, tanggal_masuk, gambar_path))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data berhasil ditambahkan'}), 201

@app.route('/uploads/images/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/bahan', methods=['GET', 'POST', 'PUT', 'DELETE'])
def bahan():
    if request.method == 'GET':
        # Mengambil ID dari query string
        bahan_id = request.args.get('id', type=int)  # Mengambil parameter 'id' dari query string
        if bahan_id is None:
            return jsonify({'error': 'ID bahan tidak diberikan'}), 400
        
        # Menampilkan detail bahan berdasarkan ID
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM bahan WHERE bahan_id = %s", (bahan_id,))
        column_names = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))
        cursor.close()
        if data:
            return jsonify(data)  # Menampilkan detail bahan jika ditemukan
        else:
            return jsonify({'error': 'bahan tidak ditemukan'}), 404
    
    elif request.method == 'POST':
        # Menambahkan stok pada bahan yang ada
        data = request.get_json()
        bahan_id = request.args.get('id', type=int)  # ID bahan yang ingin ditambahkan stoknya
        tambahan_stok = data.get('stok')  # Stok yang ingin ditambahkan
        
        if bahan_id is None or tambahan_stok is None or tambahan_stok <= 0:
            return jsonify({'error': 'ID bahan dan jumlah stok yang ditambahkan harus valid'}), 400
        
        # Ambil stok yang ada di database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT stok FROM bahan WHERE bahan_id = %s", (bahan_id,))
        existing_stok = cursor.fetchone()
        if not existing_stok:
            return jsonify({'error': 'Bahan tidak ditemukan'}), 404
        current_stok = existing_stok[0]
        
        # Menambah stok
        new_stok = current_stok + tambahan_stok
        
        # Update stok di database
        cursor.execute("UPDATE bahan SET stok = %s WHERE bahan_id = %s", (new_stok, bahan_id))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Stok berhasil diperbarui', 'new_stok': new_stok})

    elif request.method == 'PUT':
        bahan_id = request.args.get('id', type=int)
        if bahan_id is None:
            return jsonify({'error': 'ID bahan tidak ditemukan'}), 400

        nama_bahan = request.form.get('nama_bahan')
        harga_satuan = request.form.get('harga_satuan')
        satuan = request.form.get('satuan')
        stok = request.form.get('stok')
        pemasok = request.form.get('pemasok_id')
        tgl_masuk = request.form.get('tanggal_masuk')
        gambar = request.files.get('gambar_bahan')

        cursor = mysql.connection.cursor()

        # Ambil gambar lama dari database
        cursor.execute("SELECT gambar FROM bahan WHERE bahan_id = %s", (bahan_id,))
        existing_gambar = cursor.fetchone()
        old_filename = existing_gambar[0] if existing_gambar and existing_gambar[0] else None

        if gambar:
            # Mengamankan nama file
            filename = secure_filename(gambar.filename)

            # Simpan file gambar ke folder yang ditentukan
            gambar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Hapus gambar lama jika ada
            if old_filename:
                old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], old_filename)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Update gambar dengan nama file baru
            sql = """
                UPDATE bahan 
                SET nama_bahan=%s, harga_satuan=%s, stok=%s, satuan=%s, pemasok_id=%s, tanggal_masuk=%s, gambar=%s
                WHERE bahan_id=%s
            """
            cursor.execute(sql, (nama_bahan, harga_satuan, stok, satuan, pemasok, tgl_masuk, filename, bahan_id))
        else:
            # Jika tidak ada gambar baru, gunakan gambar lama
            sql = """
                UPDATE bahan 
                SET nama_bahan=%s, harga_satuan=%s, stok=%s, satuan=%s, pemasok_id=%s, tanggal_masuk=%s, gambar=%s
                WHERE bahan_id=%s
            """
            cursor.execute(sql, (nama_bahan, harga_satuan, stok, satuan, pemasok, tgl_masuk, old_filename, bahan_id))

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data berhasil diperbarui'})


    elif request.method == 'DELETE':
        # Menghapus bahan berdasarkan ID
        bahan_id = request.args.get('id', type=int)  # Mengambil parameter 'id' dari query string
        if bahan_id is None:
            return jsonify({'error': 'ID bahan tidak diberikan'}), 400
        
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM bahan WHERE bahan_id = %s"
        cursor.execute(sql, (bahan_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data deleted successfully'})

@app.route('/daftarlayanan', methods=['GET','POST'])
def layanan_list():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT layanan.*, bahan.nama_bahan
            FROM layanan
            JOIN bahan ON layanan.bahan_id = bahan.bahan_id
        """)
        column_names = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names,row)))

        cursor.close()
        return jsonify (data)
    
    elif request.method == 'POST':
        # Mengambil data dari form
        data = request.form
        nama_layanan = data.get('nama_layanan')
        harga = data.get('harga')
        waktu_estimasi = data.get('waktu_estimasi')
        deskripsi = data.get('deskripsi')
        bahan_id = data.get('bahan_id')

        # Validasi file gambar
        if 'gambar' not in request.files or not request.files['gambar']:
            return jsonify({'error': 'File gambar harus diunggah'}), 400
        gambar = request.files['gambar']
        if not allowed_file(gambar.filename):
            return jsonify({'error': 'File gambar tidak valid'}), 400
        
        # Buat direktori jika belum ada
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Simpan file gambar
        filename = secure_filename(gambar.filename)
        gambar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        gambar_path = filename

        # Validasi bahan
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT bahan_id FROM bahan WHERE bahan_id = %s", (bahan_id,))
        bahan_exists = cursor.fetchone()

        if not bahan_exists:
            return jsonify({'error': 'Bahan dengan ID tersebut tidak ditemukan'}), 400

        sql = """
        INSERT INTO layanan (nama_layanan, harga, waktu_estimasi, deskripsi, bahan_id, gambar)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nama_layanan, harga, waktu_estimasi, deskripsi, bahan_id, gambar_path))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data berhasil ditambahkan'}), 201

@app.route('/layanan', methods=['GET', 'POST', 'PUT', 'DELETE'])
def layanan():
    if request.method == 'GET':
        # Mengambil ID dari query string
        layanan_id = request.args.get('id', type=int)  # Mengambil parameter 'id' dari query string
        if layanan_id is None:
            return jsonify({'error': 'ID layanan tidak ditemukan'}), 400
        
        # Menampilkan detail layanan berdasarkan ID
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM layanan WHERE layanan_id = %s", (layanan_id,))
        column_names = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))
        cursor.close()
        if data:
            return jsonify(data)  # Menampilkan detail layanan jika ditemukan
        else:
            return jsonify({'error': 'layanan tidak ditemukan'}), 404
    
    elif request.method == 'PUT':
        layanan_id = request.args.get('id', type=int)
        if layanan_id is None:
            return jsonify({'error': 'ID layanan tidak ditemukan'}), 400

        # Ambil data dari request
        nama_layanan = request.form.get('nama_layanan')
        bahan_id = request.form.get('bahan_id')
        harga = request.form.get('harga')
        waktu_estimasi = request.form.get('waktu_estimasi')
        deskripsi = request.form.get('deskripsi')
        gambar = request.files.get('gambar_layanan')  # Ambil gambar dari request

        cursor = mysql.connection.cursor()

        # Ambil gambar lama dari database
        cursor.execute("SELECT gambar FROM layanan WHERE layanan_id = %s", (layanan_id,))
        existing_gambar = cursor.fetchone()
        old_filename = existing_gambar[0] if existing_gambar and existing_gambar[0] else None

        if gambar:
            # Mengamankan nama file
            filename = secure_filename(gambar.filename)

            # Simpan file gambar ke folder yang ditentukan
            gambar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Hapus gambar lama jika ada
            if old_filename:
                old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], old_filename)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Update data layanan dengan gambar baru
            sql = """
                UPDATE layanan 
                SET nama_layanan=%s, bahan_id=%s, harga=%s, waktu_estimasi=%s, deskripsi=%s, gambar=%s 
                WHERE layanan_id=%s
            """
            cursor.execute(sql, (nama_layanan, bahan_id, harga, waktu_estimasi, deskripsi, filename, layanan_id))
        else:
            # Jika tidak ada gambar baru, gunakan gambar lama
            sql = """
                UPDATE layanan 
                SET nama_layanan=%s, bahan_id=%s, harga=%s, waktu_estimasi=%s, deskripsi=%s, gambar=%s 
                WHERE layanan_id=%s
            """
            cursor.execute(sql, (nama_layanan, bahan_id, harga, waktu_estimasi, deskripsi, old_filename, layanan_id))

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data layanan berhasil diperbarui'})
    
    elif request.method == 'DELETE':
        # Menghapus data layanan
        layanan_id = request.args.get('id', type=int)  # Mengambil parameter 'id' dari query string
        if layanan_id is None:
            return jsonify({'error': 'ID layanan tidak diberikan'}), 400
        
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM layanan WHERE layanan_id = %s"
        cursor.execute(sql, (layanan_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data deleted successfully'})

@app.route('/daftarpelanggan', methods=['GET','POST'])
def pelanggan_list():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pelanggan")
        column_names = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names,row)))

        cursor.close()
        return jsonify (data)
    
    elif request.method == 'POST':
        data = request.get_json()
        nama = data.get('nama')
        alamat = data.get('alamat')
        telepon = data.get('telepon')
        email = data.get('email')
        tanggal_registrasi = data.get('tanggal_registrasi')

        cursor = mysql.connection.cursor()
        # validasi bila ada data yang duplikat
        #     cursor.execute("""
        #     SELECT * FROM pelanggan 
        #     WHERE nama = %s AND alamat = %s AND telepon = %s AND email = %s
        # """, (nama, alamat, telepon, email))
        # existing_pelanggan = cursor.fetchone()
        
        # if existing_pelanggan:
        #     return jsonify({'error': 'Data dengan semua informasi yang sama sudah ada'}), 400
        sql = "INSERT INTO pelanggan (nama, alamat, telepon, email, tanggal_registrasi) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nama, alamat, telepon, email, tanggal_registrasi))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data added successfully'})
    
    # elif request.method == 'PUT':
    #     # Memperbarui data bahan
    #     if 'id' not in request.args:
    #         return jsonify({'error': 'ID is required for updating data'}), 400

    #     pelanggan_id = request.args['id']
    #     data = request.get_json()
    #     nama = data.get('nama')
    #     alamat = data.get('alamat')
    #     telepon = data.get('telepon')
    #     email = data.get('email')
    #     tanggal_registrasi = data.get('tanggal_registrasi')

    #     cursor = mysql.connection.cursor()
    #     sql = "UPDATE pelanggan SET nama=%s, alamat=%s, telepon=%s, email=%s, tanggal_registrasi=%s WHERE pelanggan_id=%s"
    #     cursor.execute(sql, (nama, alamat, telepon, email, tanggal_registrasi, pelanggan_id))
    #     mysql.connection.commit()
    #     cursor.close()
    #     return jsonify({'message': 'Data berhasil diperbarui'})
    
    # elif request.method == 'DELETE':
        # Menghapus data tanggal_registrasi
        if 'id' not in request.args:
            return jsonify({'error': 'ID is required for deleting data'}), 400

        pelanggan_id = request.args['id']
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM pelanggan WHERE pelanggan_id = %s"
        cursor.execute(sql, (pelanggan_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data deleted successfully'})

@app.route('/pelanggan', methods=['GET', 'PUT', 'DELETE'])
def pelanggan():
    if request.method == 'GET':
        # Mengambil ID dari query string
        pelanggan_id = request.args.get('id', type=int)  # Mengambil parameter 'id' dari query string
        if pelanggan_id is None:
            return jsonify({'error': 'ID pelanggan tidak ditemukan'}), 400
        
        # Mengambil riwayat perbaikan berdasarkan ID pelanggan
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT rp.*, p.nama AS nama_pelanggan 
            FROM riwayat_perbaikan rp
            JOIN pelanggan p ON rp.pelanggan_id = p.pelanggan_id
            WHERE rp.pelanggan_id = %s
        """, (pelanggan_id,))
        
        column_names = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))
        cursor.close()
        
        if data:
            return jsonify(data)  # Menampilkan riwayat perbaikan jika ditemukan
        else:
            return jsonify({'error': 'Riwayat perbaikan tidak ditemukan'}), 404

    elif request.method == 'PUT':
        # Memperbarui data pelanggan berdasarkan ID
        data = request.get_json()
        pelanggan_id = request.args.get('id', type=int)  # Mengambil parameter 'id' dari query string
        if pelanggan_id is None:
            return jsonify({'error': 'ID pelanggan tidak ditemukan'}), 400
        
        nama = data.get('nama')
        alamat = data.get('alamat')
        telepon = data.get('telepon')
        email = data.get('email')
        tanggal_registrasi = data.get('tanggal_registrasi')

        cursor = mysql.connection.cursor()
        sql = "UPDATE pelanggan SET nama=%s, alamat=%s, telepon=%s, email=%s, tanggal_registrasi=%s WHERE pelanggan_id=%s"
        cursor.execute(sql, (nama, alamat, telepon, email, tanggal_registrasi, pelanggan_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data berhasil diperbarui'})

    elif request.method == 'DELETE':
        # Menghapus pelanggan berdasarkan ID
        pelanggan_id = request.args.get('id', type=int)  # Mengambil parameter 'id' dari query string
        if pelanggan_id is None:
            return jsonify({'error': 'ID pelanggan tidak ditemukan'}), 400
        
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM pelanggan WHERE pelanggan_id = %s"
        cursor.execute(sql, (pelanggan_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data deleted successfully'})

@app.route('/daftarpemasok', methods=['GET', 'POST'])
def pemasok_list():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pemasok")
        column_names = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names,row)))

        cursor.close()
        return jsonify (data)
    
    elif request.method == 'POST':
        data = request.get_json()
        nama_pemasok = data.get('nama_pemasok')
        alamat = data.get('alamat')
        telepon = data.get('telepon')
        email = data.get('email')

        cursor = mysql.connection.cursor()
        # validasi bila ada data yang duplikat
        #     cursor.execute("""
        #     SELECT * FROM pemasok 
        #     WHERE nama = %s AND alamat = %s AND telepon = %s AND email = %s
        # """, (nama, alamat, telepon, email))
        # existing_pemasok = cursor.fetchone()
        
        # if existing_pemasok:
        #     return jsonify({'error': 'Data dengan semua informasi yang sama sudah ada'}), 400
        sql = "INSERT INTO pemasok (nama_pemasok, alamat, telepon, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nama_pemasok, alamat, telepon, email))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data added successfully'})

@app.route('/pemasok', methods=['GET', 'PUT', 'DELETE'])
def pemasok():
    if request.method == 'GET':
        # Mengambil ID dari query string
        pemasok_id = request.args.get('id', type=int)  # Mengambil parameter 'id' dari query string
        if pemasok_id is None:
            return jsonify({'error': 'ID pemasok tidak diberikan'}), 400
        
        # Menampilkan detail pemasok berdasarkan ID
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pemasok WHERE pemasok_id = %s", (pemasok_id,))
        column_names = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))
        cursor.close()
        if data:
            return jsonify(data)  # Menampilkan detail pemasok jika ditemukan
        else:
            return jsonify({'error': 'pemasok tidak ditemukan'}), 404

    elif request.method == 'PUT':
        # Memperbarui data pemasok berdasarkan ID
        data = request.get_json()
        pemasok_id = request.args.get('id', type=int)  # Mengambil parameter 'id' dari query string
        if pemasok_id is None:
            return jsonify({'error': 'ID pemasok tidak diberikan'}), 400
        
        nama_pemasok = data.get('nama_pemasok')
        alamat = data.get('alamat')
        telepon = data.get('telepon')
        email = data.get('email')

        cursor = mysql.connection.cursor()
        sql = "UPDATE pemasok SET nama_pemasok=%s, alamat=%s, telepon=%s, email=%s WHERE pemasok_id=%s"
        cursor.execute(sql, (nama_pemasok, alamat, telepon, email, pemasok_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data berhasil diperbarui'})

    elif request.method == 'DELETE':
        # Menghapus pemasok berdasarkan ID
        pemasok_id = request.args.get('id', type=int)  # Mengambil parameter 'id' dari query string
        if pemasok_id is None:
            return jsonify({'error': 'ID pemasok tidak diberikan'}), 400
        
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM pemasok WHERE pemasok_id = %s"
        cursor.execute(sql, (pemasok_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data deleted successfully'})

@app.route('/daftarperbaikan', methods=['GET','POST'])
def perbaikan_list():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT 
                perbaikan.perbaikan_id,
                perbaikan.kode_perbaikan,
                pelanggan.nama AS nama_pelanggan,
                pelanggan.telepon AS notelp,
                layanan.nama_layanan,
                perbaikan.tanggal_masuk,
                perbaikan.tanggal_selesai,
                perbaikan.biaya_perbaikan,
                perbaikan.status,
                perbaikan.status_pembayaran
            FROM perbaikan
            LEFT JOIN pelanggan ON perbaikan.pelanggan_id = pelanggan.pelanggan_id
            LEFT JOIN layanan ON perbaikan.layanan_id = layanan.layanan_id
            GROUP BY perbaikan.perbaikan_id;
        """)
        column_names = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            # Menghitung waktu estimasi (selisih antara tanggal_masuk dan tanggal_selesai)
            tanggal_masuk = row[column_names.index('tanggal_masuk')]
            tanggal_selesai = row[column_names.index('tanggal_selesai')]
        
            if isinstance(tanggal_masuk, str):  # Jika tanggal_masuk adalah string, parsing ke datetime.date
                try:
                    tanggal_masuk = datetime.strptime(tanggal_masuk, '%Y-%m-%d').date()
                except ValueError as e:
                    print(f"Error parsing tanggal_masuk: {e}")  # Menangani kesalahan parsing
                    tanggal_masuk = None

            if isinstance(tanggal_selesai, str):  # Jika tanggal_selesai adalah string, parsing ke datetime.date
                try:
                    tanggal_selesai = datetime.strptime(tanggal_selesai, '%Y-%m-%d').date()
                except ValueError as e:
                    print(f"Error parsing tanggal_selesai: {e}")  # Menangani kesalahan parsing
                    tanggal_selesai = None

            if tanggal_masuk and tanggal_selesai:
                estimasi = (tanggal_selesai - tanggal_masuk).days
            else:
                estimasi = None
        
            # Menambahkan data perbaikan beserta estimasi waktu
            row_dict = dict(zip(column_names, row))
            row_dict['waktu_estimasi'] = estimasi  # Menambahkan estimasi waktu ke dictionary
            data.append(row_dict)

        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        data = request.get_json()
        layanan_ids = data.get('layanan_ids')  # List layanan
        pelanggan_id = data.get('pelanggan_id')
        tanggal_masuk = data.get('tanggal_masuk', datetime.now().date())
        tanggal_selesai = data.get('tanggal_selesai')
        status = data.get('status', 'Dalam Antrian')
        status_pembayaran = data.get('status_pembayaran', 'Belum Bayar')
        total_biaya = 0

        cursor = mysql.connection.cursor()

        # Validasi apakah semua layanan_id ada di tabel layanan dan ambil harga masing-masing
        cursor.execute("""
            SELECT layanan_id, harga 
            FROM layanan 
            WHERE layanan_id IN (%s)
        """ % ','.join(['%s'] * len(layanan_ids)), layanan_ids)
        valid_layanan = cursor.fetchall()
        
        if len(valid_layanan) != len(layanan_ids):
            return jsonify({'error': 'Salah satu atau lebih layanan tidak ditemukan'}), 404

        # Hitung total biaya dan simpan harga layanan untuk digunakan nanti
        harga_layanan_map = {}
        for layanan in valid_layanan:
            layanan_id, harga = layanan
            total_biaya += harga
            harga_layanan_map[layanan_id] = harga

        # Ambil bahan terkait semua layanan yang dipilih
        cursor.execute("""
            SELECT bahan.bahan_id, bahan.stok, layanan.layanan_id 
            FROM layanan
            JOIN bahan ON layanan.bahan_id = bahan.bahan_id
            WHERE layanan.layanan_id IN (%s)
        """ % ','.join(['%s'] * len(layanan_ids)), layanan_ids)
        bahan_list = cursor.fetchall()

        # Periksa stok bahan untuk semua layanan
        for bahan in bahan_list:
            bahan_id, stok, layanan_id = bahan
            if stok < 1:  # Per layanan minimal stok harus ada
                return jsonify({'error': f'Stok bahan untuk layanan {layanan_id} tidak mencukupi'}), 400

        # Kurangi stok bahan sesuai kebutuhan
        for bahan in bahan_list:
            bahan_id, stok, layanan_id = bahan
            cursor.execute("""
                UPDATE bahan SET stok = stok - 1 WHERE bahan_id = %s
            """, (bahan_id,))

        # Simpan data perbaikan ke dalam tabel `perbaikan`
        sql_perbaikan = """
            INSERT INTO perbaikan (kode_perbaikan, pelanggan_id, tanggal_masuk, tanggal_selesai, status, status_pembayaran, biaya_perbaikan)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        now = datetime.now()
    
        date_str = now.strftime('%Y%m%d')
        time_str = now.strftime('%H%M%S')
        kode_perbaikan = f"P{date_str}{time_str}"  # Kode perbaikan berbasis timestamp
        cursor.execute(sql_perbaikan, (
            kode_perbaikan,
            pelanggan_id,
            tanggal_masuk,
            tanggal_selesai,
            status,
            status_pembayaran,
            total_biaya
        ))
        perbaikan_id = cursor.lastrowid

        # Simpan data layanan ke dalam tabel `layanan_perbaikan`
        sql_layanan_perbaikan = """
            INSERT INTO layanan_perbaikan (perbaikan_id, layanan_id, harga)
            VALUES (%s, %s, %s)
        """
        for layanan_id in layanan_ids:
            harga = harga_layanan_map[layanan_id]
            cursor.execute(sql_layanan_perbaikan, (perbaikan_id, layanan_id, harga))

        # Komit semua perubahan
        mysql.connection.commit()
        cursor.close()

        return jsonify({
            'message': 'Perbaikan berhasil ditambahkan',
            'perbaikan_id': perbaikan_id,
            'total_biaya': total_biaya
        })

@app.route('/perbaikan', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def perbaikan():
    if request.method == 'GET':
        perbaikan_id = request.args.get('id')
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT perbaikan.perbaikan_id, 
            perbaikan.kode_perbaikan, 
            pelanggan.nama AS nama_pelanggan, 
            perbaikan.tanggal_masuk, 
            perbaikan.tanggal_selesai, 
            perbaikan.status_pembayaran, 
            perbaikan.biaya_perbaikan, 
            perbaikan.status, layanan.nama_layanan, layanan_perbaikan.harga 
            FROM perbaikan 
            JOIN layanan_perbaikan ON perbaikan.perbaikan_id = layanan_perbaikan.perbaikan_id 
            JOIN layanan ON layanan_perbaikan.layanan_id = layanan.layanan_id 
            JOIN pelanggan ON perbaikan.pelanggan_id = pelanggan.pelanggan_id
            WHERE perbaikan.perbaikan_id = %s
        """, (perbaikan_id,))
        perbaikan = cursor.fetchall()
        if perbaikan:
            # Ambil data perbaikan dari hasil pertama
            perbaikan_data = perbaikan[0]
            return jsonify({
                'perbaikan_id': perbaikan_data[0],
                'kode_perbaikan': perbaikan_data[1],
                'pelanggan_id': perbaikan_data[2],
                'tanggal_masuk': perbaikan_data[3],
                'tanggal_selesai': perbaikan_data[4],
                'status': perbaikan_data[7],
                'status_pembayaran': perbaikan_data[5],
                'biaya_perbaikan': perbaikan_data[6],
                'layanan': [
                    {'nama_layanan': layanan[8], 'harga': layanan[9]}  # Indeks yang benar
                    for layanan in perbaikan    # Menggunakan hasil yang sama
                ]
            })
        else:
            return jsonify({'error': 'Perbaikan tidak ditemukan'}), 404
    
    elif request.method == 'PATCH':
        data = request.get_json()
        perbaikan_id = request.args.get('id', type=int)
        if perbaikan_id is None:
            return jsonify({'error': 'ID layanan tidak ditemukan'}), 400
        
        status = data.get('status')  # Status perbaikan yang baru
        status_pembayaran = data.get('status_pembayaran')  # Status pembayaran yang baru

        if not status and not status_pembayaran:
            return jsonify({'error': 'Perbarui Status perbaikan atau pembayaran'}), 400

        cursor = mysql.connection.cursor()

        if status:
            cursor.execute("""
                UPDATE perbaikan
                SET status = %s
                WHERE perbaikan_id = %s
            """, (status, perbaikan_id))

        if status_pembayaran:
            cursor.execute("""
                UPDATE perbaikan
                SET status_pembayaran = %s
                WHERE perbaikan_id = %s
            """, (status_pembayaran, perbaikan_id))

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data perbaikan berhasil diperbarui'})
    
    # elif request.method == 'PUT':
    #     data = request.get_json()
    #     layanan_ids = data.get('layanan_ids')  # List layanan
    #     pelanggan_id = data.get('pelanggan_id')
    #     tanggal_masuk = data.get('tanggal_masuk', datetime.now().date())
    #     tanggal_selesai = data.get('tanggal_selesai')
    #     status = data.get('status', 'Dalam Antrian')
    #     status_pembayaran = data.get('status_pembayaran', 'Belum Bayar')
    #     total_biaya = 0

    #     cursor = mysql.connection.cursor()

    #     # Validasi apakah semua layanan_id ada di tabel layanan dan ambil harga masing-masing
    #     cursor.execute("""
    #         SELECT layanan_id, harga 
    #         FROM layanan 
    #         WHERE layanan_id IN (%s)
    #     """ % ','.join(['%s'] * len(layanan_ids)), layanan_ids)
    #     valid_layanan = cursor.fetchall()
        
    #     if len(valid_layanan) != len(layanan_ids):
    #         return jsonify({'error': 'Salah satu atau lebih layanan tidak ditemukan'}), 404

    #     # Hitung total biaya dan simpan harga layanan untuk digunakan nanti
    #     harga_layanan_map = {}
    #     for layanan in valid_layanan:
    #         layanan_id, harga = layanan
    #         total_biaya += harga
    #         harga_layanan_map[layanan_id] = harga

    #     # Ambil bahan terkait semua layanan yang dipilih
    #     cursor.execute("""
    #         SELECT bahan.bahan_id, bahan.stok, layanan.layanan_id 
    #         FROM layanan
    #         JOIN bahan ON layanan.bahan_id = bahan.bahan_id
    #         WHERE layanan.layanan_id IN (%s)
    #     """ % ','.join(['%s'] * len(layanan_ids)), layanan_ids)
    #     bahan_list = cursor.fetchall()

    #     # Periksa stok bahan untuk semua layanan
    #     for bahan in bahan_list:
    #         bahan_id, stok, layanan_id = bahan
    #         if stok < 1:  # Per layanan minimal stok harus ada
    #             return jsonify({'error': f'Stok bahan untuk layanan {layanan_id} tidak mencukupi'}), 400

    #     # Kurangi stok bahan sesuai kebutuhan
    #     for bahan in bahan_list:
    #         bahan_id, stok, layanan_id = bahan
    #         cursor.execute("""
    #             UPDATE bahan SET stok = stok - 1 WHERE bahan_id = %s
    #         """, (bahan_id,))

    #     # Update data perbaikan di tabel `perbaikan`
    #     sql_perbaikan = """
    #         UPDATE perbaikan 
    #         SET pelanggan_id = %s, tanggal_masuk = %s, tanggal_selesai = %s, 
    #             status = %s, status_pembayaran = %s, biaya_perbaikan = %s
    #         WHERE id = %s
    #     """
    #     cursor.execute(sql_perbaikan, (
    #         pelanggan_id,
    #         tanggal_masuk,
    #         tanggal_selesai,
    #         status,
    #         status_pembayaran,
    #         total_biaya,
    #         perbaikan_id
    #     ))

    #     # Hapus layanan_perbaikan yang lama
    #     cursor.execute("DELETE FROM layanan_perbaikan WHERE perbaikan_id = %s", (perbaikan_id,))

    #     # Simpan data layanan baru ke dalam tabel `layanan_perbaikan`
    #     sql_layanan_perbaikan = """
    #         INSERT INTO layanan_perbaikan (perbaikan_id, layanan_id, harga)
    #         VALUES (%s, %s, %s)
    #     """
    #     for layanan_id in layanan_ids:
    #         harga = harga_layanan_map[layanan_id]
    #         cursor.execute(sql_layanan_perbaikan, (perbaikan_id, layanan_id, harga))

    #     # Komit semua perubahan
    #     mysql.connection.commit()
    #     cursor.close()

    #     return jsonify({
    #         'message': 'Perbaikan berhasil diperbarui',
    #         'perbaikan_id': perbaikan_id,
    #         'total_biaya': total_biaya
    #     })

    elif request.method == 'DELETE':
        perbaikan_id = request.args.get('id', type=int)
        if perbaikan_id is None:
            return jsonify({'error': 'ID perbaikan tidak diberikan'}), 400
        
        cursor = mysql.connection.cursor()
        cursor.execute("""
            DELETE FROM layanan_perbaikan WHERE perbaikan_id = %s
        """, (perbaikan_id,))

        cursor.execute("""
            DELETE FROM perbaikan WHERE perbaikan_id = %s
        """, (perbaikan_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data deleted successfully'})

@app.route('/pengeluaran', methods=[ 'GET', 'POST'])
def pengeluaran():  
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        sql = """
        SELECT 
            pengeluaran.pengeluaran_id, 
            pengeluaran.tanggal, 
            pengeluaran.total_pengeluaran, 
            pengeluaran.jenis_pengeluaran, 
            pengeluaran.keterangan, 
            pemasok.nama_pemasok, 
            bahan.nama_bahan
        FROM pengeluaran
        LEFT JOIN pemasok ON pengeluaran.pemasok_id = pemasok.pemasok_id
        LEFT JOIN bahan ON pengeluaran.bahan_id = bahan.bahan_id
        ORDER BY pengeluaran.tanggal DESC
        """
        
        cursor.execute(sql)
        result = cursor.fetchall()

        # Format data ke dalam JSON
        laporan = []
        for row in result:
            laporan.append({
                'pengeluaran_id': row[0],
                'tanggal': row[1],
                'total_pengeluaran': float(row[2]),
                'jenis_pengeluaran': row[3],
                'keterangan': row[4],
                'nama_pemasok': row[5] if row[5] else "Tidak Diketahui",
                'nama_bahan': row[6] if row[6] else "Tidak Diketahui",
            })

        cursor.close()

        return jsonify({'message': laporan}), 200

    elif request.method == 'POST':
        data = request.get_json()

        # Mendapatkan data dari request
        pemasok_id = data.get('pemasok_id')
        bahan_id = data.get('bahan_id')
        total_pengeluaran = data.get('total_pengeluaran')
        tanggal = data.get('tanggal')
        keterangan = data.get('keterangan')
        jenis_pengeluaran = data.get('jenis_pengeluaran')

        # Validasi input (misalnya, memastikan tidak ada nilai kosong untuk field penting)
        if not pemasok_id or not total_pengeluaran or not jenis_pengeluaran:
            return jsonify({'error': 'Pemasok ID, Total Pengeluaran, dan Jenis Pengeluaran harus diisi'}), 400

        cursor = mysql.connection.cursor()
        
        # SQL untuk memasukkan data ke tabel pengeluaran
        sql = """
        INSERT INTO pengeluaran (pemasok_id, bahan_id, total_pengeluaran, tanggal, keterangan, jenis_pengeluaran) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (pemasok_id, bahan_id, total_pengeluaran, tanggal, keterangan, jenis_pengeluaran))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Pengeluaran berhasil ditambahkan'})
        
@app.route('/laporanKeuangan', methods=['GET', 'POST'])
def laporanKeuangan_list():
    if request.method == 'GET':
        # Mengambil laporan keuangan dari tabel laporan_keuangan
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM laporan_keuangan ORDER BY tanggal_laporan DESC")
        laporan = cursor.fetchall()

        data = []
        for row in laporan:
            tanggal_laporan = row[1].strftime('%Y-%m-%d') if row[1] else None  # Format tanggal
            data.append({
                "laporan_id": row[0],
                "tanggal_laporan": tanggal_laporan,
                "pendapatan": float(row[2]),
                "pengeluaran": float(row[3])
            })

        # Laporan uang masuk berdasarkan perbaikan dengan status 'Sudah Bayar'
        cursor.execute("""
            SELECT 
                perbaikan.kode_perbaikan,
                perbaikan.biaya_perbaikan,
                perbaikan.tanggal_pembayaran       
            FROM perbaikan
            WHERE perbaikan.status_pembayaran = 'Sudah Bayar'
        """)
        uangMasuk = cursor.fetchall()

        # Laporan uang keluar berdasarkan biaya perbaikan dan status 'Sudah Bayar'
        cursor.execute("""
            SELECT 
                DATE(tanggal_selesai) AS tanggal, 
                SUM(biaya_perbaikan) AS biaya_perbaikan
            FROM perbaikan
            WHERE status_pembayaran = 'Sudah Bayar'
            GROUP BY DATE(tanggal_selesai)
        """)
        uangKeluar = cursor.fetchall()

        # Menyusun laporan uang masuk
        sinkronisasi_laporan = {}
        for row in uangMasuk:
            kode_perbaikan = row[0]
            biaya_perbaikan = row[1]
            tanggal_pembayaran = row[2]
            sinkronisasi_laporan[kode_perbaikan] = {
                "tanggal": tanggal_pembayaran,
                "pendapatan": float(biaya_perbaikan),
                "pengeluaran": 0.0
            }

        # Sinkronisasi hasil akhir laporan
        sinkronisasi_hasil = []
        for kode_perbaikan, nilai in sinkronisasi_laporan.items():
            sinkronisasi_hasil.append({
                "kode_perbaikan": kode_perbaikan,
                "tanggal_laporan": nilai["tanggal"],
                "pendapatan": nilai["pendapatan"],
                "pengeluaran": nilai["pengeluaran"],
            })

        # Update pengeluaran
        for row in uangKeluar:
            tanggal = row[0]
            total_pengeluaran = row[1]
            # Menyinkronkan laporan uang keluar dengan tanggal yang sesuai
            for laporan in sinkronisasi_hasil:
                if laporan['tanggal_laporan'] == tanggal:
                    laporan['pengeluaran'] = total_pengeluaran

         # Simpan laporan ke database (tabel laporan_keuangan)
        for laporan in sinkronisasi_hasil:
            # Memastikan kode_perbaikan belum ada di tabel laporan_keuangan
            cursor.execute("SELECT 1 FROM laporan_keuangan WHERE kode_perbaikan = %s", (laporan['kode_perbaikan'],))
            
            # Jika kode_perbaikan tidak ditemukan, lakukan insert
            if not cursor.fetchone():  # Kode perbaikan belum ada, baru insert
                cursor.execute("""
                    INSERT INTO laporan_keuangan (kode_perbaikan, tanggal_laporan, pendapatan, pengeluaran, deskripsi, keuntungan)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    laporan['kode_perbaikan'],
                    laporan['tanggal_laporan'],
                    laporan['pendapatan'],
                    laporan['pengeluaran'],
                    f"Laporan untuk {laporan['kode_perbaikan']}",
                    laporan['pendapatan'] - laporan['pengeluaran']  # Keuntungan
                ))
        
        mysql.connection.commit()            
        cursor.close()
        return jsonify({
            # "laporan_keuangan": data,
            "Laporan Keuangan": sinkronisasi_hasil
        }), 200

    elif request.method == 'POST':
        # Update status pembayaran dan otomatis menambahkan laporan keuangan
        data = request.get_json()
        kode_perbaikan = data.get('kode_perbaikan')
        status_pembayaran = data.get('status_pembayaran')

        if not kode_perbaikan or not status_pembayaran:
            return jsonify({"error": "kode_perbaikan dan status_pembayaran diperlukan"}), 400

        try:
            cursor = mysql.connection.cursor()

            # Perbarui status pembayaran di tabel perbaikan
            cursor.execute("""
                UPDATE perbaikan
                SET status_pembayaran = %s
                WHERE kode_perbaikan = %s
            """, (status_pembayaran, kode_perbaikan))

            # Memastikan perubahan berhasil
            if cursor.rowcount == 0:
                return jsonify({"error": "Data perbaikan tidak ditemukan"}), 404
            
            if status_pembayaran == 'Belum Bayar':
                cursor.execute("""
                    DELETE FROM laporan_keuangan 
                    WHERE deskripsi LIKE %s
                """, (f"%{kode_perbaikan}%",))  # Menghapus laporan yang terkait dengan kode_perbaikan
                mysql.connection.commit()

            elif status_pembayaran == 'Sudah Bayar':
                # Ambil biaya perbaikan dan kode_perbaikan dari tabel perbaikan
                cursor.execute("""
                    SELECT biaya_perbaikan FROM perbaikan WHERE kode_perbaikan = %s
                """, (kode_perbaikan,))
                result = cursor.fetchone()

                if result:
                    biaya_perbaikan = result[0]

                    # Menambahkan data ke laporan_keuangan
                    cursor.execute("""
                        INSERT INTO laporan_keuangan (tanggal_laporan, pendapatan, pengeluaran)
                        VALUES (NOW(), %s, 0)
                    """, (biaya_perbaikan,))

                    # Commit perubahan
                    mysql.connection.commit()

            cursor.close()
            return jsonify({"message": "Status pembayaran berhasil diperbarui dan laporan keuangan otomatis dicatat"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


if __name__== '__main__':
    app.run(host='127.0.0.1', port=50, debug=True)