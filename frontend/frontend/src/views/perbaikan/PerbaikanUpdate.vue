<template>
    <div class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="card" style="width: 80%;">
                    <div class="card-header">
                        <h4 class="card-title">Edit Perbaikan</h4>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="onSubmit">
                            <!-- Kode Perbaikan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <label for="kodePerbaikan">Kode Perbaikan</label>
                                </div>
                                <div class="col-md-10">
                                    <input type="text" class="form-control" id="kodePerbaikan" v-model="kodePerbaikan"
                                        readonly />
                                </div>
                            </div>

                            <!-- Nama Pelanggan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <label for="pelanggan_id">Nama Pelanggan</label>
                                </div>
                                <div class="col-md-10">
                                    <select class="form-control" v-model="formData.pelanggan_id" id="pelanggan_id"
                                        required>
                                        <option value="" disabled>Pilih Pelanggan</option>
                                        <option v-for="pelanggan in daftarPelanggan" :key="pelanggan.pelanggan_id"
                                            :value="pelanggan.pelanggan_id">
                                            {{ pelanggan.nama }}
                                        </option>
                                    </select>
                                </div>
                            </div>

                            <!-- Jenis Perbaikan -->
                            <div v-for="(jenis, index) in formData.jenisPerbaikanList" :key="index"
                                class="row align-items-center mb-3">
                                <div class="col-md-2">
                                    <label for="jenisPerbaikan" class="form-label">Layanan {{ index + 1 }}</label>
                                </div>
                                <div class="col-md-5">
                                    <select class="form-control" v-model="jenis.layanan_id" @change="updateHarga(index)"
                                        required>
                                        <option value="" disabled>Pilih Layanan</option>
                                        <option v-for="layanan in daftarLayanan" :key="layanan.layanan_id"
                                            :value="layanan.layanan_id">
                                            {{ layanan.nama_layanan }}
                                        </option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <input type="text" class="form-control" :value="jenis.harga" readonly />
                                </div>
                                <div class="col-md-2 text-end">
                                    <button type="button" class="btn btn-danger" @click="removeJenisPerbaikan(index)">
                                        Hapus
                                    </button>
                                </div>
                            </div>

                            <!-- Tombol Tambah Layanan -->
                            <div class="row mb-3 justify-content-center">
                                <div class="col-md-3">
                                    <button type="button" class="btn btn-success btn-fill" @click="addJenisPerbaikan">
                                        <i class="nc-icon nc-simple-add"></i> Tambah Layanan
                                    </button>
                                </div>
                            </div>

                            <!-- Tanggal Masuk dan Keluar -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <label for="tanggalMasuk">Tanggal Masuk</label>
                                </div>
                                <div class="col-md-10">
                                    <input type="date" id="tanggalMasuk" v-model="formData.tanggalMasuk"
                                        class="form-control" required>
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <label for="tanggalKeluar">Tanggal Keluar</label>
                                </div>
                                <div class="col-md-10">
                                    <input type="date" id="tanggalKeluar" v-model="formData.tanggalKeluar"
                                        class="form-control" required>
                                </div>
                            </div>

                            <!-- Total Biaya -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <label for="totalBiaya">Total Biaya</label>
                                </div>
                                <div class="col-md-10">
                                    <input type="text" class="form-control" id="totalBiaya" :value="totalBiaya"
                                        readonly>
                                </div>
                            </div>

                            <!-- Status Pembayaran -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <label>Status Pembayaran</label>
                                </div>
                                <div class="col-md-10">
                                    <div>
                                        <label style="margin-right: 20px;">
                                            <input type="radio" v-model="formData.statusPembayaran" value="Sudah Bayar"
                                                required>
                                            Sudah Bayar
                                        </label>
                                        <label>
                                            <input type="radio" v-model="formData.statusPembayaran" value="Belum Bayar"
                                                required>
                                            Belum Bayar
                                        </label>
                                    </div>
                                </div>
                            </div>

                            <!-- Tombol Submit -->
                            <button type="submit" class="btn btn-primary btn-fill pull-right">
                                Update
                            </button>
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
            kodePerbaikan: '',
            isEdit: true,
            formData: {
                pelanggan_id: '',
                tanggalMasuk: '',
                tanggalKeluar: '',
                statusPembayaran: '',
                jenisPerbaikanList: [{ layanan_id: '', harga: '' }]
            },
            daftarPelanggan: [],
            daftarLayanan: []
        };
    },
    mounted() {
        this.getPelanggan();
        this.getLayanan();
        this.getPerbaikan(this.$route.params.perbaikan_id);
    },
    computed: {
        totalBiaya() {
            return this.formData.jenisPerbaikanList.reduce((total, item) => total + (parseFloat(item.harga) || 0), 0);
        }
    },
    methods: {
        getPelanggan() {
            axios.get('http://localhost:50/daftarpelanggan')
                .then(response => this.daftarPelanggan = response.data)
                .catch(error => console.error('Error:', error));
        },
        getLayanan() {
            axios.get('http://localhost:50/daftarlayanan')
                .then(response => this.daftarLayanan = response.data)
                .catch(error => console.error('Error:', error));
        },
        getPerbaikan(perbaikan_id) {
            axios.get(`http://localhost:50/perbaikan/${perbaikan_id}`)
                .then(response => {
                    const data = response.data;
                    this.kodePerbaikan = data.kode_perbaikan;
                    this.formData.pelanggan_id = data.pelanggan_id;
                    this.formData.tanggalMasuk = data.tanggal_masuk;
                    this.formData.tanggalKeluar = data.tanggal_selesai;
                    this.formData.statusPembayaran = data.status_pembayaran;
                    this.formData.jenisPerbaikanList = data.layanan.map(layanan => ({
                        layanan_id: layanan.layanan_id,
                        harga: layanan.harga
                    }));
                })
                .catch(error => console.error('Error:', error));
        },
        updateHarga(index) {
            const selectedLayanan = this.daftarLayanan.find(
                layanan => layanan.layanan_id === this.formData.jenisPerbaikanList[index].layanan_id
            );
            if (selectedLayanan) this.formData.jenisPerbaikanList[index].harga = selectedLayanan.harga;
        },
        addJenisPerbaikan() {
            this.formData.jenisPerbaikanList.push({ layanan_id: '', harga: '' });
        },
        removeJenisPerbaikan(index) {
            this.formData.jenisPerbaikanList.splice(index, 1);
        },
        onSubmit() {
            const payload = {
                kode_perbaikan: this.kodePerbaikan,
                pelanggan_id: this.formData.pelanggan_id,
                tanggal_masuk: this.formData.tanggalMasuk,
                tanggal_selesai: this.formData.tanggalKeluar,
                status_pembayaran: this.formData.statusPembayaran,
                layanan_ids: this.formData.jenisPerbaikanList.map(jenis => jenis.layanan_id),
                biaya_perbaikan: this.totalBiaya
            };

            axios.put(`http://localhost:50/daftarperbaikan/${this.$route.params.perbaikan_id}`, payload)
                .then(() => {
                    alert('Data berhasil diperbarui.');
                    this.$router.push({ name: 'perbaikan' });
                })
                .catch(error => console.error('Error:', error));
        }
    }
};
</script>