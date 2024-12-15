<template>
  <div class="content">
    <div class="container-fluid">
      <button class="btn btn-primary btn-fill action-button" @click="onSubmit" style="margin-bottom: 16px;">+ Insert
        Data</button>
      <div class="row">
        <div class="col-md-12">
          <div class="card strpied-tabled-with-hover">
            <div class="card-header">
              <h4 class="card-title">Jenis Layanan</h4>
            </div>
            <div class="card-body table-full-width table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>No</th>
                    <th>Nama Layanan</th>
                    <th>Bahan</th>
                    <th>Harga</th>
                    <th>Waktu Estimasi</th>
                    <th>Deskripsi</th>
                    <th>Gambar</th>
                    <th>Aksi</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(layanan, index) in layanan" :key="layanan.layanan_id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ layanan.nama_layanan }}</td>
                    <td>{{ layanan.nama_bahan }}</td>
                    <td>{{ layanan.harga }}</td>
                    <td>{{ layanan.waktu_estimasi }} hari</td>
                    <td>{{ layanan.deskripsi.length > 50 ? layanan.deskripsi.substring(0, 50) + '...' :
                      layanan.deskripsi }}</td>
                    <td><template v-if="layanan.gambar">
                        <img :src="`http://localhost:50/uploads/images/${layanan.gambar}`" alt="Gambar Layanan"
                          class="img-thumbnail" style="width: 100px; height: 100px;">
                      </template>
                      <span v-else>No Image</span>
                    </td>
                    <td>
                      <button class="btn btn-info btn-fill action-button"
                        @click="showDetailLayanan(layanan.layanan_id)">Detail</button>
                      <button class="btn btn-warning btn-fill action-button"
                        @click="onUpdate(layanan.layanan_id)">Edit</button>
                      <button class="btn btn-danger btn-fill action-button" @click="onDelete(index)">Hapus</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- Paginasi -->
            <nav aria-label="Table Pagination">
              <ul class="pagination">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                  <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">Previous</a>
                </li>
                <li class="page-item" :class="{ active: page === currentPage }" v-for="page in totalPages" :key="page">
                  <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                  <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">Next</a>
                </li>
              </ul>
            </nav>
          </div>
        </div>
        <!-- Modal untuk menampilkan detail layanan -->
        <div v-if="showModal" class="modal">
          <div class="modal-content">
            <div class="modal-header">
              <h2>Detail Layanan {{ detailLayanan.nama_layanan }}</h2>
              <button class="close-button" @click="closeModal" aria-label="Close">
                <i class="bi bi-x-lg"></i> <!-- Ganti dengan ikon yang Anda inginkan -->
              </button>
            </div>
            <div class="modal-body">
              <div v-if="detailLayanan.gambar">
                <img :src="`http://localhost:50/uploads/images/${detailLayanan.gambar}`" alt="Gambar Layanan"
                  class="img-thumbnail" style="max-width: 200px;">
              </div>
              <p><strong>Nama Layanan:</strong> {{ detailLayanan.nama_layanan }}</p>
              <p><strong>Deskripsi:</strong> {{ detailLayanan.deskripsi }}</p>
              <p><strong>Harga:</strong> {{ formatRupiah(detailLayanan.harga) }}</p>
              <p><strong>Waktu Estimasi:</strong> {{ detailLayanan.waktu_estimasi }} Hari</p>
              <p><strong>Nama Bahan:</strong> {{ detailLayanan.nama_bahan }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pagination {
  justify-content: right;
  margin-top: 15px;
  margin-right: 10px;
}

.table-hover tbody tr:hover {
  background-color: #f9f9f9;
}

.action-button {
  margin-right: 10px;
}

.modal {
  display: block;
  /* Pastikan modal ditampilkan */
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.5);
  /* Latar belakang transparan */
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  /* 15% dari atas dan tengah */
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  /* Lebar modal */
  position: relative;
  /* Agar tombol close bisa diposisikan */
}

.modal-header {
  display: flex;
  justify-content: space-between;
  /* Memastikan header terpisah */
  align-items: center;
  /* Vertikal center */
}
</style>

<script>
import axios from 'axios';
import * as bootstrap from 'bootstrap';

export default {
  data() {
    return {
      api: 'http://localhost:50/daftarlayanan', // Endpoint API
      layanan: [], // Menyimpan data bahan dalam bentuk array
      showModal: false,
      detailLayanan: {},
      currentPage: 1,
      itemsPerPage: 10,
    };
  },

  computed: {
    totalPages() {
      // Menghitung total halaman
      return Math.ceil(this.layanan.length / this.itemsPerPage);
    },
    paginatedLayanan() {
      // Mengambil data untuk halaman saat ini
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.layanan.slice(start, end);
    },
  },

  mounted() {
    // Memanggil metode getBahan saat komponen dimuat
    this.getLayanan();
  },

  methods: {
    getLayanan() {
      axios.get(this.api)
        .then(response => {
          console.log(response.data); // Log data API untuk debugging
          this.layanan = response.data; // Menyimpan data bahan dari API
        })
        .catch(error => {
          console.log('Error fetching data:', error);
        });
    },
    onSubmit() {
      this.$router.push('/jenislayanan/insert');
    },
    onUpdate(layanan_id) {
      this.$router.push({ name: 'layananUpdate', params: { id: layanan_id } });
    },
    onDelete(index) {
      const layanan_id = this.layanan[index].layanan_id;
      const isConfirmed = window.confirm("Apakah Anda yakin ingin menghapus data layanan ini?");

      if (isConfirmed) {
        axios.delete(`http://localhost:50/layanan?id=${layanan_id}`)
          .then(response => {
            console.log(response.data);
            this.layanan.splice(index, 1);
            alert("Data layanan berhasil dihapus!");
          })
          .catch(error => {
            console.log('Error deleting data:', error);
          });
      } else {
        console.log('Penghapusan dibatalkan');
      }
    },
    showDetailLayanan(layanan_id) {
      axios.get(`http://localhost:50/layanan?id=${layanan_id}`)
        .then(response => {
          // Pastikan response.data adalah array dan memiliki elemen
          if (response.data && response.data.length > 0) {
            this.detailLayanan = response.data[0]; // Ambil objek pertama dari array
            this.showModal = true; // Menampilkan modal
          } else {
            console.error('Data tidak ditemukan');
            alert('Data tidak ditemukan');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('Gagal memuat detail layanan.');
        });
    },
    closeModal() {
      this.showModal = false;
      this.detailLayanan = {}; // Reset layanan saat modal ditutup
    },
    formatRupiah(value) {
      return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR'
      }).format(value);
    }
  }
};
</script>