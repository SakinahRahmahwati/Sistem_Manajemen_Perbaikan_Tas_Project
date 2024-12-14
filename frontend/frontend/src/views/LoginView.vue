<template>
  <div class="login-page">
    <main class="login-container">
      <div class="login-card">
        <div class="login-content">
          <img src="@/assets/image_inventory.png" alt="Illustration" class="login-illustration" />
        </div>
        <div class="login-form">
          <h2>Form Login</h2>
          <form @submit.prevent="login">
            <div class="input-group">
              <input type="text" placeholder="Username" v-model="username" required />
            </div>
            <div class="input-group password-container">
              <input :type="showPassword ? 'text' : 'password'" placeholder="Password" v-model="password" required />
              <button type="button" @click="togglePasswordVisibility" class="password-toggle-btn">
                <i :class="showPassword ? 'fa fa-eye' : 'fa fa-eye-slash'"></i>
              </button>
            </div>
            <button type="submit">Login</button>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>


<script>
import axios from 'axios';
export default {
  data() {
    return {
      username: '',
      password: '',
      showPassword: false, // Toggle password visibility
      errorMessage: '', // Untuk menampilkan pesan error
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:50/login', {
          username: this.username,
          password: this.password,
        }, {
          headers: { 'Content-Type': 'application/json' }
        });

        if (response.status === 200) {
          const { token, role } = response.data;

          localStorage.setItem('token', token);
          localStorage.setItem('role', role);
          alert('Login successful');
          this.$router.push('/dashboard');
        }
      } catch (error) {
        console.error('Login error:', error.response);
        const message = error.response?.data?.error || 'An error occurred. Please try again.';
        alert(message);
      }
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
  },
};
</script>



<style scoped>
/* Struktur Halaman */
.login-page {
  font-family: Arial, sans-serif;
  background-color: #f3f8fc;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Container */
.login-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  display: flex;
  width: 1000px;
  height: 600px;
  background-color: white;
  border-radius: 15px;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.login-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f9fafb;
}

.login-illustration {
  width: 90%;
}

/* Form */
.login-form {
  flex: 1;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

h2 {
  font-size: 32px;
  color: #333;
  margin-bottom: 30px;
}

.input-group {
  width: 100%;
  margin-bottom: 20px;
}

input {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 18px;
}

button {
  width: 100%;
  padding: 15px;
  font-size: 20px;
  background-color: #ffd600;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  outline: none; 
}

button:hover {
  background-color: #ffcb00;
}

/* Menyesuaikan Kontainer Input Password */
.password-container {
  display: flex;
  align-items: center;
  width: 100%;
  position: relative;
}

/* Menyesuaikan Styling Input Password */
.password-container input {
  padding-right: 40px;
  /* Memberikan ruang untuk ikon mata */
}

/* Tombol toggle password (ikon mata) */
.password-toggle-btn {
  background: none;
  border: none;
  color: #9da0a2;
  cursor: pointer;
  font-size: 20px;
  position: absolute;
  right: 10px;
  /* Disesuaikan untuk penataan yang lebih baik */
  top: 50%;
  transform: translateY(-50%);
  /* Menyelaraskan tombol secara vertikal */
  padding: 0;
  /* Menghilangkan ruang ekstra di sekitar tombol */
  height: 20px;
  /* Menentukan ukuran tombol agar tidak mempengaruhi layout */
  width: 20px;
  /* Menentukan ukuran tombol */
}

button.password-toggle-btn:hover {
  background-color: transparent;  /* Tombol mata tidak berubah warna saat di-hover */
}
</style>
