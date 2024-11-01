<template>
  
  <div class="wrapper">
    <SideBar></SideBar>
         <div class="main-panel">
          <NavWeb/>
          <router-view/>
             <FooterWeb/>
         </div>
     </div>
</template>

<script>
//components
import FooterWeb from './components/FooterWeb.vue';
import NavWeb from './components/NavWeb.vue';
import SideBar from './components/SideBar.vue';


export default {
  name: 'App',
  components:{
    FooterWeb,
    NavWeb,
    SideBar,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
