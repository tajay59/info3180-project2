<script>
import { RouterLink } from "vue-router";
export default {

    data() {
        return {
            message: "Home of United Auto Sales "
        };
    },

    created(){
      this.logout();
    },

    methods:{

      logout(){
            console.log("logout in progress"); 
             
            if(localStorage.jwt_token){
              let token = localStorage.getItem("jwt_token"); 
              fetch('/api/auth/logout',{  headers: {'Authorization':`Bearer ${token}`}})
              .then((response) => response.json())
              .then((res) => {

                  let keys = Object.keys(res);
                  if (keys.includes("message")){
                     if(res.message === "Logged out successfully"){
                        this.loggedin = false;
                        localStorage.clear();                        
                        this.$router.push({name:"home"});
                     }
                                 
                  }
              });
                
            }       
      } 
    }
}
</script>

<template> 

</template>

<style>
/* Add any component specific styles here */
/*@import '../assets/css/home.css';*/

.logoutcontainer {
  color:lightseagreen;
}

h1{
    color: lightseagreen;
  }

body{
  width: 100vw;
  height: 100vh;
}

</style>