<template>
  <header>
    <nav class="navbar navbar-expand-lg fixed-top loginnav">  <!--   navbar-dark bg-primary  -->
      <div class="container-fluid">

        <a class="navbar-brand  logo" href="/"  >
        <h4>U A S</h4>
        <img id="logginicon" class="logginicon" src="@/assets/images/logo.svg" alt="">
        </a>

        <button
              class="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarSupportedContent"
              aria-controls="navbarSupportedContent"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
             
            <img src="@/assets/images/hamburger.svg" alt="">
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav me-auto headerlinks">

              </ul>
              <ul class="navbar-nav me-auto"> 
                <li class="nav-item">
                  <RouterLink class="nav-link  headerlinks" to="/explore">Explore</RouterLink>
                </li>
                <li class="nav-item">
                  <RouterLink class="nav-link headerlinks" to="/addcar">Add Car</RouterLink>
                </li>
                <li class="nav-item">
                  <RouterLink class="nav-link headerlinks" to="/profile">My Profile</RouterLink>
                </li>
                
              </ul>
              <ul  class="navbar-nav ">
                <li v-if="!loggedin" class="nav-item headerlinks">
                  <RouterLink class="nav-link headerlinks" to="/register">Register</RouterLink>
                </li>

                <li class="nav-item  loginlogout">
                  <RouterLink v-if="loggedin" class="nav-link headerlinks" to="/logout" @click.prevent="logout" >   <!-- @click.prevent="logout" -->                
                    <img class="logginicon" src="@/assets/images/logout.svg" alt="">
                    <label for="logginicon"> Logout</label>
                  </RouterLink>

                  <RouterLink v-else class="nav-link headerlinks" to="/login">                  
                    <img id="logginicon" class="logginicon" src="@/assets/images/login.svg" alt="">
                    <label for="logginicon">Login</label>
                  </RouterLink>
                </li>

              </ul>
        </div>

      </div>
    </nav>
  </header>
</template>

<script>
import { RouterLink } from "vue-router";
export default {
    data() {
        return {
            loggedin : false 
        };
    },
    created(){
      this.checkloggedinstatus();
    },
    methods:{

      checkloggedinstatus(){
        setInterval(()=> {
          if(localStorage.jwt_token){
            this.loggedin = true;
          }
          else{
            this.loggedin = false;
          }
            
          }, 100);
        
    },
   
    logout(){

      this.loggedin = false;
      this.$emit('loggingrule');
      console.log('just sent emit');

        /*
        if(localStorage.jwt_token){
              this.loggedin = false;
              localStorage.removeItem("jwt_token");
              localStorage.removeItem("user");
              localStorage.removeItem("user_id");
              location.href = '/';
            } 
          */
        
        },
    
    
    
    }
}
</script>

<style>
/* Add any component specific styles here */
.logginicon{
  width: 30px;
  height: auto;
}

 .logo, .headerlinks{
   display: flex;
   flex-direction: row-reverse;
   gap:2px;
     font-size: 15px;
     color: lightseagreen;
    
 }
 
 .logo:hover, .headerlinks:hover{    
  color: rgba(32, 178, 171, 0.678);
  
 }

 .headerlinks{
   display: flex;
   flex-direction: column;
   justify-content: center;
   align-items: center;
 }

 .headerlinks > label{
   cursor: pointer;
   font-size: 10px;
 }


.loginlogout{
  display: flex;
  width: 100%;
  justify-content: space-around;
}
</style>