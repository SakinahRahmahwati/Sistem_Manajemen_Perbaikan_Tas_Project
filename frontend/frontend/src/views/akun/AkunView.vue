<template>
  <div class="content">
    <div class="container-fluid">
      <button class="btn btn-primary btn-fill action-button" @click="onSubmit" style="margin-bottom: 16px;">+ Pengguna Baru</button>
      <div class="row">
        <div class="col-md-12">
          <div class="card strpied-tabled-with-hover">
            <div class="card-header">
              <h4 class="card-title">Daftar Pengguna</h4>
            </div>
            <div class="card-body table-full-width table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>No</th>
                    <th>Username</th>
                    <th>Nama Pengguna</th>
                    <th>No Telpon</th>
                    <th>Role</th>
                    <th>Aksi</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(pengguna, index) in pengguna" :key="pengguna.pengguna_id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ pengguna.username }}</td>
                    <td>{{ pengguna.nama_pengguna }}</td>
                    <td>{{ pengguna.no_telp }}</td>
                    <td>{{ pengguna.role }}</td>
                    <td>
                      <!-- <button class="btn btn-primary btn-fill action-button" style="margin-right: 10px;"
                        @click="detailItem(index)">Detail</button> -->
                      <button class="btn btn-warning btn-fill action-button"
                        @click="onUpdate(pengguna.pengguna_id)">Edit</button>
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
      api: 'http://localhost:50/daftarpengguna', // Endpoint API
      pengguna: [],
      currentPage: 1,
      itemsPerPage: 10,
    };
  },

  computed: {
    totalPages() {
      return Math.ceil(this.pengguna.length / this.itemsPerPage);
    },
    paginatedPengguna() {
      // Mengambil data untuk halaman saat ini
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.pengguna.slice(start, end);
    },
  },

  mounted() {
    // Memanggil metode getBahan saat komponen dimuat
    this.getPengguna();
  },

  methods: {
    getPengguna() {
      axios.get(this.api)
        .then(response => {
          console.log(response.data);
          this.pengguna = response.data;
        })
        .catch(error => {
          console.log('Error fetching data:', error);
        });
    },
    onUpdate(pengguna_id) {
      this.$router.push({ name: 'akunUpdate', params: { id: pengguna_id } });
    },
    onDelete(index) {
      const pengguna_id = this.pengguna[index].pengguna_id;

      const isConfirmed = window.confirm("Apakah Anda yakin ingin menghapus data pengguna ini?");

      if (isConfirmed) {
        axios.delete(`http://localhost:50/kelola_akun?pengguna_id=${pengguna_id}`)
          .then(response => {
            console.log(response.data);
            this.pengguna.splice(index, 1);
            alert("Data pengguna berhasil dihapus!");
          })
          .catch(error => {
            console.log('Error deleting data:', error);
          });
      } else {
        console.log('Penghapusan dibatalkan');
      }
    },
    onSubmit() {
      this.$router.push('/kelola_akun');
    }
  }
};
</script>