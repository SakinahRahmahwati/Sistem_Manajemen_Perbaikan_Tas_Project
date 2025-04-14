<template>
    <div class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="card" style="width: 80%;">
                    <div class="card-header">
                        <h4 class="card-title">Form Pengeluaran</h4>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="onSubmit">
                            <!-- Tanggal Pengeluaran -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="tanggal_pengeluaran">Tanggal Pengeluaran</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="date" class="form-control" v-model="tanggalPengeluaran" required />
                                    </div>
                                </div>
                            </div>

                            <!-- Pemasok -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="pemasok_id">Pemasok</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <select v-model="pemasokId" class="form-control">
                                            <option v-for="pemasok in daftarPemasok" :key="pemasok.pemasok_id"
                                                :value="pemasok.pemasok_id">
                                                {{ pemasok.nama_pemasok }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <!-- Bahan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="bahan_id">Bahan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <select v-model="bahanId" class="form-control">
                                            <option v-for="bahan in daftarBahan" :key="bahan.bahan_id"
                                                :value="bahan.bahan_id">
                                                {{ bahan.nama_bahan }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <!-- Jenis Pengeluaran -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="jenis_pengeluaran">Jenis Pengeluaran</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" v-model="jenisPengeluaran" class="form-control" required />
                                    </div>
                                </div>
                            </div>

                            <!-- total  Pengeluaran -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="total_pengeluaran">Total Pengeluaran</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="number" v-model="totalPengeluaran" class="form-control" required />
                                    </div>
                                </div>
                            </div>

                            <!-- deskripsi -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="keterangan">Deskripsi</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <textarea v-model="keterangan" class="form-control"></textarea>
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
            tanggalPengeluaran: '',
            jenisPengeluaran: '',
            totalPengeluaran: '',
            keterangan: '',
            pemasokId: '', // Pemasok ID yang dipilih
            bahanId: '', // Bahan ID yang dipilih
            daftarPemasok: [], // Daftar pemasok
            daftarBahan: [], // Daftar bahan
        };
    },

    mounted() {
        this.getPemasok();
        this.getBahan();
    },

    methods: {
        // Ambil data pemasok dari backend
        getPemasok() {
            axios.get("http://localhost:50/daftarpemasok")
                .then(response => {
                    this.daftarPemasok = response.data; // Menyimpan data pemasok dalam daftarPemasok
                    console.log('Daftar Pemasok:', this.daftarPemasok);
                })
                .catch(error => {
                    console.error("Terjadi kesalahan saat mengambil data pemasok:", error);
                });
        },

        // Ambil data bahan dari backend
        getBahan() {
            axios.get("http://localhost:50/daftarbahan")
                .then(response => {
                    this.daftarBahan = response.data; // Menyimpan data bahan dalam daftarBahan
                    console.log('Daftar Bahan:', this.daftarBahan);
                })
                .catch(error => {
                    console.error("Terjadi kesalahan saat mengambil data bahan:", error);
                });
        },

        // Kirim data pengeluaran ke backend
        onSubmit() {
            if (!this.totalPengeluaran || !this.jenisPengeluaran) {
                alert("Total Pengeluaran, dan Jenis Pengeluaran harus diisi!");
                return;
            }

            const data = {
                pemasok_id: this.pemasokId || null,
                bahan_id: this.bahanId || null,
                total_pengeluaran: this.totalPengeluaran,
                tanggal: this.tanggalPengeluaran,
                keterangan: this.keterangan,
                jenis_pengeluaran: this.jenisPengeluaran
            };

            axios.post("http://localhost:50/pengeluaran", data)
                .then(response => {
                    alert('Data Pengeluaran berhasil ditambahkan!');
                    console.log(response.data);
                    // Reset form atau melakukan tindakan lainnya
                    this.pemasokId = '';
                    this.bahanId = '';
                    this.totalPengeluaran = '';
                    this.tanggalPengeluaran = '';
                    this.keterangan = '';
                    this.jenisPengeluaran = '';
                })
                .catch(error => {
                    console.error("Terjadi kesalahan saat mengirim data:", error);
                });
        }
    },
};
</script>
