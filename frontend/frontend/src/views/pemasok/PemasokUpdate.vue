<template>
    <div class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="card" style="width: 80%;">
                    <div class="card-header">
                        <h4 class="card-title">Edit Pemasok</h4>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="onUpdate">
                            <!-- Nama Pemasok -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_namaPemasok">Nama Pemasok</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="edit_namaPemasok"
                                            v-model="edit_namaPemasok" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Alamat -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_alamatPemasok">Alamat</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="edit_alamatPemasok"
                                            v-model="edit_alamatPemasok" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Telephone -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_telpPemasok">No Telephone</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="edit_telpPemasok"
                                            v-model="edit_telpPemasok" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Email -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_emailPemasok">Email</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="email" class="form-control" id="edit_emailPemasok"
                                            v-model="edit_emailPemasok" required>
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
            edit_namaPemasok: '',
            edit_alamatPemasok: '',
            edit_telpPemasok: '',
            edit_emailPemasok: ''
        };
    },

    mounted() {
        const pemasok_id = this.$route.params.id; // Mendapatkan ID dari URL
        this.getPemasok(pemasok_id); // Mengambil data Pemasok berdasarkan ID
    },

    methods: {
        getPemasok(id) {
            axios.get(`http://localhost:50/pemasok?id=${id}`)
                .then(response => {
                    // console.log('Response:', response);
                    const pemasok = response.data[0]; // Ambil data Pemasok (asumsikan array)
                    this.edit_namaPemasok = pemasok.nama_pemasok;
                    this.edit_alamatPemasok = pemasok.alamat;
                    this.edit_telpPemasok = pemasok.telepon;
                    this.edit_emailPemasok = pemasok.email;
                })
                .catch(error => {
                    console.error('Error fetching Pemasok data:', error);
                });
        },

        onUpdate() {
            const pemasok_id = this.$route.params.id; // Mendapatkan ID dari URL
            const updatedData = {
                nama_pemasok: this.edit_namaPemasok,
                alamat: this.edit_alamatPemasok,
                telepon: this.edit_telpPemasok,
                email: this.edit_emailPemasok
            };

            axios.put(`http://localhost:50/pemasok?id=${pemasok_id}`, updatedData, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    alert('Data berhasil diperbarui!', response.data);
                    this.$router.push({ name: 'pemasok' });
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