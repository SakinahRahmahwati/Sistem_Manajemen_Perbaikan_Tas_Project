<template>
    <div class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="card" style="width: 80%;">
                    <div class="card-header">
                        <h4 class="card-title">Material Baru</h4>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="onSubmit">
                            <!-- Nama -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="namaBahan">Nama Bahan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="namaBahan" v-model="namaBahan"
                                            required>
                                    </div>
                                </div>
                            </div>

                            <!-- Harga -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="hargaBahan">Harga Satuan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="number" class="form-control" id="hargaBahan" v-model="hargaBahan"
                                            required>
                                    </div>
                                </div>
                            </div>

                            <!-- Stok -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="stok">Jumlah Stok</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="number" class="form-control" id="stok" v-model="stok" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Satuan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="satuan">Satuan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="satuan" v-model="satuan" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Pemasok -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="namaPemasok">Nama Pemasok</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <select class="form-control" id="namaPemasok" v-model="namaPemasok" required>
                                            <option value="" disabled>Pilih Pemasok</option>
                                            <option v-for="pemasok in daftarPemasok" :key="pemasok.pemasok_id"
                                                :value="pemasok.pemasok_id">
                                                {{ pemasok.nama_pemasok }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <!-- Gambar Bahan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="gambarBahan">Gambar Bahan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="file" class="form-control" id="gambarBahan"
                                            @change="handleFileUpload" accept="image/*">
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

                            <!-- tanggal masuk -->
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
            namaBahan: '',
            hargaBahan: '',
            stok: '',
            satuan: '',
            namaPemasok: '',
            tanggalMasuk: '',
            gambarBahan: null,
            previewImage: null,
            daftarPemasok: []
        };
    },

    mounted() {
        this.getPemasok();
    },

    methods: {
        getPemasok() {
            axios.get("http://localhost:50/daftarpemasok")
                .then(response => {
                    this.daftarPemasok = response.data;
                })
                .catch(error => {
                    console.error("Error:", error);
                });
        },
        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.gambarBahan = file;
                this.previewImage = URL.createObjectURL(file);
            }
        },
        onSubmit() {
            const formData = new FormData();
            formData.append('nama_bahan', this.namaBahan);
            formData.append('harga_satuan', this.hargaBahan);
            formData.append('stok', this.stok);
            formData.append('satuan', this.satuan);
            formData.append('pemasok_id', this.namaPemasok);
            formData.append('tanggal_masuk', this.tanggalMasuk);
            formData.append('gambar', this.gambarBahan);

            axios.post('http://localhost:50/daftarbahan', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            })
                .then(response => {
                    alert('Data berhasil ditambahkan!');
                    this.$router.push({ name: 'material' });
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert(error.response?.data?.error || 'Terjadi kesalahan.');
                });
        }
    }
};
</script>
