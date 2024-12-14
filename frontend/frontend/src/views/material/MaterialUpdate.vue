<template>
    <div class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="card" style="width: 80%;">
                    <div class="card-header">
                        <h4 class="card-title">Edit Material</h4>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="onUpdate">
                            <!-- Nama -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_namaBahan">Edit Nama Bahan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="edit_namaBahan"
                                            v-model="edit_namaBahan" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Harga -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_hargaBahan">Edit Harga Satuan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="number" class="form-control" id="edit_hargaBahan"
                                            v-model="edit_hargaBahan" required>
                                    </div>
                                </div>
                            </div>

                            <!-- edit_Stok -->
                            <!-- <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_stok">Edit Jumlah Stok</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="number" class="form-control" id="edit_stok" v-model="edit_stok"
                                            >
                                    </div>
                                </div>
                            </div> -->

                            <!-- Satuan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_satuan">Edit Satuan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="edit_satuan" v-model="edit_satuan"
                                            required>
                                    </div>
                                </div>
                            </div>

                            <!-- Pemasok -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_namaPemasok">Edit Nama Pemasok</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <select class="form-control" id="edit_namaPemasok" v-model="edit_namaPemasok"
                                            required>
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
                                        <label for="edit_gambarBahan">Gambar Bahan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <!-- Tampilkan Gambar Saat Ini -->
                                    <div class="form-group">
                                        <img :src="edit_gambarBahanURL" alt="Gambar Bahan" width="200"
                                            v-if="edit_gambarBahanURL" />
                                    </div>
                                    <!-- Input File untuk Mengubah Gambar -->
                                    <div class="form-group">
                                        <input type="file" class="form-control" id="edit_gambarBahan"
                                            @change="handleFileUpload" accept="image/*" />
                                    </div>
                                </div>
                            </div>

                            <!-- Tanggal Masuk -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_tanggalMasuk">Edit Tanggal Masuk</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="date" id="edit_tanggalMasuk" v-model="edit_tanggalMasuk" required>
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
            edit_namaBahan: '',
            edit_hargaBahan: '',
            edit_stok: '',
            edit_satuan: '',
            edit_namaPemasok: '',
            edit_tanggalMasuk: '',
            edit_gambarBahan: null, // Untuk file baru
            edit_gambarBahanURL: '',
            daftarPemasok: []
        };
    },

    mounted() {
        this.getPemasok();
        const bahan_id = this.$route.params.id;
        this.getBahan(bahan_id);
    },

    methods: {
        getBahan(id) {
            axios.get(`http://localhost:50/bahan?id=${id}`)
                .then(response => {
                    const bahan = response.data[0];
                    this.edit_namaBahan = bahan.nama_bahan;
                    this.edit_hargaBahan = bahan.harga_satuan;
                    this.edit_stok = parseInt(bahan.stok, 10);
                    this.edit_satuan = bahan.satuan;
                    this.edit_namaPemasok = bahan.pemasok_id;
                    this.edit_gambarBahanURL = bahan.gambar_url;

                    const date = new Date(bahan.tanggal_masuk);
                    const formattedDate = date.toISOString().split('T')[0];
                    this.edit_tanggalMasuk = formattedDate;
                })
                .catch(error => {
                    console.error('Error fetching bahan data:', error);
                });
        },

        getPemasok() {
            axios.get("http://localhost:50/daftarpemasok")
                .then(response => {
                    this.daftarPemasok = response.data;
                })
                .catch(error => {
                    console.error("Terjadi kesalahan saat mengambil data pemasok:", error);
                });
        },

        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.edit_gambarBahan = file;
            }
        },

        onUpdate() {
            const bahan_id = this.$route.params.id;
            const formData = new FormData();
            formData.append('nama_bahan', this.edit_namaBahan);
            formData.append('harga_satuan', this.edit_hargaBahan);
            formData.append('stok', parseInt(this.edit_stok, 10));
            formData.append('satuan', this.edit_satuan);
            formData.append('pemasok_id', this.edit_namaPemasok);
            formData.append('tanggal_masuk', this.edit_tanggalMasuk);

            if (this.edit_gambarBahan) {
                formData.append('gambar_bahan', this.edit_gambarBahan);
            }

            axios.put(`http://localhost:50/bahan?id=${bahan_id}`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            })
                .then(response => {
                    alert('Data berhasil diperbarui!');
                    this.$router.push({ name: 'material' });
                })
                .catch(error => {
                    console.error('Terjadi kesalahan saat memperbarui data:', error);
                    alert('Terjadi kesalahan saat memperbarui data.');
                });
        }
    }
}
</script>
