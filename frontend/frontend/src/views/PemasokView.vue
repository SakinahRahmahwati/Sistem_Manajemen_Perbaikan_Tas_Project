<template>
  <div class="content">
    <div class="container-fluid">
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
                  <tr v-for="(pemasok, index) in pemasok" :key="pemasok.pemasok_id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ pemasok.nama_pemasok }}</td>
                    <td>{{ pemasok.alamat }}</td>
                    <td>{{ pemasok.email }}</td>
                    <td>{{ pemasok.telepon }}</td>
                    <td>
                      <button class="btn btn-primary btn-fill action-button" style="margin-right: 10px;"
                        @click="detailItem(index)">Detail</button>
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
      api: 'http://localhost:50/pemasok', // Endpoint API
      pemasok: [], // Menyimpan data bahan dalam bentuk array
    };
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