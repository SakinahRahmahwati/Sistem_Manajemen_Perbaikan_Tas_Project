from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask import request
from flask_cors import CORS  # Impor CORS

app = Flask(__name__)

CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventory_perbaikantas'
mysql = MySQL(app)

@app.route('/bahan', methods=['GET', 'POST', 'PUT', 'DELETE'])
def bahan():
    if request.method == 'GET':
        # Mengambil semua data bahan
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT bahan.*, pemasok.nama_pemasok
            FROM bahan
            JOIN pemasok ON bahan.pemasok_id = pemasok.pemasok_id
        """)
        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        # Menambahkan data bahan baru
        data = request.get_json()
        nama_bahan = data.get('nama_bahan')
        harga_satuan = data.get('harga_satuan')
        satuan = data.get('satuan')
        stok = data.get('stok')
        pemasok = data.get('pemasok_id')
        tgl_masuk = data.get('tanggal_masuk')

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO bahan (nama_bahan, harga_satuan, satuan, stok, pemasok_id, tanggal_masuk) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (nama_bahan, harga_satuan, satuan, stok, pemasok, tgl_masuk))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data added successfully'})
    
    elif request.method == 'PUT':
        # Memperbarui data bahan
        if 'id' not in request.args:
            return jsonify({'error': 'ID is required for updating data'}), 400

        bahan_id = request.args['id']
        data = request.get_json()
        nama_bahan = data.get('nama_bahan')
        harga_satuan = data.get('harga_satuan')
        satuan = data.get('satuan')
        stok = data.get('stok')
        pemasok = data.get('pemasok_id')
        tgl_masuk = data.get('tanggal_masuk')

        cursor = mysql.connection.cursor()
        sql = "UPDATE bahan SET nama_bahan=%s, harga_satuan=%s, satuan=%s, stok=%s, pemasok_id=%s, tanggal_masuk=%s WHERE bahan_id=%s"
        cursor.execute(sql, (nama_bahan, harga_satuan, satuan, stok, pemasok, tgl_masuk, bahan_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data updated successfully'})
    
    elif request.method == 'DELETE':
        # Menghapus data bahan
        if 'id' not in request.args:
            return jsonify({'error': 'ID is required for deleting data'}), 400

        bahan_id = request.args['id']
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM bahan WHERE bahan_id = %s"
        cursor.execute(sql, (bahan_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data deleted successfully'})

@app.route('/layanan', methods=['GET', 'POST', 'PUT', 'DELETE'])
def layanan():
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
        data = request.get_json()
        nama_layanan = data.get('nama_layanan')
        harga = data.get('harga')
        waktu_estimasi = data.get('waktu_estimasi')
        deskripsi = data.get('deskripsi')
        bahan = data.get('bahan_id')

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO layanan (nama_layanan, harga, waktu_estimasi, deskripsi, bahan_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nama_layanan, harga, waktu_estimasi, deskripsi, bahan))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data added successfully'})
    
    elif request.method == 'PUT':
        if 'id' not in request.args:
            return jsonify({'error': 'ID is required for updating data'}), 400

        layanan_id = request.args['id']
        data = request.get_json()
        nama_layanan = data.get('nama_layanan')
        harga = data.get('harga')
        waktu_estimasi = data.get('waktu_estimasi')
        deskripsi = data.get('deskripsi')
        bahan = data.get('bahan_id')

        cursor = mysql.connection.cursor()
        sql = "UPDATE bahan SET nama_layanan=%s, harga=%s, waktu_estimasi=%s, deskripsi=%s, bahan_id=%s, WHERE layanan_id=%s"
        cursor.execute(sql, (nama_layanan, harga, waktu_estimasi, deskripsi, bahan, layanan_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data updated successfully'})
    
    elif request.method == 'DELETE':
        # Menghapus data bahan
        if 'id' not in request.args:
            return jsonify({'error': 'ID is required for deleting data'}), 400

        layanan_id = request.args['id']
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM layanan WHERE layanan_id = %s"
        cursor.execute(sql, (layanan_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data deleted successfully'})

@app.route('/pelanggan', methods=['GET', 'POST', 'PUT', 'DELETE'])
def pelanggan():
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
        sql = "INSERT INTO pelanggan (nama, alamat, telepon, email, tanggal_registrasi) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nama, alamat, telepon, email, tanggal_registrasi))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data added successfully'})
    
    elif request.method == 'PUT':
        # Memperbarui data bahan
        if 'id' not in request.args:
            return jsonify({'error': 'ID is required for updating data'}), 400

        pelanggan_id = request.args['id']
        data = request.get_json()
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
        return jsonify({'message': 'Data updated successfully'})
    
    elif request.method == 'DELETE':
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

@app.route('/pemasok', methods=['GET', 'POST', 'PUT', 'DELETE'])
def pemasok():
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
        sql = "INSERT INTO pemasok (nama_pemasok, alamat, telepon, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nama_pemasok, alamat, telepon, email))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data added successfully'})
    
    elif request.method == 'PUT':
        # Memperbarui data bahan
        if 'id' not in request.args:
            return jsonify({'error': 'ID is required for updating data'}), 400

        pemasok_id = request.args['id']
        data = request.get_json()
        nama_pemasok = data.get('nama_pemasok')
        alamat = data.get('alamat')
        telepon = data.get('telepon')
        email = data.get('email')

        cursor = mysql.connection.cursor()
        sql = "UPDATE pemasok SET nama_pemasok=%s, alamat=%s, telepon=%s, email=%s=%s WHERE pemasok_id=%s"
        cursor.execute(sql, (nama_pemasok, alamat, telepon, email, pemasok_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data updated successfully'})
    
    elif request.method == 'DELETE':
        # Menghapus dat
        if 'id' not in request.args:
            return jsonify({'error': 'ID is required for deleting data'}), 400

        pemasok_id = request.args['id']
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM pemasok WHERE pemasok_id = %s"
        cursor.execute(sql, (pemasok_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data deleted successfully'})

if __name__== '__main__':
    app.run(host='127.0.0.1', port=50, debug=True)