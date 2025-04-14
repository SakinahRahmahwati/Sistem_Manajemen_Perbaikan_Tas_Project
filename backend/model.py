from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class Bahan(db.Model):
    __tablename__ = 'bahan'
    bahan_id = db.Column(db.Integer, primary_key=True)
    kode_bahan = db.Column(db.String(50), nullable=False)
    nama_bahan = db.Column(db.String(100), nullable=False)
    harga_satuan = db.Column(db.Numeric(10, 2), nullable=False)
    satuan = db.Column(db.String(50), nullable=False)
    stok = db.Column(db.Integer, default=0)
    tanggal_masuk = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JadwalPerbaikan(db.Model):
    __tablename__ = 'jadwal_perbaikan'
    jadwal_id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.Date, nullable=False)
    kapasitas = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='Tersedia')
    keterangan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class KategoriProduk(db.Model):
    __tablename__ = 'kategori_produk'
    kategori_id = db.Column(db.Integer, primary_key=True)
    nama_kategori = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Pelanggan(db.Model):
    __tablename__ = 'pelanggan'
    pelanggan_id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    no_hp = db.Column(db.String(20))
    alamat = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Pemasok(db.Model):
    __tablename__ = 'pemasok'
    pemasok_id = db.Column(db.Integer, primary_key=True)
    nama_pemasok = db.Column(db.String(100), nullable=False)
    kontak = db.Column(db.String(100))
    alamat = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Pengguna(db.Model):
    __tablename__ = 'pengguna'
    pengguna_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('Admin', 'Kepala Toko', 'Staff'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Produk(db.Model):
    __tablename__ = 'produk'
    produk_id = db.Column(db.Integer, primary_key=True)
    nama_produk = db.Column(db.String(100), nullable=False)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori_produk.kategori_id'))
    harga = db.Column(db.Numeric(10, 2))
    deskripsi = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaksi(db.Model):
    __tablename__ = 'transaksi'
    transaksi_id = db.Column(db.Integer, primary_key=True)
    pelanggan_id = db.Column(db.Integer, db.ForeignKey('pelanggan.pelanggan_id'))
    jadwal_id = db.Column(db.Integer, db.ForeignKey('jadwal_perbaikan.jadwal_id'))
    produk_id = db.Column(db.Integer, db.ForeignKey('produk.produk_id'))
    status = db.Column(db.String(50), default='Pending')
    tanggal_masuk = db.Column(db.Date)
    tanggal_selesai = db.Column(db.Date)
    biaya_total = db.Column(db.Numeric(10, 2))
    keterangan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
