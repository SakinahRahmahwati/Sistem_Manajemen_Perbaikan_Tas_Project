<template>
    <div class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="card" style="width: 80%;">
                    <div class="card-header">
                        <h4 class="card-title">Edit Pelanggan</h4>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="onUpdate">
                            <!-- Nama Pelanggan -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_namaPelanggan">Nama Pelanggan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="edit_namaPelanggan"
                                            v-model="edit_namaPelanggan" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Alamat -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_alamatPelanggan">Alamat</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="edit_alamatPelanggan"
                                            v-model="edit_alamatPelanggan" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Telephone -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_telpPelanggan">No Telephone</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="edit_telpPelanggan"
                                            v-model="edit_telpPelanggan" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Email -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_emailPelanggan">Email</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="email" class="form-control" id="edit_emailPelanggan"
                                            v-model="edit_emailPelanggan" required>
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
            edit_namaPelanggan: '',
            edit_alamatPelanggan: '',
            edit_telpPelanggan: '',
            edit_emailPelanggan: ''
        };
    },

    mounted() {
        const pelanggan_id = this.$route.params.id; // Mendapatkan ID dari URL
        this.getPelanggan(pelanggan_id); // Mengambil data pelanggan berdasarkan ID
    },

    methods: {
        getPelanggan(id) {
            axios.get(`http://localhost:50/pelanggan?id=${id}`)
                .then(response => {
                    // console.log('Response:', response);
                    const pelanggan = response.data[0]; // Ambil data pelanggan (asumsikan array)
                    this.edit_namaPelanggan = pelanggan.nama;
                    this.edit_alamatPelanggan = pelanggan.alamat;
                    this.edit_telpPelanggan = pelanggan.telepon;
                    this.edit_emailPelanggan = pelanggan.email;
                })
                .catch(error => {
                    console.error('Error fetching pelanggan data:', error);
                });
        },

        onUpdate() {
            const pelanggan_id = this.$route.params.id; // Mendapatkan ID dari URL
            const updatedData = {
                nama: this.edit_namaPelanggan,
                alamat: this.edit_alamatPelanggan,
                telepon: this.edit_telpPelanggan,
                email: this.edit_emailPelanggan
            };

            axios.put(`http://localhost:50/pelanggan?id=${pelanggan_id}`, updatedData, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    alert('Data berhasil diperbarui!', response.data);
                    this.$router.push({ name: 'pelanggan' });
                    // Redirect atau lakukan tindakan lain setelah pembaruan
                })
                .catch(error => {
                    console.error('Terjadi kesalahan saat memperbarui data:', error);
                    alert('Terjadi kesalahan saat memperbarui data. Silakan coba lagi.');
                });
        }
    }
};
</script>