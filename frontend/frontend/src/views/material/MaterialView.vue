<template>
  <div class="content">
    <div class="container-fluid">
      <!-- Notifikasi -->
      <!-- Notifikasi -->
      <div v-for="(notif, index) in notifications" :key="index"
        class="alert alert-danger alert-dismissible fade show d-flex justify-content-between align-items-center"
        role="alert">
        <span class="text-start">
          <strong>Peringatan:</strong> Stok bahan "{{ notif.nama_bahan }}" hanya tersisa {{ notif.stok }}!
        </span>
        <button type="button" class="btn-close-icon ms-auto" @click="closeNotification(index)" aria-label="Close">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>

      <button class="btn btn-primary btn-fill action-button" @click="onSubmit" style="margin-bottom: 16px;">+ Insert
        Data</button>
      <div class="row">
        <div class="col-md-12">
          <div class="card strpied-tabled-with-hover">
            <div class="card-header">
              <h4 class="card-title">Data Material</h4>
            </div>
            <div class="card-body table-full-width table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>No</th>
                    <th>Bahan</th>
                    <th>Harga Persatuan</th>
                    <th>Stok</th>
                    <th>Satuan</th>
                    <th>Pemasok</th>
                    <th>Tanggal Masuk</th>
                    <th>Gambar</th>
                    <th>Aksi</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(bahan, index) in paginatedBahan" :key="bahan.bahan_id">
                    <td>{{ bahan.no }}</td> <!-- Menampilkan nomor urut -->
                    <td>{{ bahan.nama_bahan }}</td>
                    <td>{{ bahan.harga_satuan }}</td>
                    <td>{{ bahan.stok }}</td>
                    <td>{{ bahan.satuan }}</td>
                    <td>{{ bahan.nama_pemasok }}</td>
                    <td>{{ bahan.tanggal_masuk ? new Date(bahan.tanggal_masuk).toLocaleDateString('id-ID', {
                      year:
                        'numeric', month: 'numeric', day: 'numeric'
                    }) : '' }}</td>
                    <td><template v-if="bahan.gambar">
                        <img :src="`http://localhost:50/uploads/images/${bahan.gambar}`" alt="Gambar Bahan"
                          class="img-thumbnail" style="width: 100px; height: 100px;">
                      </template>
                      <span v-else>No Image</span>
                    </td>
                    <td>
                      <button class="btn btn-info btn-fill action-button" @click="openModal(bahan.bahan_id)">+ Tambah
                        Stok</button>
                      <button class="btn btn-warning btn-fill action-button"
                        @click="onUpdate(bahan.bahan_id)">Edit</button>
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
      </div>
      <!-- Modal Tambah Stok -->
      <div class="modal fade" id="tambahStokModal" tabindex="-1" aria-labelledby="tambahStokModalLabel"
        aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="tambahStokModalLabel">Tambah Stok</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"><i class="bi bi-x-lg"></i></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label for="stokTambahan" class="form-label">Jumlah Stok Tambahan</label>
                <input type="number" id="stokTambahan" v-model="stokTambahan" class="form-control" />
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Batal</button>
              <button type="button" class="btn btn-primary" @click="addStok">Simpan</button>
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
</style>

<script>
import axios from 'axios';
import * as bootstrap from 'bootstrap';

export default {
  data() {
    return {
      api: 'http://localhost:50/daftarbahan', // Endpoint API
      bahan: [], // Menyimpan data bahan dalam bentuk array
      currentPage: 1, // Halaman saat ini
      itemsPerPage: 10, // Jumlah item per halaman
      stokTambahan: 0, // Jumlah stok tambahan dari input modal
      selectedBahanIndex: null,
      notifications: [],
    };
  },

  computed: {
    totalPages() {
      // Menghitung total halaman
      return Math.ceil(this.bahan.length / this.itemsPerPage);
    },
    paginatedBahan() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.bahan.slice(start, end).map((bahan, index) => ({
        ...bahan,
        no: start + index + 1
      }));
    },
  },

  mounted() {
    // Memanggil metode getBahan saat komponen dimuat
    this.getBahan();
  },

  methods: {
    getBahan() {
      axios.get(this.api)
        .then(response => {
          console.log(response.data); // Log data API untuk debugging
          this.bahan = response.data; // Menyimpan data bahan dari API
          this.checkLowStock();
        })
        .catch(error => {
          console.log('Error fetching data:', error);
        });
    },

    checkLowStock() {
      // Memfilter bahan dengan stok kurang dari 10
      this.notifications = this.bahan.filter((item) => item.stok < 10);
    },

    closeNotification(index) {
      this.notifications.splice(index, 1);
    },

    onSubmit() {
      this.$router.push('/material/insert');
    },

    onUpdate(bahan_id) {
      // Logika untuk mengedit item
      this.$router.push({ name: 'materialUpdate', params: { id: bahan_id } });
    },

    onDelete(index) {
      const bahan_id = this.bahan[index].bahan_id;

      // Menampilkan konfirmasi peringatan
      const isConfirmed = window.confirm("Apakah Anda yakin ingin menghapus data bahan ini?");

      if (isConfirmed) {
        // Jika pengguna mengkonfirmasi, lanjutkan dengan penghapusan
        axios.delete(`http://localhost:50/bahan?id=${bahan_id}`)
          .then(response => {
            console.log(response.data); // Menampilkan pesan sukses
            // Menghapus item yang telah dihapus dari array lokal
            this.bahan.splice(index, 1);
            alert("Data bahan berhasil dihapus!");
          })
          .catch(error => {
            console.log('Error deleting data:', error);
          });
      } else {
        console.log('Penghapusan dibatalkan');
      }
    },

    openModal(bahan_id) {
      if (this.bahan.length === 0) {
        console.error('Data bahan belum dimuat.');
        return;
      }
      this.selectedBahanIndex = this.bahan.findIndex(bahan => bahan.bahan_id === bahan_id);
      if (this.selectedBahanIndex === -1) {
        console.error('Data bahan tidak ditemukan.');
        return;
      }
      this.stokTambahan = 0;

      const modalElement = document.getElementById('tambahStokModal');
      const modalInstance = new bootstrap.Modal(modalElement);
      modalInstance.show();
    },

    addStok() {
      if (this.selectedBahanIndex !== -1) {
        const bahan = this.bahan[this.selectedBahanIndex];

        const stokTambahan = parseInt(this.stokTambahan || 0);
        if (isNaN(stokTambahan) || stokTambahan <= 0) {
          console.error('Stok tambahan tidak valid:', this.stokTambahan);
          return;
        }

        axios.post(`http://localhost:50/bahan?id=${bahan.bahan_id}`, { stok: stokTambahan })
          .then(response => {
            console.log(response.data);
            alert('Stok berhasil ditambahkan!');
            this.stokTambahan = 0; // Reset stok tambahan
            const modalElement = document.getElementById('tambahStokModal');
            const modalInstance = bootstrap.Modal.getInstance(modalElement);
            modalInstance.hide();
            this.getBahan(); // Refresh data bahan setelah update
          })
          .catch(error => {
            console.error('Error updating stock:', error.response ? error.response.data : error.message);
          });
      } else {
        console.error('Index tidak valid atau data bahan belum dimuat.');
      }
    },
    changePage(page) {
      this.currentPage = page;
    },
  }

};
</script>
