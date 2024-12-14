<template>
    <div class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="card" style="width: 80%;">
                    <div class="card-header">
                        <h4 class="card-title">Edit Layanan</h4>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="onUpdate">
                            <!-- Nama Layanan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_namaLayanan">Nama Layanan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="edit_namaLayanan"
                                            v-model="edit_namaLayanan" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Bahan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_namaBahan">Nama Bahan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <select class="form-control" id="edit_namaBahan" v-model="edit_namaBahan"
                                            required>
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
                                        <label for="edit_hargaLayanan">Harga Layanan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="number" class="form-control" id="edit_hargaLayanan"
                                            v-model="edit_hargaLayanan" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Estimasi -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_waktuEstimasi">Waktu Estimasi</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="number" class="form-control" id="edit_waktuEstimasi"
                                            v-model="edit_waktuEstimasi" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Deskripsi -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_deskripsi">Deskripsi</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <textarea class="form-control" id="edit_deskripsi" v-model="edit_deskripsi"
                                        required style="height: 300px;"></textarea>
                                    </div>
                                </div>
                            </div>

                            <!-- Gambar Layanan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_gambarLayanan">Gambar Layanan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="file" class="form-control" id="edit_gambarLayanan"
                                            @change="handleFileUpload" accept="image/*" />
                                    </div>
                                    <div class="form-group">
                                        <img :src="edit_gambarLayananURL" alt="Gambar Layanan" width="200"
                                            v-if="edit_gambarLayananURL" />
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
            edit_namaLayanan: '',
            edit_namaBahan: '',
            edit_hargaLayanan: '',
            edit_waktuEstimasi: '',
            edit_deskripsi: '',
            edit_gambarLayanan: null, // Untuk file baru
            edit_gambarLayananURL: '',
            daftarBahan: []
        };
    },

    mounted() {
        this.getBahan();
        const layanan_id = this.$route.params.id;
        this.getLayanan(layanan_id);
    },

    methods: {
        getLayanan(id) {
            axios.get(`http://localhost:50/layanan?id=${id}`)
                .then(response => {
                    const layanan = response.data[0];
                    this.edit_namaLayanan = layanan.nama_layanan;
                    this.edit_namaBahan = layanan.bahan_id;
                    this.edit_hargaLayanan = layanan.harga;
                    this.edit_waktuEstimasi = layanan.waktu_estimasi;
                    this.edit_deskripsi = layanan.deskripsi;

                    // Set URL gambar hanya jika ada
                    this.edit_gambarLayananURL = layanan.gambar ? `http://localhost:50/uploads/images/${layanan.gambar}` : null;
                })
                .catch(error => {
                    console.error("Error fetching data layanan", error);
                });
        },
        getBahan() {
            axios.get("http://localhost:50/daftarbahan")
                .then(response => {
                    this.daftarBahan = response.data;
                    console.log('Daftar Bahan:', this.daftarBahan);
                })
                .catch(error => {
                    console.error("Terjadi kesalahan saat mengambil data pemasok:", error);
                });
        },
        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.edit_gambarLayanan = file;

                // Membaca file gambar dan mengubahnya menjadi URL untuk preview
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.edit_gambarLayananURL = e.target.result; // Set URL gambar untuk preview
                };
                reader.readAsDataURL(file); // Membaca file sebagai URL data
            }
        },
        onUpdate() {
            const layanan_id = this.$route.params.id;
            const formData = new FormData();
            formData.append('nama_layanan', this.edit_namaLayanan);
            formData.append('bahan_id', this.edit_namaBahan);
            formData.append('harga', this.edit_hargaLayanan);
            formData.append('waktu_estimasi', this.edit_waktuEstimasi);
            formData.append('deskripsi', this.edit_deskripsi);

            // Tambahkan gambar baru jika ada
            if (this.edit_gambarLayanan) {
                formData.append('gambar_layanan', this.edit_gambarLayanan);
            }

            axios.put(`http://localhost:50/layanan?id=${layanan_id}`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            })
                .then(response => {
                    alert('Data berhasil diperbarui!');
                    this.$router.push({ name: 'layanan' });
                })
                .catch(error => {
                    console.error('Terjadi kesalahan saat memperbarui data:', error);
                    alert('Terjadi kesalahan saat memperbarui data.');
                });
        }
    }
}
</script>