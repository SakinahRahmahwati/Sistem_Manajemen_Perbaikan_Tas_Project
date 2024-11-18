<template>
    <div class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="card" style="width: 80%;">
                    <div class="card-header">
                        <h4 class="card-title">Pelanggan Baru</h4>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="onSubmit">
                            <!-- Nama Pelanggan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form  -group">
                                        <label for="namaPelanggan">Nama Pelanggan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="namaPelanggan"
                                            v-model="namaPelanggan" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Alamat -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="alamatPelanggan">Alamat</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="alamatPelanggan"
                                            v-model="alamatPelanggan" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Telephone -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="telpPelanggan">No Telephone</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="telpPelanggan"
                                            v-model="telpPelanggan" required>
                                    </div>
                                </div>
                            </div>

                            <!-- email -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="emailPelanggan">Email</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="email" class="form-control" id="emailPelanggan"
                                            v-model="emailPelanggan" required>
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
            namaPelanggan: '',
            alamatPelanggan: '',
            telpPelanggan: '',
            emailPelanggan: ''
        };
    },
    methods: {
        onSubmit() {
            if (this.namaPelanggan && this.alamatPelanggan && this.telpPelanggan && this.emailPelanggan) {
                axios.post("http://localhost:50/daftarpelanggan", {
                    nama: this.namaPelanggan,
                    alamat: this.alamatPelanggan,
                    telepon: this.telpPelanggan,
                    email: this.emailPelanggan,
                    tanggal_registrasi: new Date().toISOString() // Contoh nilai untuk tanggal
                }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                    .then(response => {
                        console.log('Form berhasil dikirim:', response.data);
                        alert('Data berhasil ditambahkan!');
                        // Reset form atau melakukan tindakan lainnya
                        this.namaPelanggan = '';
                        this.alamatPelanggan = '';
                        this.telpPelanggan = '';
                        this.emailPelanggan = '';
                        this.$router.push({ name: 'pelanggan' });
                    })
                    .catch(error => {
                        console.error('Terjadi kesalahan saat mengirim form:', error);
                    });
            } else {
                alert('Silakan isi semua kolom yang wajib.');
            }
        }

    }
}
</script>
