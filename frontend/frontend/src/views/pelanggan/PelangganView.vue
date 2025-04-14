<template>
  <div class="content">
    <div class="container-fluid">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <button class="btn btn-primary btn-fill action-button" @click="onSubmit">+ Pelanggan Baru</button>
        <input type="text" v-model="searchQuery" class="form-control d-flex w-25" placeholder="Search..."
          @input="filterSearch" />
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="card strpied-tabled-with-hover">
            <div class="card-header">
              <h4 class="card-title">Daftar Pelanggan</h4>
            </div>
            <div class="card-body table-full-width table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>No</th>
                    <th>Nama</th>
                    <th>Alamat</th>
                    <th>Email</th>
                    <th>No Telp</th>
                    <th>Aksi</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(pelanggan, index) in paginatedPelanggan" :key="pelanggan.pelanggan_id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ pelanggan.nama }}</td>
                    <td>{{ pelanggan.alamat }}</td>
                    <td>{{ pelanggan.email }}</td>
                    <td>{{ pelanggan.telepon }}</td>
                    <td>
                      <button class="btn btn-info btn-fill action-button"
                        @click="showRiwayat(pelanggan.pelanggan_id, pelanggan.nama)">Riwayat</button>
                      <button class="btn btn-warning btn-fill action-button"
                        @click="onUpdate(pelanggan.pelanggan_id)">Edit</button>
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
        <!-- Modal untuk menampilkan detail perbaikan -->
        <div v-if="showModal" class="modal">
          <div class="modal-content">
            <div class="modal-header">
              <h2>Riwayat Perbaikan {{ namaPelanggan }}</h2>
              <button class="close-button" @click="closeModal" aria-label="Close">
                <i class="bi bi-x-lg"></i> <!-- Ganti dengan ikon yang Anda inginkan -->
              </button>
            </div>
            <div class="modal-body">
              <ul>
                <li v-for="riwayat in riwayatPerbaikan" :key="riwayat.riwayat_perbaikan_id">
                  <p><strong>Kode Perbaikan:</strong> {{ riwayat.kode_perbaikan }}</p>
                  <p><strong>Tanggal Perbaikan:</strong> {{ riwayat.tanggal_perbaikan }}</p>
                  <p><strong>Deskripsi:</strong> {{ riwayat.deskripsi_perbaikan }}</p>
                  <p><strong>Total Biaya:</strong> {{ formatRupiah(riwayat.total_biaya) }}</p>
                  <hr />
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
    <router-view></router-view>
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

export default {
  data() {
    return {
      api: 'http://localhost:50/daftarpelanggan', // Endpoint API
      showModal: false,
      riwayatPerbaikan: [],
      pelanggan: [],
      namaPelanggan: '',
      currentPage: 1,
      itemsPerPage: 20,
      searchQuery: '',
    };
  },

  computed: {
    totalPages() {
      return Math.ceil(this.filteredPelanggan.length / this.itemsPerPage);
    },
    paginatedPelanggan() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredPelanggan.slice(start, end);
    },
    filteredPelanggan() {
      if (!this.searchQuery) {
        return this.pelanggan;
      }
      const lowerCaseQuery = this.searchQuery.toLowerCase();
      return this.pelanggan.filter(pelanggan =>
        pelanggan.nama.toLowerCase().includes(lowerCaseQuery) ||
        pelanggan.alamat.toLowerCase().includes(lowerCaseQuery) ||
        pelanggan.email.toLowerCase().includes(lowerCaseQuery) ||
        pelanggan.telepon.toLowerCase().includes(lowerCaseQuery)
      );
    },
  },

  mounted() {
    this.getPelanggan();
  },

  methods: {
    getPelanggan() {
      axios.get(this.api)
        .then(response => {
          console.log(response.data); // Log data API untuk debugging
          this.pelanggan = response.data; // Menyimpan data bahan dari API
        })
        .catch(error => {
          console.log('Error fetching data:', error);
        });
    },
    // viewDetail(index) {
    //   // Logika untuk menampilkan detail item
    //   console.log("Lihat detail item ke-", index);
    // },
    onUpdate(pelanggan_id) {
      // Logika untuk mengedit item
      this.$router.push({ name: 'pelangganUpdate', params: { id: pelanggan_id } });
    },
    onDelete(index) {
      const pelanggan_id = this.pelanggan[index].pelanggan_id;

      // Menampilkan konfirmasi peringatan
      const isConfirmed = window.confirm("Apakah Anda yakin ingin menghapus data pelanggan ini?");

      if (isConfirmed) {
        // Jika pengguna mengkonfirmasi, lanjutkan dengan penghapusan
        axios.delete(`http://localhost:50/pelanggan?id=${pelanggan_id}`)
          .then(response => {
            console.log(response.data); // Menampilkan pesan sukses
            // Menghapus item yang telah dihapus dari array lokal
            this.pelanggan.splice(index, 1);
            alert("Data pelanggan berhasil dihapus!");
          })
          .catch(error => {
            console.log('Error deleting data:', error);
          });
      } else {
        console.log('Penghapusan dibatalkan');
      }
    },
    onSubmit() {
      this.$router.push('/pelanggan/insert');
    },
    formatRupiah(value) {
      const number = Number(value);
      if (isNaN(number)) return "-";
      return new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR" }).format(number);
    },
    showRiwayat(pelanggan_id, nama) {
      axios.get(`http://localhost:50/pelanggan?id=${pelanggan_id}`)
        .then(response => {
          // Pastikan response.data memiliki struktur yang benar
          if (response.data && response.data.riwayat_perbaikan) {
            this.riwayatPerbaikan = response.data.riwayat_perbaikan; // Ambil riwayat perbaikan dari respons
            this.namaPelanggan = nama;
            this.showModal = true;
          } else {
            console.error('Data tidak ditemukan');
            alert('Data tidak ditemukan');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('Gagal memuat detail perbaikan.');
        });
    },
    closeModal() {
      this.showModal = false;
    }
  }
};
</script>