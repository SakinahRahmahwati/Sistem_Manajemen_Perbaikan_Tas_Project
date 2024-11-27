from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask import request
from flask_cors import CORS  # Impor CORS
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

CORS(app)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
mysql = MySQL(app)

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
        data = request.get_json()
        nama_bahan = data.get('nama_bahan')
        harga_satuan = data.get('harga_satuan')
        satuan = data.get('satuan')
        stok = data.get('stok')
        pemasok = data.get('pemasok_id')
        tgl_masuk = data.get('tanggal_masuk')

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT pemasok_id FROM pemasok WHERE pemasok_id = %s", (pemasok,))
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
        sql = "INSERT INTO bahan (nama_bahan, harga_satuan, satuan, stok, pemasok_id, tanggal_masuk) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (nama_bahan, harga_satuan, satuan, stok, pemasok, tgl_masuk))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data added successfully'})

@app.route('/bahan', methods=['GET', 'PUT', 'DELETE'])
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
    
    elif request.method == 'PUT':
        data = request.get_json()
        bahan_id = request.args.get('id', type=int)
        if bahan_id is None:
            return jsonify({'error': 'ID bahan tidak ditemukan'}), 400
        
        nama_bahan = data.get('nama_bahan')
        harga_satuan = data.get('harga_satuan')
        satuan = data.get('satuan')
        stok = data.get('stok')
        pemasok = data.get('pemasok_id')
        tgl_masuk = data.get('tanggal_masuk')

        cursor = mysql.connection.cursor()
        sql = """
            UPDATE bahan 
            SET nama_bahan=%s, harga_satuan=%s, stok=%s, satuan=%s, pemasok_id=%s, tanggal_masuk=%s 
            WHERE bahan_id=%s
        """
        cursor.execute(sql, (nama_bahan, harga_satuan, stok, satuan, pemasok, tgl_masuk, bahan_id))
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
        data = request.get_json()
        nama_layanan = data.get('nama_layanan')
        harga = data.get('harga')
        waktu_estimasi = data.get('waktu_estimasi')
        deskripsi = data.get('deskripsi')
        bahan = data.get('bahan_id')

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT bahan_id FROM bahan WHERE bahan_id = %s", (bahan,))
        bahan_exists = cursor.fetchone()

        if not bahan_exists:
            return jsonify({'error': 'bahan dengan ID tersebut tidak ditemukan'}), 400

        sql = "INSERT INTO layanan (nama_layanan, harga, waktu_estimasi, deskripsi, bahan_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nama_layanan, harga, waktu_estimasi, deskripsi, bahan))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data added successfully'})

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
        data = request.get_json()
        layanan_id = request.args.get('id', type=int)
        if layanan_id is None:
            return jsonify({'error': 'ID layanan tidak ditemukan'}), 400
        
        nama_layanan = data.get('nama_layanan')
        bahan_id = data.get('bahan_id')
        harga = data.get('harga')
        waktu_estimasi = data.get('waktu_estimasi')
        deskripsi = data.get('deskripsi')

        # Melakukan update data layanan
        cursor = mysql.connection.cursor()
        sql = """
            UPDATE layanan 
            SET nama_layanan=%s, bahan_id=%s, harga=%s, waktu_estimasi=%s, deskripsi=%s 
            WHERE layanan_id=%s
        """
        cursor.execute(sql, (nama_layanan, bahan_id, harga, waktu_estimasi, deskripsi, layanan_id))
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
        
        # Menampilkan detail pelanggan berdasarkan ID
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pelanggan WHERE pelanggan_id = %s", (pelanggan_id,))
        column_names = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))
        cursor.close()
        if data:
            return jsonify(data)  # Menampilkan detail pelanggan jika ditemukan
        else:
            return jsonify({'error': 'Pelanggan tidak ditemukan'}), 404

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

if __name__== '__main__':
    app.run(host='127.0.0.1', port=50, debug=True)