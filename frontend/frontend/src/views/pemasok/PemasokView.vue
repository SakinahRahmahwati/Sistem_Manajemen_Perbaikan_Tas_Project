<template>
  <div class="content">
    <div class="container-fluid">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <button class="btn btn-primary btn-fill action-button" @click="onSubmit">+ Pemasok Baru</button>
        <input type="text" v-model="searchQuery" class="form-control d-flex w-25" placeholder="Search..."
          @input="filterSearch" />
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="card strpied-tabled-with-hover">
            <div class="card-header">
              <h4 class="card-title">Daftar Pemasok</h4>
            </div>
            <div class="card-body table-full-width table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>No</th>
                    <th>Nama Pemasok</th>
                    <th>Alamat</th>
                    <th>Email</th>
                    <th>No Telp</th>
                    <th>Aksi</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(pemasok, index) in paginatedPemasok" :key="pemasok.pemasok_id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ pemasok.nama_pemasok }}</td>
                    <td>{{ pemasok.alamat }}</td>
                    <td>{{ pemasok.email }}</td>
                    <td>{{ pemasok.telepon }}</td>
                    <td>
                      <!-- <button class="btn btn-primary btn-fill action-button" style="margin-right: 10px;"
                        @click="detailItem(index)">Detail</button> -->
                      <button class="btn btn-warning btn-fill action-button"
                        @click="onUpdate(pemasok.pemasok_id)">Edit</button>
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
</style>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      api: 'http://localhost:50/daftarpemasok', // Endpoint API
      pemasok: [],
      currentPage: 1,
      itemsPerPage: 20,
      searchQuery: '',
    };
  },

  computed: {
    totalPages() {
      return Math.ceil(this.filteredPemasok.length / this.itemsPerPage);
    },
    paginatedPemasok() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredPemasok.slice(start, end);
    },
    filteredPemasok() {
      if (!this.searchQuery) {
        return this.pemasok;
      }
      const lowerCaseQuery = this.searchQuery.toLowerCase();
      return this.pemasok.filter(pemasok =>
        pemasok.nama_pemasok.toLowerCase().includes(lowerCaseQuery) ||
        pemasok.alamat.toLowerCase().includes(lowerCaseQuery) ||
        pemasok.email.toLowerCase().includes(lowerCaseQuery) ||
        pemasok.telepon.toLowerCase().includes(lowerCaseQuery)
      );
    },
  },

  mounted() {
    // Memanggil metode getBahan saat komponen dimuat
    this.getPemasok();
  },

  methods: {
    getPemasok() {
      axios.get(this.api)
        .then(response => {
          console.log(response.data);
          this.pemasok = response.data;
        })
        .catch(error => {
          console.log('Error fetching data:', error);
        });
    },
    // viewDetail(index) {
    //   // Logika untuk menampilkan detail item
    //   console.log("Lihat detail item ke-", index);
    // },
    onUpdate(pemasok_id) {
      // Logika untuk mengedit item
      this.$router.push({ name: 'pemasokUpdate', params: { id: pemasok_id } });
    },
    onDelete(index) {
      const pemasok_id = this.pemasok[index].pemasok_id;

      // Menampilkan konfirmasi peringatan
      const isConfirmed = window.confirm("Apakah Anda yakin ingin menghapus data pemasok ini?");

      if (isConfirmed) {
        // Jika pengguna mengkonfirmasi, lanjutkan dengan penghapusan
        axios.delete(`http://localhost:50/pemasok?id=${pemasok_id}`)
          .then(response => {
            console.log(response.data); // Menampilkan pesan sukses
            // Menghapus item yang telah dihapus dari array lokal
            this.pemasok.splice(index, 1);
            alert("Data pemasok berhasil dihapus!");
          })
          .catch(error => {
            console.log('Error deleting data:', error);
          });
      } else {
        console.log('Penghapusan dibatalkan');
      }
    },
    onSubmit() {
      this.$router.push('/pemasok/insert');
    }
  }
};
</script>