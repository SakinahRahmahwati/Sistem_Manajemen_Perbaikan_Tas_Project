<template>
  <div class="content">
    <div class="container-fluid">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <button class="btn btn-primary btn-fill action-button" @click="onSubmit">+ Perbaikan Baru</button>
        <input type="text" v-model="searchQuery" class="form-control d-flex w-25" placeholder="Search..."
          @input="filterSearch" />
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="card strpied-tabled-with-hover">
            <div class="card-header">
              <h4 class="card-title">Daftar Perbaikan</h4>
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
                  <tr v-for="(perbaikan, index) in paginatedPerbaikan" :key="perbaikan.perbaikan_id">
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
                      <button class="btn btn-info btn-fill action-button"
                        @click="showDetailPerbaikan(perbaikan.perbaikan_id)">Detail</button>
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
              <h2>Detail Perbaikan</h2>
              <button class="close-button" @click="closeModal" aria-label="Close">
                <i class="bi bi-x-lg"></i> <!-- Ganti dengan ikon yang Anda inginkan -->
              </button>
            </div>
            <div class="modal-body">
              <p><strong>Kode Perbaikan:</strong> {{ detailPerbaikan.kode_perbaikan }}</p>
              <p><strong>Pelanggan:</strong> {{ detailPerbaikan.pelanggan_id }}</p>
              <p><strong>Tanggal Masuk:</strong> {{ detailPerbaikan.tanggal_masuk }}</p>
              <p><strong>Tanggal Selesai:</strong> {{ detailPerbaikan.tanggal_selesai }}</p>
              <p><strong>Status Perbaikan:</strong> {{ detailPerbaikan.status }}</p>
              <p><strong>Status Pembayaran:</strong> {{ detailPerbaikan.status_pembayaran }}</p>
              <p><strong>Total Biaya:</strong> {{ formatRupiah(detailPerbaikan.biaya_perbaikan) }}</p>
              <h3>Layanan yang Dipilih</h3>
              <ul>
                <li
                  v-if="detailPerbaikan.layanan && Array.isArray(detailPerbaikan.layanan) && detailPerbaikan.layanan.length"
                  v-for="layanan in detailPerbaikan.layanan" :key="layanan.nama_layanan">
                  {{ layanan.nama_layanan }} (Rp. {{ formatRupiah(layanan.harga) }})
                </li>
                <li v-else>Tidak ada layanan yang dipilih.</li>
              </ul>
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
import axios from "axios";

export default {
  data() {
    return {
      apiGet: "http://localhost:50/daftarperbaikan", // Endpoint untuk GET data
      apiUpdate: "http://localhost:50/perbaikan", // Endpoint untuk PATCH data
      showModal: false,
      perbaikan: [],
      detailPerbaikan: {},
      currentPage: 1,
      itemsPerPage: 20,
      searchQuery: '',
    };
  },

  computed: {
    totalPages() {
      return Math.ceil(this.filteredPerbaikan.length / this.itemsPerPage);
    },
    paginatedPerbaikan() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredPerbaikan.slice(start, end);
    },
    filteredPerbaikan() {
      if (!this.searchQuery) {
        return this.perbaikan;
      }
      const lowerCaseQuery = this.searchQuery.toLowerCase();
      return this.perbaikan.filter(perbaikan =>
        perbaikan.kode_perbaikan.toLowerCase().includes(lowerCaseQuery) ||
        perbaikan.nama_pelanggan.toLowerCase().includes(lowerCaseQuery) ||
        perbaikan.notelp.toLowerCase().includes(lowerCaseQuery) ||
        perbaikan.status.toLowerCase().includes(lowerCaseQuery) ||
        perbaikan.status_pembayaran.toLowerCase().includes(lowerCaseQuery)
      );
    },
  },

  mounted() {
    this.getPerbaikan();
  },

  methods: {
    async getPerbaikan() {
      try {
        const response = await axios.get(this.apiGet);
        this.perbaikan = response.data.sort((a, b) => {
          if (a.status === "Selesai" && b.status !== "Selesai") return 1;
          if (a.status !== "Selesai" && b.status === "Selesai") return -1;
          if (a.status_pembayaran === "Sudah Bayar" && b.status_pembayaran !== "Sudah Bayar") return 1;
          if (a.status_pembayaran !== "Sudah Bayar" && b.status_pembayaran === "Sudah Bayar") return -1;
          return 0;
        });
      } catch (error) {
        console.error("Error fetching data:", error);
        alert("Gagal memuat data perbaikan.");
      }
    },

    onSubmit() {
      this.$router.push("/perbaikan/insert");
    },

    // onUpdate(perbaikan_id) {
    //   this.$router.push({ name: "perbaikanUpdate", params: { id: perbaikan_id } });
    // },

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

    async updateStatus(perbaikan_id, field, value) {
      const payload = { [field]: value };
      try {
        const response = await axios.patch(`${this.apiUpdate}?id=${perbaikan_id}`, payload);
        console.log(`Status berhasil diperbarui`, response.data);
        alert(`Status berhasil diperbarui`);
      } catch (error) {
        console.error(`Gagal memperbarui ${field}:`, error);
        alert(`Gagal memperbarui ${field}. Silakan coba lagi.`);
      }
    },

    formatRupiah(value) {
      const number = Number(value);
      if (isNaN(number)) return "-";
      return new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR" }).format(number);
    },

    showDetailPerbaikan(perbaikan_id) {
      axios.get(`http://localhost:50/perbaikan?id=${perbaikan_id}`)
        .then(response => {
          // Pastikan response.data memiliki struktur yang benar
          if (response.data) {
            this.detailPerbaikan = response.data; // Pastikan ini adalah objek yang benar
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
      this.showModal = false
    },
  },
};
</script>
