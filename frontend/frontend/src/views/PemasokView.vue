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
                      <th>Nama pemasok</th>
                      <th>Alamat</th>
                      <th>Email</th>
                      <th>No Telp</th>
                      <th>Aksi</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in tableData" :key="index">
                      <td>{{ item.no }}</td>
                      <td>{{ item.pemasok }}</td>
                      <td>{{ item.bahan }}</td>
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
          { no: 1, pemasok: "Dakota Rice", bahan: "$36,738", alamat: "Niger", email: "Oud-Turnhout", notelp: "Oud-Turnhout" },
          { no: 2, pemasok: "Minerva Hooper", bahan: "$23,789", alamat: "Curaçao", email: "Sinaai-Waas", notelp: "Oud-Turnhout" },
          { no: 3, pemasok: "Sage Rodriguez", bahan: "$56,142", alamat: "Netherlands", email: "Baileux", notelp: "Oud-Turnhout" },
          { no: 4, pemasok: "Philip Chaney", bahan: "$38,735", alamat: "Korea, South", email: "Overland Park", notelp: "Oud-Turnhout" },
          { no: 5, pemasok: "Doris Greene", bahan: "$63,542", alamat: "Malawi", email: "Feldkirchen in Kärnten", notelp: "Oud-Turnhout" },
          { no: 6, pemasok: "Mason Porter", bahan: "$78,615", alamat: "Chile", email: "Gloucester", notelp: "Oud-Turnhout" }
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