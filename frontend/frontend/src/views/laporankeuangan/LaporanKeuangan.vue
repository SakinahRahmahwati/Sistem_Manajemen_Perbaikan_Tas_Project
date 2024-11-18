<template>
    <div class="content">
      <div class="container-fluid">
        <div class="row">
          <div class="col-md-12">
            <div class="card strpied-tabled-with-hover">
              <div class="card-header">
                <h4 class="card-title">Laporan Keuangan</h4>
              </div>
              <div class="card-body table-full-width table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>Tanggal</th>
                      <th>Perbaikan</th>
                      <th>Nama Pelanggan</th>
                      <th>pelanggan</th>
                      <th>Aksi</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in tableData" :key="index">
                      <td>{{ item.no }}</td>
                      <td>{{ item.tanggal }}</td>
                      <td>{{ item.perbaikan }}</td>
                      <td>{{ item.pelanggan }}</td>
                      <td>{{ item.harga }}</td>
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
  export default {
    data() {
      return {
        tableData: [
          { no: 1, tanggal: "Dakota Rice", perbaikan: "$36,738", pelanggan: "Niger", harga: "Oud-Turnhout"},
          { no: 2, tanggal: "Minerva Hooper", perbaikan: "$23,789", pelanggan: "Curaçao", harga: "Sinaai-Waas"},
          { no: 3, tanggal: "Sage Rodriguez", perbaikan: "$56,142", pelanggan: "Netherlands", harga: "Baileux"},
          { no: 4, tanggal: "Philip Chaney", perbaikan: "$38,735", pelanggan: "Korea, South", harga: "Overland Park"},
          { no: 5, tanggal: "Doris Greene", perbaikan: "$63,542", pelanggan: "Malawi", harga: "Feldkirchen in Kärnten"},
          { no: 6, tanggal: "Mason Porter", perbaikan: "$78,615", pelanggan: "Chile", harga: "Gloucester"}
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