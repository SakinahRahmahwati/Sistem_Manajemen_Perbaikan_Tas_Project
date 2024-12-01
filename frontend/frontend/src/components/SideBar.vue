<template>
    <div class="sidebar" data-color="white">
        <div class="sidebar-wrapper">
            <div class="logo">
                <router-link to="/" class="simple-text">
                    <img :src="require('@/assets/logo.png')" alt="Logo" width="80" />
                </router-link>
            </div>
            <ul class="nav">
                <li class="nav-item" :class="{ active: isActive('/dashboard') || isActive('/') }">
                    <router-link class="nav-link" to="/dashboard">
                        <i class="bi bi-house-door-fill"></i>
                        <p>Dashboard</p>
                    </router-link>
                </li>
                <li class="nav-item" :class="{ active: isActive('/jenislayanan') }">
                    <router-link class="nav-link" to="/jenislayanan">
                        <i class="bi bi-gear"></i>
                        <p>Jenis Layanan</p>
                    </router-link>
                </li>
                <li class="nav-item" :class="{ active: isActive('/material') }">
                    <router-link class="nav-link" to="/material">
                        <i class="bi bi-list-ul"></i>
                        <p>Material</p>
                    </router-link>
                </li>
                <li class="nav-item" :class="{ active: isActive('/pelanggan') || isActive('/pelanggan/insert') || isActive('/pelanggan/update') }">
                    <router-link class="nav-link" to="/pelanggan">
                        <i class="bi bi-people-fill"></i>
                        <p>Pelanggan</p>
                    </router-link>
                </li>
                <li class="nav-item" :class="{ active: isActive('/pemasok') || isActive('/pemasok/insert') }">
                    <router-link class="nav-link" to="/pemasok">
                        <i class="bi bi-boxes"></i>
                        <p>Pemasok</p>
                    </router-link>
                </li>
                <li class="nav-item" :class="{ active: isActive('/perbaikan') || isActive('/perbaikan/insert') }">
                <router-link class="nav-link" to="/perbaikan">
                    <i class="bi bi-briefcase-fill"></i>
                    <p>Perbaikan Tas</p>
                </router-link>
            </li>
                <!-- Dropdown Menu for Perbaikan Tas -->
                <!-- <li class="nav-item dropdown" :class="{ active: isDropdownActive('/perbaikan') }">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="bi bi-briefcase-fill"></i>
                        <p>Perbaikan Tas</p>
                    </a>
                    <ul class="dropdown-menu">
                        <li :class="{ active: isActive('/perbaikan') }">
                            <router-link class="dropdown-item" to="/perbaikan">
                                List Perbaikan
                            </router-link>
                        </li>
                        <li :class="{ active: isActive('/perbaikan/insert') }">
                            <router-link class="dropdown-item" to="/perbaikan/insert">
                                Perbaikan Baru
                            </router-link>
                        </li>
                    </ul>
                </li> -->
                <li class="nav-item" :class="{ active: isActive('/pengeluaran/insert') }">
                    <router-link class="nav-link" to="/pengeluaran/insert">
                        <i class="bi bi-box-arrow-up"></i>
                        <p>Pengeluaran</p>
                    </router-link>
                </li>
                <li class="nav-item" :class="{ active: isActive('/laporankeuangan') || isActive('/pengeluaran') }">
                    <router-link class="nav-link" to="/laporankeuangan">
                        <i class="bi bi-cash-coin"></i>
                        <p>Laporan Keuangan</p>
                    </router-link>
                </li>
                <li class="nav-item" :class="{ active: isActive('') }">
                    <router-link class="nav-link" to="#">
                        <i class="bi bi-person-fill"></i>
                        <p>Akun</p>
                    </router-link>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    methods: {
        isActive(route) {
            return this.$route.path === route;
        },
        isDropdownActive(baseRoute) {
            return this.$route.path.startsWith(baseRoute);
        },
    },
};
</script>

<style scoped>
/* Tambahkan gaya untuk dropdown agar sesuai */
.nav-item.dropdown .dropdown-menu {
    margin-left: 20px;
    border: none;
    background-color: #f8f9fa; /* Sesuaikan warna sesuai tema */
}
.dropdown-item.active {
    background-color: #e9ecef; /* Warna submenu aktif */
    font-weight: bold;
}
</style>
