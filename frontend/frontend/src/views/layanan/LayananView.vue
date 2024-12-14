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
                      <!-- <button class="btn btn-primary btn-fill action-button" style="margin-right: 10px;" @click="detailItem(index)">Detail</button> -->
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
      api: 'http://localhost:50/daftarlayanan', // Endpoint API
      layanan: [], // Menyimpan data bahan dalam bentuk array
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
  }
};
</script>