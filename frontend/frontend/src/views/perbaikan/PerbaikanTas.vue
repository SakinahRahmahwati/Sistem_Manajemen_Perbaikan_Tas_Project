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
                            <!-- Nama Pelanggan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="customerName">Nama Pelanggan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <select class="form-control" v-model="customerName" id="customerName" required>
                                            <option selected>Choose...</option>
                                            <option>...</option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <!-- Jenis Perbaikan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="jenisPerbaikan">Jenis Perbaikan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <select class="form-control" v-model="jenisPerbaikan" id="jenisPerbaikan" required>
                                            <option selected>Choose...</option>
                                            <option>...</option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <!-- Tanggal Masuk -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="tanggalMasuk">Tanggal Masuk</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="date" id="tanggalMasuk" v-model="tanggalMasuk" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Tanggal Keluar -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="tanggalKeluar">Tanggal Keluar</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="date" id="tanggalKeluar" v-model="tanggalKeluar" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Biaya Perbaikan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="biayaPerbaikan">Biaya Perbaikan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="biayaPerbaikan" v-model="biayaPerbaikan" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Status Pembayaran -->
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
                                                <input type="radio" v-model="statusPembayaran" value="lunas" id="belumBayar" required>
                                                Belum Bayar
                                            </label>
                                            <label>
                                                <input type="radio" v-model="statusPembayaran" value="belum-lunas" id="sudahBayar" required>
                                                Sudah Bayar
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <button type="submit" class="btn btn-primary btn-fill pull-right">Submit</button>
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
            biayaPerbaikan: '',
            statusPembayaran: ''
        };
    },
    methods: {
        handleSubmit() {
            if (this.customerName && this.jenisPerbaikan && this.statusPembayaran) {
                console.log('Form dikirim:', {
                    customerName: this.customerName,
                    jenisPerbaikan: this.jenisPerbaikan,
                    statusPembayaran: this.statusPembayaran
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
