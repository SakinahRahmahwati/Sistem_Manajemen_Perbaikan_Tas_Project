<template>
    <div class="content">
      <div class="container-fluid">
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
                      <th>Almat</th>
                      <th>Email</th>
                      <th>No Telp</th>
                      <th>Aksi</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in tableData" :key="index">
                      <td>{{ item.no }}</td>
                      <td>{{ item.nama }}</td>
                      <td>{{ item.alamat }}</td>
                      <td>{{ item.email }}</td>
                      <td>{{ item.notelp }}</td>
                      <td>
                        <button class="btn btn-primary btn-fill action-button" style="margin-right: 10px;" @click="detailItem(index)">Detail</button>
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
  export default {
    data() {
      return {
        tableData: [
          { no: 1, nama: "Dakota Rice", alamat: "$36,738", email: "Niger", notelp: "Oud-Turnhout" },
          { no: 2, nama: "Minerva Hooper", alamat: "$23,789", email: "Curaçao", notelp: "Sinaai-Waas" },
          { no: 3, nama: "Sage Rodriguez", alamat: "$56,142", email: "Netherlands", notelp: "Baileux" },
          { no: 4, nama: "Philip Chaney", alamat: "$38,735", email: "Korea, South", notelp: "Overland Park" },
          { no: 5, nama: "Doris Greene", alamat: "$63,542", email: "Malawi", notelp: "Feldkirchen in Kärnten" },
          { no: 6, nama: "Mason Porter", alamat: "$78,615", email: "Chile", notelp: "Gloucester" }
        ]
      };
    },
    methods:  {
      viewDetail(index) {
        // Logika untuk menampilkan detail item
        console.log("Lihat detail item ke-", index);
      },
      editItem(index) {
        // Logika untuk mengedit item
        console.log("Edit item ke-", index);
      },
      deleteItem(index) {
        // Logika untuk menghapus item
        console.log("Hapus item ke-", index);
        // Contoh menghapus item dari array
        this.tableData.splice(index, 1);
      }
    }
  };
  </script>