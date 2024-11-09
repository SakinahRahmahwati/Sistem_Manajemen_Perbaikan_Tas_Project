<template>
  <div class="content">
    <div class="container-fluid">
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
                    <th>Jumlah</th>
                    <th>Satuan</th>
                    <th>Pemasok</th>
                    <th>Aksi</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(bahan, index) in bahan" :key="bahan.bahan_id">
                    <td>{{ index + 1 }}</td> <!-- Menampilkan nomor urut -->
                    <td>{{ bahan.nama_bahan }}</td>
                    <td>{{ bahan.harga_satuan }}</td>
                    <td>{{ bahan.stok }}</td>
                    <td>{{ bahan.satuan }}</td>
                    <td>{{ bahan.nama_pemasok }}</td>
                    <td>
                      <button class="btn btn-warning btn-fill action-button" @click="editItem(index)">Edit</button>
                      <button class="btn btn-danger btn-fill action-button" @click="deleteItem(index)">Hapus</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
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
      api: 'http://localhost:50/bahan', // Endpoint API
      bahan: [], // Menyimpan data bahan dalam bentuk array
    };
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
        })
        .catch(error => {
          console.log('Error fetching data:', error);
        });
    },
    // editItem(index) {
    //   console.log("Edit item ke-", index);
    // },
    // deleteItem(index) {
    //   console.log("Hapus item ke-", index);
    //   // Menghapus item dari array bahan (jika diperlukan)
    //   this.bahan.splice(index, 1);
    // }
  }
};
</script>
