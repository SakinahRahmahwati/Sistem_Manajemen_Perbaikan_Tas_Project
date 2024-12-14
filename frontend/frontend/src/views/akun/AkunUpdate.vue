<template>
    <div class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="card" style="width: 80%;">
                    <div class="card-header">
                        <h4 class="card-title">Edit Akun</h4>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="onUpdate">
                            <!-- Username -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_username">Username</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="edit_username"
                                            v-model="edit_username" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Nama Pengguna -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_namaPengguna">Nama Pengguna</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="edit_namaPengguna"
                                            v-model="edit_namaPengguna" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Telephone -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_telpPengguna">No Telephone</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="edit_telpPengguna"
                                            v-model="edit_telpPengguna" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Role -->
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label for="edit_role">Role *</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <select id="edit_role" class="form-control" v-model="edit_role" required>
                                            <option value="Admin">Admin</option>
                                            <option value="Kepala Toko">Kepala Toko</option>
                                            <option value="Staff">Staff</option>
                                        </select>
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
            edit_username: '',
            edit_namaPengguna: '',
            edit_telpPengguna: '',
            edit_role: ''
        };
    },

    mounted() {
        const pengguna_id = this.$route.params.id;
        this.getPengguna(pengguna_id);
    },

    methods: {
        getPengguna(pengguna_id) {
            axios.get(`http://localhost:50/kelola_akun?pengguna_id=${pengguna_id}`)
                .then(response => {
                    // console.log('Response:', response);
                    const pengguna = response.data; // Ambil data pengguna (asumsikan array)
                    this.edit_username = pengguna.username;
                    this.edit_namaPengguna = pengguna.nama_pengguna;
                    this.edit_telpPengguna = pengguna.no_telp;
                    this.edit_role = pengguna.role;
                })
                .catch(error => {
                    console.error('Error fetching pengguna data:', error);
                });
        },

        onUpdate() {
            const pengguna_id = this.$route.params.id; // Mendapatkan ID dari URL
            const updatedData = {
                pengguna_id: pengguna_id,
                username: this.edit_username,
                nama_pengguna: this.edit_namaPengguna,
                no_telp: this.edit_telpPengguna,
                role: this.edit_role
            };

            axios.put(`http://localhost:50/kelola_akun?pengguna_id=${pengguna_id}`, updatedData, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    alert('Data berhasil diperbarui!', response.data);
                    this.$router.push({ name: 'akunview' });
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