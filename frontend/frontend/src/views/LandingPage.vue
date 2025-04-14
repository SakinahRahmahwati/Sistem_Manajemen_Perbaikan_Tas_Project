<template>
    <div>
        <!-- Navbar Section -->
        <nav class="navbar navbar-expand-lg navbar-light fixed-top">
            <div class="container">
                <a class="navbar-brand" href="#">
                    <img src="../assets/logo.png" alt="BizLand Logo" style="height: 50px;">
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                    aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        <!-- <li class="nav-item">
                            <a class="nav-link" href="#home">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#about">About</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#services">Services</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#portfolio">Portfolio</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#team">Team</a>
                        </li> -->
                        <!-- <li class="nav-item">
                            <router-link to="/login" class="btn btn-primary btn-fill pull-right">Login</router-link>
                        </li> -->
                    </ul>
                </div>
            </div>
        </nav>

        <!-- Hero Section -->
        <section class="hero-section" id="home">
            <div class="container text-center">
                <h1 class="display-4 font-weight-bold">Welcome to Dian Tas</h1>
                <p class="lead">Sistem Manajemen Perbaikan Dian Tas yang dirancang untuk mengelola seluruh proses
                    perbaikan tas secara efektif dan efisien.</p>
                <!-- <div class="d-flex justify-content-center">
                    <button @click="scrollToSection('get-started')" class="btn btn-primary btn-lg mx-2">Get
                        Started</button>
                </div> -->
                <div class="d-flex justify-content-center">
                    <router-link to="/login" class="btn btn-primary btn-fill pull-right">Login</router-link>
                </div>
            </div>
        </section>

        <!-- Get Started Section -->
        <!-- <section id="get-started" class="py-5">
            <div class="container text-center">
                <h2>Get Started</h2>
                <p>Learn more about our services and how we can help you achieve your goals.</p>
            </div>
        </section> -->
    </div>
</template>

<script>
export default {
    methods: {
        // Method to scroll to specific section
        scrollToSection(sectionId) {
            const section = document.getElementById(sectionId);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth' });
            }
        }
    }
}
</script>

<style scoped>
/* Navbar Styling */
.navbar {
    background-color: #f5dd42;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
    font-weight: bold;
    font-size: 1.8rem;
    color: #007bff;
}

.navbar-nav {
    margin-left: auto;
    /* Membuat navbar menjauh dari kiri */
}

.nav-item .nav-link {
    color: #007bff;
    font-size: 1.2rem;
    padding-right: 20px;
    /* Menambahkan jarak antara item */
}

.nav-item .nav-link:hover {
    color: #0056b3;
}

.hero-section {
    background-image: url('../assets/foto.jpg');
    /* Ganti dengan gambar latar belakang yang sesuai */
    background-size: cover;
    background-position: center;
    color: white;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.hero-section h1 {
    font-size: 4rem;
    font-weight: 700;
}

.hero-section p {
    font-size: 1.25rem;
    margin-bottom: 20px;
}

.hero-section .btn {
    font-size: 1.25rem;
    padding: 15px 30px;
}

#get-started {
    background-color: #f4f4f4;
    padding: 50px 0;
}

#get-started h2 {
    font-size: 2.5rem;
}

#get-started p {
    font-size: 1.1rem;
    color: #555;
}
</style>