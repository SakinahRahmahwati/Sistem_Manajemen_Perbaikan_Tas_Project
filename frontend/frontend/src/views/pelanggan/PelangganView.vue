<template>
  <div class="content">
    <div class="container-fluid">
      <button class="btn btn-primary btn-fill action-button" @click="onSubmit" style="margin-bottom: 16px;">+ Insert
        Data</button>
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
                  <tr v-for="(pelanggan, index) in pelanggan" :key="pelanggan.pelanggan_id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ pelanggan.nama }}</td>
                    <td>{{ pelanggan.alamat }}</td>
                    <td>{{ pelanggan.email }}</td>
                    <td>{{ pelanggan.telepon }}</td>
                    <td>
                      <!-- <button class="btn btn-info btn-fill action-button" style="margin-right: 10px;"
                        @click="detailItem(index)">Detail</button> -->
                      <button class="btn btn-warning btn-fill action-button"
                        @click="onUpdate(pelanggan.pelanggan_id)">Edit</button>
                      <button class="btn btn-danger btn-fill action-button" @click="onDelete(index)">Hapus</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<style scoped>
.action-button {
  margin-right: 10px;
}
</style>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      api: 'http://localhost:50/daftarpelanggan', // Endpoint API
      pelanggan: [], // Menyimpan data bahan dalam bentuk array
    };
  },

  mounted() {
    // Memanggil metode getBahan saat komponen dimuat
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
    }
  }
};
</script>