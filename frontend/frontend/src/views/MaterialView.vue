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
                    <th>Jumlah</th>
                    <th>Harga Persatuan</th>
                    <th>Satuan</th>
                    <th>Pemasok</th>
                    <th>Aksi</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in tableData" :key="index">
                    <td>{{ item.no }}</td>
                    <td>{{ item.bahan }}</td>
                    <td>{{ item.jumlah }}</td>
                    <td>{{ item.harga }}</td>
                    <td>{{ item.satuan }}</td>
                    <td>{{ item.pemasok }}</td>
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
        { no: 1, bahan: "Dakota Rice", jumlah: "$36,738", harga: "Niger", satuan: "Oud-Turnhout", pemasok: "Oud-Turnhout" },
        { no: 2, bahan: "Minerva Hooper", jumlah: "$23,789", harga: "Curaçao", satuan: "Sinaai-Waas", pemasok: "Oud-Turnhout" },
        { no: 3, bahan: "Sage Rodriguez", jumlah: "$56,142", harga: "Netherlands", satuan: "Baileux", pemasok: "Oud-Turnhout" },
        { no: 4, bahan: "Philip Chaney", jumlah: "$38,735", harga: "Korea, South", satuan: "Overland Park", pemasok: "Oud-Turnhout" },
        { no: 5, bahan: "Doris Greene", jumlah: "$63,542", harga: "Malawi", satuan: "Feldkirchen in Kärnten", pemasok: "Oud-Turnhout" },
        { no: 6, bahan: "Mason Porter", jumlah: "$78,615", harga: "Chile", satuan: "Gloucester", pemasok: "Oud-Turnhout" }
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