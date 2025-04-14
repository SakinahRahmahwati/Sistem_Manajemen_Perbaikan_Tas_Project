<template>
    <div class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="card" style="width: 80%;">
                    <div class="card-header">
                        <h4 class="card-title">Pemasok Baru </h4>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="onSubmit">
                            <!-- Nama pemasok -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="namaPemasok">Nama Pemasok *</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="namaPemasok"
                                            v-model="namaPemasok" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Alamat -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="alamatPemasok">Alamat *</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="alamatPemasok"
                                            v-model="alamatPemasok" required>
                                    </div>
                                </div>
                            </div>

                            <!-- email -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="emailPemasok">Email *</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="email" class="form-control" id="emailPemasok"
                                            v-model="emailPemasok" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Telephone -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="telpPemasok">No Telpon *</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="telpPemasok"
                                            v-model="telpPemasok" required>
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
            namaPemasok: '',
            alamatPemasok: '',
            telpPemasok: '',
            emailPemasok: ''
        };
    },
    methods: {
        onSubmit() {
            if (this.namaPemasok && this.alamatPemasok && this.telpPemasok && this.emailPemasok) {
                axios.post("http://localhost:50/daftarpemasok", {
                    nama_pemasok: this.namaPemasok,
                    alamat: this.alamatPemasok,
                    telepon: this.telpPemasok,
                    email: this.emailPemasok
                }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                    .then(response => {
                        console.log('Form berhasil dikirim:', response.data);
                        alert('Data berhasil ditambahkan!');
                        // Reset form atau melakukan tindakan lainnya
                        this.namaPemasok = '';
                        this.alamatPemasok = '';
                        this.telpPemasok = '';
                        this.emailPemasok = '';
                        this.$router.push({ name: 'pemasok' });
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
