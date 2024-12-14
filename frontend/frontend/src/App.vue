<template>
  <div v-if="$route.path !== '/login' && $route.path !== '/'">
    <div class="wrapper">
      <SideBar :role="userRole"></SideBar>
      <div class="main-panel">
        <NavWeb />
        <router-view />
        <FooterWeb />
      </div>
    </div>
  </div>
  <div v-else>
    <router-view />
  </div>
</template>

<script>
import FooterWeb from './components/FooterWeb.vue';
import NavWeb from './components/NavWeb.vue';
import SideBar from './components/SideBar.vue';

export default {
  name: 'App',
  components: {
    FooterWeb,
    NavWeb,
    SideBar,
  },
  data() {
    return {
      userRole: '', // Variabel untuk menyimpan role user
    };
  },
  created() {
    this.setUserRole(); // Tentukan userRole saat komponen dibuat
    console.log('User Role Set on Created Hook:', this.userRole);
  },
  watch: {
    '$route.path'() {
      this.setUserRole();
    },
  },
  methods: {
    setUserRole() {
      // Ambil role dari localStorage menggunakan kunci 'role'
      const storedRole = localStorage.getItem('role');

      if (!storedRole) {
        console.warn(
          "Role not found in localStorage. Defaulting to 'Guest'."
        );
      }

      // Set userRole ke nilai dari localStorage atau default 'Guest'
      this.userRole = storedRole || 'Guest';
      this.isLoading = false;

      console.log('User role set to:', this.userRole); // Debugging
    },

  },
};
</script>
