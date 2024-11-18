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
                    <th>Aksi</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(layanan, index) in layanan" :key="layanan.layanan_id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ layanan.nama_layanan }}</td>
                    <td>{{ layanan.nama_bahan }}</td>
                    <td>{{ layanan.harga }}</td>
                    <td>{{ layanan.waktu_estimasi }}</td>
                    <td>{{ layanan.deskripsi.length > 50 ? layanan.deskripsi.substring(0, 50) + '...' : layanan.deskripsi }}</td>
                    <td>
                      <!-- <button class="btn btn-primary btn-fill action-button" style="margin-right: 10px;" @click="detailItem(index)">Detail</button> -->
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
      api: 'http://localhost:50/layanan', // Endpoint API
      layanan: [], // Menyimpan data bahan dalam bentuk array
    };
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
    // editItem(index) {
    //   // Logika untuk mengedit item
    //   console.log("Edit item ke-", index);
    // },
    // deleteItem(index) {
    //   // Logika untuk menghapus item
    //   console.log("Hapus item ke-", index);
    //   // Contoh menghapus item dari array
    //   this.tableData.splice(index, 1);
    // }
  }
};
</script>