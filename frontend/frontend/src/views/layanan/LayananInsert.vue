<template>
    <div class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="card" style="width: 80%;">
                    <div class="card-header">
                        <h4 class="card-title">Layanan Baru</h4>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="onSubmit">
                            <!-- Nama -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="namaLayanan">Nama Layanan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="namaLayanan" v-model="namaLayanan"
                                            required>
                                    </div>
                                </div>
                            </div>

                            <!-- Bahan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="namaBahan">Nama Bahan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <select class="form-control" id="namaBahan" v-model="namaBahan" required>
                                            <option value="" disabled>Pilih Bahan</option>
                                            <option v-for="bahan in daftarBahan" :key="bahan.bahan_id"
                                                :value="bahan.bahan_id">
                                                {{ bahan.nama_bahan }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <!-- Harga Layanan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="hargaLayanan">Harga Layanan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="number" class="form-control" id="hargaLayanan"
                                            v-model="hargaLayanan" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Estimasi -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="waktuEstimasi">Waktu Estimasi</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="number" class="form-control" id="waktuEstimasi"
                                            v-model="waktuEstimasi" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Deskripsi -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="deskripsi">Deskripsi</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="textarea" class="form-control" id="deskripsi" v-model="deskripsi"
                                            required>
                                    </div>
                                </div>
                            </div>

                            <button type="submit" class="btn btn-info btn-fill pull-right">Submit</button>
                            <div class="clearfix"></div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            namaLayanan: '',
            namaBahan: '',
            hargaLayanan: '',
            waktuEstimasi: '',
            deskripsi: '',
            daftarBahan: []
        };
    },

    mounted() {
        this.getBahan();
    },

    methods: {
        getBahan() {
            axios.get("http://localhost:50/daftarbahan")
                .then(response => {
                    this.daftarBahan = response.data;
                    console.log('Daftar Bahan:', this.daftarBahan);
                })
                .catch(error => {
                    console.error("Terjadi kesalahan saat mengambil data bahan:", error);
                });
        },
        onSubmit() {
            const hargaLayanan = parseFloat(this.hargaLayanan);
            const waktuEstimasiValue = parseInt(this.waktuEstimasi, 10);

            if (this.namaLayanan.trim() && this.namaBahan && !isNaN(hargaLayanan) && !isNaN(waktuEstimasiValue) && this.deskripsi) {
                const dataToSend = {
                    nama_layanan: this.namaLayanan,
                    bahan_id: this.namaBahan,
                    harga: this.hargaLayanan,
                    waktu_estimasi: this.waktuEstimasi,
                    deskripsi: this.deskripsi,
                };

                axios.post('http://localhost:50/daftarlayanan', dataToSend)
                    .then(response => {
                        console.log('Data berhasil dikirim:', response.data);
                        // Reset form atau lakukan tindakan lain setelah sukses
                        alert('Data berhasil ditambahkan!');
                        // Reset form atau melakukan tindakan lainnya
                        this.namaLayanan = '';
                        this.namaBahan = '';
                        this.hargaLayanan = '';
                        this.waktuEstimasi = '';
                        this.deskripsi = '';
                        this.$router.push({ name: 'layanan' });
                    })
                    .catch(error => {
                        console.error('Terjadi kesalahan saat mengirim data:', error);
                    });
            } else {
                alert('Silakan isi semua kolom yang wajib.');
            }
        }
    }
}
</script>
