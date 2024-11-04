<template>
    <div class="content">
      <div class="container-fluid">
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
                    <tr v-for="(item, index) in tableData" :key="index">
                      <td>{{ item.no }}</td>
                      <td>{{ item.layanan }}</td>
                      <td>{{ item.bahan }}</td>
                      <td>{{ item.harga }}</td>
                      <td>{{ item.estimasi }}</td>
                      <td>{{ item.deskripsi }}</td>
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
          { no: 1, layanan: "Dakota Rice", bahan: "$36,738", harga: "Niger", estimasi: "Oud-Turnhout", deskripsi: "Oud-Turnhout"},
          { no: 2, layanan: "Minerva Hooper", bahan: "$23,789", harga: "Curaçao", estimasi: "Sinaai-Waas", deskripsi: "Oud-Turnhout"},
          { no: 3, layanan: "Sage Rodriguez", bahan: "$56,142", harga: "Netherlands", estimasi: "Baileux", deskripsi: "Oud-Turnhout"},
          { no: 4, layanan: "Philip Chaney", bahan: "$38,735", harga: "Korea, South", estimasi: "Overland Park", deskripsi: "Oud-Turnhout"},
          { no: 5, layanan: "Doris Greene", bahan: "$63,542", harga: "Malawi", estimasi: "Feldkirchen in Kärnten", deskripsi: "Oud-Turnhout"},
          { no: 6, layanan: "Mason Porter", bahan: "$78,615", harga: "Chile", estimasi: "Gloucester", deskripsi: "Oud-Turnhout"}
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