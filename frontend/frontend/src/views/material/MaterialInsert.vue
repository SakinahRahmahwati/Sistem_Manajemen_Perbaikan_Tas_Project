<template>
  <div class="content">
      <div class="container-fluid">
          <div class="row">
              <div class="card" style="width: 80%;">
                  <div class="card-header">
                      <h4 class="card-title">Perbaikan Baru</h4>
                  </div>
                  <div class="card-body">
                      <form @submit.prevent="handleSubmit">
                          <div class="row">
                              <div class="col-md-2 pr-1">
                                  <div class="form-group">
                                      <label>Nama Pelanggan</label>
                                  </div>
                              </div>
                              <div class="col-md-10">
                                  <div class="form-group">
                                      <select class="form-control" v-model="customerName" required>
                                          <option selected>Choose...</option>
                                          <option>...</option>
                                      </select>
                                  </div>
                              </div>
                          </div>
                          <div class="row">
                              <div class="col-md-2 pr-1">
                                  <div class="form-group">
                                      <label>Jenis Perbaikan</label>
                                  </div>
                              </div>
                              <div class="col-md-10">
                                  <div class="form-group">
                                      <select class="form-control" v-model="jenisPerbaikan" required>
                                          <option selected>Choose...</option>
                                          <option>...</option>
                                      </select>
                                  </div>
                              </div>
                          </div>
                          <div class="row">
                              <div class="col-md-2 pr-1">
                                  <div class="form-group">
                                      <label for="tanggal">Tanggal Masuk</label>
                                  </div>
                              </div>
                              <div class="col-md-10">
                                  <div class="form-group">
                                      <input type="date" id="tanggalMasuk" v-model="tanggal">
                                  </div>
                              </div>
                          </div>
                          <div class="row">
                              <div class="col-md-2 pr-1">
                                  <div class="form-group">
                                      <label for="tanggal">Tanggal Keluar</label>
                                  </div>
                              </div>
                              <div class="col-md-10">
                                  <div class="form-group">
                                      <input type="date" id="tanggalKeluar" v-model="tanggal">
                                  </div>
                              </div>
                          </div>
                          <div class="row">
                              <div class="col-md-2 pr-1">
                                  <div class="form-group">
                                      <label>Biaya Perbaikan</label>
                                  </div>
                              </div>
                              <div class="col-md-10">
                                  <div class="form-group">
                                      <input type="text" class="form-control">
                                  </div>
                              </div>
                          </div>
                          <div class="row">
                              <div class="col-md-2 pr-1">
                                  <div class="form-group">
                                      <label>Status Pembayaran</label>
                                  </div>
                              </div>
                              <div class="col-md-10">
                                  <div class="form-group">
                                      <div>
                                          <label style="margin-right: 20px;">
                                              <input type="radio" v-model="statusPembayaran" value="lunas" required>
                                              Belum Bayar
                                          </label>
                                          <label>
                                              <input type="radio" v-model="statusPembayaran" value="belum-lunas"
                                                  required>
                                              Sudah Bayar
                                          </label>
                                      </div>

                                  </div>
                              </div>
                          </div>
                          <button type="submit" class="btn btn-info btn-fill pull-right">Update Profile</button>
                          <div class="clearfix"></div>
                      </form>
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
export default {
  data() {
      return {
          customerName: '',
          jenisPerbaikan: '',
          tanggalMasuk: '',
          tanggalKeluar: '',
          statusPembayaran: ''
      };
  },
  methods: {
      handleSubmit() {
          if (this.customerName && this.jenisPerbaikan && this.statusPembayaran) {
              console.log('Form dikirim:', {
                  customerName: this.customerName,
                  jenisPerbaikan: this.jenisPerbaikan,
                  statusPembayaran: this.statusPembayaran // Menambahkan status pembayaran
              });
              // Reset form atau melakukan tindakan lain
              this.customerName = '';
              this.jenisPerbaikan = '';
              this.statusPembayaran = ''; // Reset status pembayaran
          } else {
              alert('Silakan isi semua kolom yang wajib.');
          }
      }

  }
}
</script>