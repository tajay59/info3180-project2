<script>
import { RouterLink } from "vue-router";
export default {
    data() {
        return {
            loggedin:false
        };
    },
    created(){
      this.checkloggedin();
      console.log(`LOGGEDIN SATE ${this.loggedin}`)
    },
    methods:{
      checkloggedin(){
        this.loggedin = false;
        if(localStorage.jwt_token){ 
          this.loggedin = true;
        }
        
    }
}
}
</script>

<template>
    <div class="homecontainer">
      <div class="homeinfo"> 
        <div class="homedetails">
            <div class="hometitles">
              <h1> Buy and Sell </h1>
              <h1> Cars Online </h1>
            </div>
            <p class="homedescription"> <span>U</span>nited <span>A</span>uto <span>S</span>ales   provides the fastest, easiest and most user friendly way to buy or sell cars online. Find a Great Price on the Vehicle You Want</p>
            <div class="homebuttons">

              <RouterLink  v-if="!loggedin" class="nav-link " to="/register">                  
                    <button >Register</button>
              </RouterLink>
              <RouterLink  v-if="!loggedin" class="nav-link " to="/login">                  
                    <button  >Login</button>
              </RouterLink>
              
            </div>
        </div>
        

      </div>

      <div class="homeimage">
        <img src="@/assets/images/home.jpg" alt="">
      </div>
       
    </div>
</template>

<style>
/* Add any component specific styles here */
@import '../assets/css/home.css';
</style>