<template>
  <div class="content">
    <div class="container-fluid">
      <button class="btn btn-primary btn-fill action-button" @click="onSubmit" style="margin-bottom: 16px;">+ Insert
        Data</button>
      <div class="row">
        <div class="col-md-12">
          <div class="card strpied-tabled-with-hover">
            <div class="card-header">
              <h4 class="card-title">List Perbaikan</h4>
            </div>
            <div class="card-body table-full-width table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>No</th>
                    <th>Kode Perbaikan</th>
                    <th>Nama Pelanggan</th>
                    <th>No Telpon</th>
                    <th>Waktu Estimasi</th>
                    <th>Status Perbaikan</th>
                    <th>Total Biaya</th>
                    <th>Status Pembayaran</th>
                    <th>Aksi</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(perbaikan, index) in perbaikan" :key="perbaikan.perbaikan_id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ perbaikan.kode_perbaikan }}</td>
                    <td>{{ perbaikan.nama_pelanggan }}</td>
                    <td>{{ perbaikan.notelp }}</td>
                    <td>{{ perbaikan.waktu_estimasi }} hari</td>
                    <td>
                      <select v-model="perbaikan.status"
                        @change="updateStatus(perbaikan.perbaikan_id, 'status', perbaikan.status)" class="form-control">
                        <option value="Dalam Antrian">Dalam Antrian</option>
                        <option value="Sedang Dikerjakan">Sedang Dikerjakan</option>
                        <option value="Selesai">Selesai</option>
                      </select>
                    </td>
                    <td>{{ formatRupiah(perbaikan.biaya_perbaikan) }}</td>
                    <td>
                      <select v-model="perbaikan.status_pembayaran"
                        @change="updateStatus(perbaikan.perbaikan_id, 'status_pembayaran', perbaikan.status_pembayaran)"
                        class="form-control">
                        <option value="Belum Bayar">Belum Bayar</option>
                        <option value="Sudah Bayar">Sudah Bayar</option>
                      </select>
                    </td>
                    <td>
                      <!-- <button class="btn btn-primary btn-fill action-button" style="margin-right: 10px;" @click="detailItem(index)">Detail</button> -->
                      <button class="btn btn-warning btn-fill action-button"
                        @click="onUpdate(perbaikan.perbaikan_id)">Edit</button>
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

export default {
  data() {
    return {
      api: 'http://localhost:50/daftarperbaikan', // Endpoint API
      perbaikan: [], // Menyimpan data bahan dalam bentuk array
      currentPage: 1,
      itemsPerPage: 10,
    };
  },

  computed: {
    totalPages() {
      // Menghitung total halaman
      return Math.ceil(this.perbaikan.length / this.itemsPerPage);
    },
    paginatedperbaikan() {
      // Mengambil data untuk halaman saat ini
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.perbaikan.slice(start, end);
    },
  },

  mounted() {
    // Memanggil metode getBahan saat komponen dimuat
    this.getperbaikan();
  },

  methods: {
    getperbaikan() {
      axios.get(this.api)
        .then(response => {
          console.log(response.data); // Log data API untuk debugging
          this.perbaikan = response.data; // Menyimpan data bahan dari API
        })
        .catch(error => {
          console.log('Error fetching data:', error);
        });
    },
    onSubmit() {
      this.$router.push('/perbaikan/insert');
    },
    onUpdate(perbaikan_id) {
      this.$router.push({ name: 'perbaikanUpdate', params: { id: perbaikan_id } });
    },
    onDelete(index) {
      const perbaikan_id = this.perbaikan[index].perbaikan_id;
      const isConfirmed = window.confirm("Apakah Anda yakin ingin menghapus data perbaikan ini?");

      if (isConfirmed) {
        axios.delete(`http://localhost:50/perbaikan?id=${perbaikan_id}`)
          .then(response => {
            console.log(response.data);
            this.perbaikan.splice(index, 1);
            alert("Data perbaikan berhasil dihapus!");
          })
          .catch(error => {
            console.log('Error deleting data:', error);
          });
      } else {
        console.log('Penghapusan dibatalkan');
      }
    },
    updateStatus(perbaikan_id, field, value) {
      const payload = { [field]: value }; // Membuat data payload
      axios.patch(`http://localhost:50/perbaikan/${perbaikan_id}`, payload)
        .then(response => {
          console.log(`Status ${field} berhasil diperbarui`, response.data);
          alert(`Status ${field} berhasil diperbarui`);
        })
        .catch(error => {
          console.error(`Gagal memperbarui ${field}:`, error);
          alert(`Gagal memperbarui ${field}. Silakan coba lagi.`);
        });
    },
    formatRupiah(value) {
      const number = Number(value);
      if (isNaN(number)) return '-';
      return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR' }).format(number);
    },

  }
};
</script>