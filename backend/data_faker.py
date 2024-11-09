from faker import Faker
import random
from datetime import datetime

fake = Faker()

# Number of records to generate
NUM_RECORDS = 10

# Generating fake data for 'bahan' table
def generate_bahan_data():
    data = []
    for _ in range(NUM_RECORDS):
        data.append({
            'bahan_id': fake.uuid4(),
            'pemasok_id': fake.uuid4(),
            'nama_bahan': fake.word(),
            'harga_satuan': random.randint(1000, 100000),
            'satuan': fake.random_element(elements=['kg', 'liter', 'pcs', 'meter']),
            'stok': random.randint(1, 1000),
            'tanggal_masuk': fake.date(),
            'created_at': fake.date_time(),
            'updated_at': fake.date_time()
        })
    return data

# Generating fake data for 'pemasok' table
def generate_pemasok_data():
    data = []
    for _ in range(NUM_RECORDS):
        data.append({
            'pemasok_id': fake.uuid4(),
            'bahan_id': fake.uuid4(),
            'nama_pemasok': fake.company(),
            'alamat': fake.address(),
            'telepon': fake.phone_number(),
            'email': fake.email(),
            'created_at': fake.date_time(),
            'updated_at': fake.date_time()
        })
    return data

# Generating fake data for 'layanan' table
def generate_layanan_data():
    data = []
    for _ in range(NUM_RECORDS):
        data.append({
            'layanan_id': fake.uuid4(),
            'bahan_id': fake.uuid4(),
            'nama_layanan': fake.catch_phrase(),
            'deskripsi': fake.text(),
            'harga': random.randint(10000, 1000000),
            'waktu_estimasi': random.randint(1, 72),  # in hours
            'created_at': fake.date_time(),
            'updated_at': fake.date_time()
        })
    return data

# Generating fake data for 'pelanggan' table
def generate_pelanggan_data():
    data = []
    for _ in range(NUM_RECORDS):
        data.append({
            'pelanggan_id': fake.uuid4(),
            'nama': fake.name(),
            'alamat': fake.address(),
            'telepon': fake.phone_number(),
            'email': fake.email(),
            'tanggal_registrasi': fake.date(),
            'created_at': fake.date_time(),
            'updated_at': fake.date_time()
        })
    return data

# Generating fake data for 'perbaikan' table
def generate_perbaikan_data():
    data = []
    for _ in range(NUM_RECORDS):
        data.append({
            'perbaikan_id': fake.uuid4(),
            'pelanggan_id': fake.uuid4(),
            'layanan_id': fake.uuid4(),
            'status': fake.random_element(elements=['pending', 'in progress', 'completed']),
            'tanggal_masuk': fake.date(),
            'tanggal_selesai': fake.date_between(start_date='-30d', end_date='today'),
            'biaya_perbaikan': random.randint(50000, 5000000),
            'status_pembayaran': fake.random_element(elements=['paid', 'unpaid']),
            'created_at': fake.date_time(),
            'updated_at': fake.date_time()
        })
    return data

# Generating fake data for 'pengeluaran' table
def generate_pengeluaran_data():
    data = []
    for _ in range(NUM_RECORDS):
        data.append({
            'pengeluaran_id': fake.uuid4(),
            'pemasok_id': fake.uuid4(),
            'nama_bahan': fake.word(),
            'total_pengeluaran': random.randint(1000, 1000000),
            'tanggal': fake.date(),
            'keterangan': fake.sentence(),
            'created_at': fake.date_time(),
            'updated_at': fake.date_time()
        })
    return data

# Generating fake data for 'pengguna' table
def generate_pengguna_data():
    data = []
    for _ in range(NUM_RECORDS):
        data.append({
            'pengguna_id': fake.uuid4(),
            'username': fake.user_name(),
            'password': fake.password(),
            'email': fake.email(),
            'alamat': fake.address(),
            'notelp': fake.phone_number(),
            'role': fake.random_element(elements=['admin', 'staff', 'kepala toko']),
            'created_at': fake.date_time(),
            'updated_at': fake.date_time()
        })
    return data

# Generating fake data for 'laporan_keuangan' table
def generate_laporan_keuangan_data():
    data = []
    for _ in range(NUM_RECORDS):
        data.append({
            'laporan_id': fake.uuid4(),
            'tanggal_laporan': fake.date(),
            'total_pendapatan': random.randint(1000000, 10000000),
            'total_pengeluaran': random.randint(500000, 5000000),
            'keuntungan': random.randint(100000, 5000000),
            'deskripsi': fake.text(),
            'created_at': fake.date_time(),
            'updated_at': fake.date_time()
        })
    return data

# Generate data for all tables
bahan_data = generate_bahan_data()
pemasok_data = generate_pemasok_data()
layanan_data = generate_layanan_data()
pelanggan_data = generate_pelanggan_data()
perbaikan_data = generate_perbaikan_data()
pengeluaran_data = generate_pengeluaran_data()
pengguna_data = generate_pengguna_data()
laporan_keuangan_data = generate_laporan_keuangan_data()

# Print sample data for demonstration
print("Sample 'bahan' data:", bahan_data)
print("Sample 'pemasok' data:", pemasok_data)
print("Sample 'layanan' data:", layanan_data)
print("Sample 'pelanggan' data:", pelanggan_data)
print("Sample 'perbaikan' data:", perbaikan_data)
print("Sample 'pengeluaran' data:", pengeluaran_data)
print("Sample 'pengguna' data:", pengguna_data)
print("Sample 'laporan_keuangan' data:", laporan_keuangan_data)
