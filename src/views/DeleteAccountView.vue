<script>
import { RouterLink } from "vue-router";
export default {

    data() {
        return {
            csrf_token:"",
            deleted:false,
            message: "Account Deleted"
        };
    },

    created(){
      this.getCsrfToken();
      //this.deleteAccount();
    },

    methods:{

    getCsrfToken(){
                let self = this;
                fetch('/api/csrf-token')
                    .then((response) => response.json())
                    .then((res) => {
                        console.log(res);
                        this.csrf_token = res.csrf_token;
                        self.deleteAccount();
                        
                    });
            },
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
                     }
                                 
                  }
              });
                
            }       
      },
        deleteAccount(){
          
          console.log("ABOUT TO DELETE ACCOUNT MY ACCOUNT");
          
          
          let text = "Are you sure you want to delete your account \n Either OK or Cancel.";
          if (confirm(text) == true) {
            text = "You pressed OK!";
            console.log(text);
            console.log(`CSRF TOKEN IS ${this.csrf_token}  THAT`)
            
            let user = localStorage.getItem("user_id");
            let token = localStorage.getItem("jwt_token");
            let data = {"user_id":user}

            fetch("/api/users/delete", { method: 'POST', body:JSON.stringify(data), headers: {'Content-Type': 'application/json','X-CSRFToken': this.csrf_token,'Authorization':`Bearer ${token}`} })
              .then((response) => response.json())
              .then((res) => {
                  console.log( res);
                  let keys = Object.keys(res);
                  if (keys.includes("success")){ 
                    console.log(res.success); 
                    this.deleted = true; 
                    localStorage.clear();
                    this.$router.push({ name: "home"});     
                      
                  }else{
                    console.log(res)
                  }
              
              }); 

          } else {
            text = "You canceled!";
            console.log(text);
          }
        }
    }
}
</script>

<template> 
  <h1 v-if="deleted" :class="{danger:deleted}">{{message}}</h1>

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