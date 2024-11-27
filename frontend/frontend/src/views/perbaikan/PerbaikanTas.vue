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
                            <!-- Form utama -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="namaPelanggan">Nama Pelanggan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <select class="form-control" v-model="formData.namaPelanggan" id="namaPelanggan"
                                            required>
                                            <option value="" disabled>Pilih Pelanggan</option>
                                            <option v-for="pelanggan in daftarPelanggan" :key="pelanggan.pelanggan_id"
                                                :value="pelanggan.pelanggan_id">
                                                {{ pelanggan.nama }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <div v-for="(jenis, index) in formData.jenisPerbaikanList" :key="index"
                                class="row align-items-center mb-3">
                                <!-- Label -->
                                <div class="col-md-2">
                                    <label for="jenisPerbaikan" class="form-label">Layanan {{ index + 1
                                        }}</label>
                                </div>

                                <!-- Layanan -->
                                <div class="col-md-5">
                                    <select class="form-control" v-model="formData.jenisPerbaikanList[index].layanan_id"
                                        @change="updateHarga(index)" required>
                                        <option value="" disabled>Pilih Layanan</option>
                                        <option v-for="layanan in daftarLayanan" :key="layanan.layanan_id"
                                            :value="layanan.layanan_id">
                                            {{ layanan.nama_layanan }}
                                        </option>
                                    </select>
                                </div>

                                <!-- Harga -->
                                <div class="col-md-3">
                                    <input type="text" class="form-control"
                                        :value="formData.jenisPerbaikanList[index].harga" readonly />
                                </div>

                                <!-- Tombol Hapus -->
                                <div class="col-md-2 text-end">
                                    <button type="button" class="btn btn-danger"
                                        @click="removeJenisPerbaikan(index)">Hapus</button>
                                </div>
                            </div>


                            <!-- Tombol Tambah Jenis Perbaikan -->
                            <div class="row mb-3">
                                <div class="col-md-4">
                                    <button type="button" class="btn btn-success w-100"
                                        @click="addJenisPerbaikan">Tambah Jenis Perbaikan</button>
                                </div>
                            </div>


                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="tanggalMasuk">Tanggal Masuk</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="date" id="tanggalMasuk" v-model="formData.tanggalMasuk"
                                            class="form-control" required>
                                    </div>
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="tanggalKeluar">Tanggal Keluar</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="date" id="tanggalKeluar" v-model="formData.tanggalKeluar"
                                            class="form-control" required>
                                    </div>
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="biayaPerbaikan">Total Biaya</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="biayaPerbaikan"
                                            v-model="formData.biayaPerbaikan" required>
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
                                                <input type="radio" v-model="formData.statusPembayaran" value="lunas"
                                                    required>
                                                Sudah Bayar
                                            </label>
                                            <label>
                                                <input type="radio" v-model="formData.statusPembayaran"
                                                    value="belum-lunas" required>
                                                Belum Bayar
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
import axios from 'axios';

export default {
    data() {
        return {
            formData: {
                namaPelanggan: '',
                tanggalMasuk: '',
                tanggalKeluar: '',
                biayaPerbaikan: '',
                statusPembayaran: '',
                jenisPerbaikanList: [
                    { layanan_id: '', nama: '', harga: '' }
                ]
            },
            daftarPelanggan: [],
            daftarLayanan: [] // Menyimpan daftar layanan
        };
    },


    mounted() {
        this.getPelanggan();
        this.getLayanan();
    },

    methods: {
        getPelanggan() {
            axios.get("http://localhost:50/daftarpelanggan")
                .then(response => {
                    this.daftarPelanggan = response.data;
                    console.log('Daftar pelanggan:', this.daftarPelanggan);
                })
                .catch(error => {
                    console.error("Terjadi kesalahan saat mengambil data pelanggan:", error);
                });
        },
        getLayanan() {
            axios.get("http://localhost:50/daftarlayanan")
                .then(response => {
                    this.daftarLayanan = response.data;
                    console.log('Daftar layanan:', this.daftarLayanan);
                })
                .catch(error => {
                    console.error("Terjadi kesalahan saat mengambil data layanan:", error);
                });
        },
        updateHarga(index) {
            const selectedLayanan = this.daftarLayanan.find(
                layanan => layanan.layanan_id === this.formData.jenisPerbaikanList[index].layanan_id
            );
            if (selectedLayanan) {
                this.formData.jenisPerbaikanList[index].harga = selectedLayanan.harga;
            }
        },
        addJenisPerbaikan() {
            this.formData.jenisPerbaikanList.push({ layanan_id: '', nama: '', harga: '' });
        },
        removeJenisPerbaikan(index) {
            this.formData.jenisPerbaikanList.splice(index, 1);
        },
        resetForm() {
            this.formData = {
                namaPelanggan: '',
                tanggalMasuk: '',
                tanggalKeluar: '',
                biayaPerbaikan: '',
                statusPembayaran: '',
                jenisPerbaikanList: ['']
            };
        },
        handleSubmit() {
            if (
                this.formData.namaPelanggan &&
                this.formData.tanggalMasuk &&
                this.formData.tanggalKeluar &&
                this.formData.statusPembayaran &&
                this.formData.jenisPerbaikanList.every(jenis => jenis.trim() !== '')
            ) {
                console.log('Data terkirim:', this.formData);
                // Reset form setelah submit
                this.resetForm();
            } else {
                alert('Silakan isi semua kolom yang wajib.');
            }
        },
    }
};
</script>
