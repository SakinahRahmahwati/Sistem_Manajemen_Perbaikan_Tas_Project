<template>
  <div class="content">
    <div class="container-fluid">
      <div class="row">
        <div class="card" style="width: 80%;">
          <div class="card-header">
            <h4 class="card-title">Daftar Pengguna Baru</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="register">
              <!-- Username -->
              <div class="row">
                <div class="col-md-2 pr-1">
                  <div class="form-group">
                    <label for="username">Username *</label>
                  </div>
                </div>
                <div class="col-md-10">
                  <div class="form-group">
                    <input type="text" class="form-control" id="username" v-model="username" required />
                  </div>
                </div>
              </div>

              <!-- Nama Pengguna -->
              <div class="row">
                <div class="col-md-2 pr-1">
                  <div class="form-group">
                    <label for="nama_pengguna">Nama Pengguna *</label>
                  </div>
                </div>
                <div class="col-md-10">
                  <div class="form-group">
                    <input type="text" class="form-control" id="nama_pengguna" v-model="nama_pengguna" required />
                  </div>
                </div>
              </div>

              <!-- Password -->
              <div class="row">
                <div class="col-md-2 pr-1">
                  <div class="form-group">
                    <label for="password">Password *</label>
                  </div>
                </div>
                <div class="col-md-10">
                  <div class="form-group">
                    <div class="input-group">
                      <input :type="passwordVisible ? 'text' : 'password'" class="form-control" id="password"
                        v-model="password" required />
                      <div class="input-group-append">
                        <button type="button" class="btn btn-outline-secondary" @click="togglePasswordVisibility">
                          <i :class="passwordVisible ? 'fa fa-eye-slash' : 'fa fa-eye'"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- No Telpom -->
              <div class="row">
                <div class="col-md-2 pr-1">
                  <div class="form-group">
                    <label for="no_telp">No Telp *</label>
                  </div>
                </div>
                <div class="col-md-10">
                  <div class="form-group">
                    <input type="text" class="form-control" id="no_telp" v-model="no_telp" required />
                  </div>
                </div>
              </div>

              <!-- Role -->
              <div class="row">
                <div class="col-md-2 pr-1">
                  <div class="form-group">
                    <label for="role">Role *</label>
                  </div>
                </div>
                <div class="col-md-10">
                  <div class="form-group">
                    <select id="role" class="form-control" v-model="role" required>
                      <option value="Admin">Admin</option>
                      <option value="Kepala Toko">Kepala Toko</option>
                      <option value="Staff">Staff</option>
                    </select>
                  </div>
                </div>
              </div>

              <button type="submit" class="btn btn-info btn-fill pull-right">Daftar</button>
              <div class="clearfix"></div>
            </form>
            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
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
      username: '',
      password: '',
      nama_pengguna: '',
      no_telp: '',
      role: '',
      errorMessage: '',
      passwordVisible: false,  // Mengontrol visibilitas password
    };
  },
  methods: {
    async register() {
      try {
        const userData = {
          username: this.username,
          nama_pengguna: this.nama_pengguna,
          no_telp: this.no_telp,
          password: this.password,
          role: this.role
        };

        console.log('Sending data:', userData);  // Log data yang dikirim

        const response = await axios.post('http://localhost:50/kelola_akun', userData);
        console.log('Response:', response);  // Log response

        this.$router.push('/daftarpengguna');
      } catch (error) {
        console.error(error);  // Log error
        this.errorMessage = error.response?.data?.error || 'Gagal mendaftar. Pastikan semua field benar.';
      }
    },
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible;
    }
  }
};
</script>
