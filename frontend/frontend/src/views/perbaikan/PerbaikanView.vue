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
import axios from "axios";

export default {
  data() {
    return {
      apiGet: "http://localhost:50/daftarperbaikan", // Endpoint untuk GET data
      apiUpdate: "http://localhost:50/perbaikan", // Endpoint untuk PATCH data
      perbaikan: [],
      currentPage: 1,
      itemsPerPage: 10,
    };
  },

  computed: {
    totalPages() {
      return Math.ceil(this.perbaikan.length / this.itemsPerPage);
    },
    paginatedPerbaikan() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.perbaikan.slice(start, end);
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

    onUpdate(perbaikan_id) {
      this.$router.push({ name: "perbaikanUpdate", params: { id: perbaikan_id } });
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

    async updateStatus(perbaikan_id, field, value) {
      const payload = { [field]: value };
      try {
        const response = await axios.patch(`${this.apiUpdate}?id=${perbaikan_id}`, payload);
        console.log(`Status ${field} berhasil diperbarui`, response.data);
        alert(`Status ${field} berhasil diperbarui`);
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
  },
};
</script>
