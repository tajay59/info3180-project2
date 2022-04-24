<script>
export default {
    data() {
        return {
            csrf_token :"",
            jwt_token: "",
            message:"",
            displayMessage:false,
            danger:false,
            success:false,
            error:false,
            username:false,
            password:false,

            
        };
    },
    created(){
        this.getCsrfToken();  // GET TOKEN FROM FLASK API
    }
    ,
    methods:{

        getCsrfToken(){
            
            fetch('/api/csrf-token')
                .then((response) => response.json())
                .then((data) => {
                    this.csrf_token = data.csrf_token;
                });
        },


        userLogin(){
            // COLLECT USER INPUT FROM LOGIN FORM THEN POST TO FLASK API
            let loginForm = document.querySelector("#loginForm")
            let form_data = new FormData(loginForm);

            fetch('/api/auth/login', { method: 'POST', body: form_data,headers: {'X-CSRFToken': this.csrf_token} })//
                .then(response => response.json())
                .then(data => {
                        let keys = Object.keys(data);
                        if (keys.includes("message")){
                            console.log(data);
                            if( data['message'] === "Login successfully"){ 
                                this.jwt_token = data['token'];
                                this.message = "Logged in sucessfully";
                                this.displayMessage = true;
                                this.success = true;
                                this.danger = false;
                                // STORE RETURN USERNAME, ID AND JWT TOKEN TO LOCALSTORAGE FOR FUTURE API REQUESTS
                                localStorage.setItem("jwt_token",this.jwt_token);  
                                localStorage.setItem("username",data['user']);  
                                localStorage.setItem("user_id",data['user_id']);    
                                
                                // REDIRECT TO EXPLORE PAGE SINCE LOGIN IS SUCCESSFUL 
                                this.$router.push("/explore");
                            }
                            else if(data['message'] === "User does not exist"){
                                this.message = "User does not exist";
                                this.displayMessage = true;
                                this.success = false;
                                this.danger = true;
                                setTimeout(()=>{this.displayMessage = false;},5000);
                            } 
                            else if(data['message'] === "Form errors"){
                                let res = data["errors"]
                                
                                res.forEach(element => {

                                    if(element.includes("Username")){   this.username = true; }
                                    if(element.includes("Password")){   this.password = true; }

                                });

                                this.error = true;
                                this.success = false;
                                this.danger = true; 

                                setTimeout(()=>{
                                    this.error      = false;
                                    this.username   = false;
                                    this.password   = false;
                                
                                
                                },5000);
                            }                             
                            else{
                                this.message = "Unable to login";
                                this.displayMessage = true;
                                this.success = false;
                                this.danger = true;
                                setTimeout(()=>{this.displayMessage = false;},5000);
                            }
                        }
                })
                .catch((error) => {
                console.error('Error:', error);
            });

        }
    }
}
</script>

<template>
    <div class="logincontainer">

        <h1>Login</h1>
        <div v-if="displayMessage" :class="{dangermessage: danger, successmessage: success}" >
            <h4  >{{message}}</h4>
        </div>        
        <hr>
        
        <form  id="loginForm" @submit.prevent="userLogin">

                <div class="loginformitems">                    
                    <input type="text" name="username" class="loginformitems__input" placeholder=" " maxlength="20">
                    <label for="username" class="loginformitems__label">Username</label>
                    <h6 v-if="(username && error)"      class="danger erroritem">required!</h6>
                </div>

                <div class="loginformitems">                    
                    <input type="password" name="password" class="loginformitems__input" placeholder=" " maxlength="40">
                    <label for="password" class="loginformitems__label">Password</label>
                    <h6 v-if="(password && error)"      class="danger erroritem">required!</h6>
                </div>

                <button id="submit" class="loginsubmit">Sign In</button>

        </form>
        


       
    </div>
</template>

<style>
/* Add any component specific styles here */
@import "../assets/css/login.css";
</style>