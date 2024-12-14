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
                                        required style="height: 300px;">
                                    </div>
                                </div>
                            </div>

                            <!-- Gambar Layanan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="gambar">Gambar Layanan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="file" class="form-control" id="gambar" @change="handleFileUpload"
                                            accept="image/*">
                                    </div>
                                </div>
                            </div>

                            <!-- Preview Gambar -->
                            <div v-if="previewImage" class="row">
                                <div class="col-md-12 text-center">
                                    <img :src="previewImage" alt="Preview Gambar" class="img-thumbnail"
                                        style="max-width: 200px;">
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
            gambar: null,
            previewImage: null,
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
        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.gambar = file;
                this.previewImage = URL.createObjectURL(file);
            }
        },
        onSubmit() {
            const hargaLayanan = parseFloat(this.hargaLayanan);
            const waktuEstimasiValue = parseInt(this.waktuEstimasi, 10);

            if (this.namaLayanan.trim() && this.namaBahan && !isNaN(hargaLayanan) && !isNaN(waktuEstimasiValue) && this.deskripsi) {
                const formData = new FormData();
                formData.append('nama_layanan', this.namaLayanan);
                formData.append('bahan_id', this.namaBahan);
                formData.append('harga', this.hargaLayanan);
                formData.append('waktu_estimasi', this.waktuEstimasi);
                formData.append('deskripsi', this.deskripsi);
                formData.append('gambar', this.gambar);

                axios.post('http://localhost:50/daftarlayanan', formData)
                    .then(response => {
                        console.log('Data berhasil dikirim:', response.data);
                        alert('Data berhasil ditambahkan!');
                        this.$router.push({ name: 'layanan' });
                        this.resetForm();
                    })
                    .catch(error => {
                        console.error('Terjadi kesalahan saat mengirim data:', error);
                    });
            } else {
                alert('Silakan isi semua kolom yang wajib.');
            }
        },
        onFileChange(event) {
            this.gambar = event.target.files[0];
        },
        resetForm() {
            this.namaLayanan = '';
            this.namaBahan = '';
            this.hargaLayanan = '';
            this.waktuEstimasi = '';
            this.deskripsi = '';
            this.gambar = null;
        }
    }
}
</script>
