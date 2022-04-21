<script>
import { RouterLink } from "vue-router";
export default {

    data() {
        return {
            message: "Home of United Auto Sales "
        };
    },

    created(){
      //this.logout();
    },

    method:{

      logout(){

            this.loggedin = false;

            if(localStorage.jwt_token){
                this.loggedin = false;
                localStorage.removeItem("jwt_token");
                localStorage.removeItem("user");
                localStorage.removeItem("user_id");
                location.href = '/';
            }       
      }
      ,
      test(){

          console.log("logout in progress");

      }
    }
}
</script>

<template>
    <div class="logoutcontainer">
      <h1 @loggingrule="test" > {{ message }}</h1>
    </div>
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