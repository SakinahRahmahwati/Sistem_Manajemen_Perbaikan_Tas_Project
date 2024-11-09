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

if __name__== '__main__':
    app.run(host='127.0.0.1', port=50, debug=True)