<script>
export default {
    data() {
        return {
            csrf_token : "", 
            newuseradded:false,
            newuserprofile:"Registration Successfull",
            existmessage : "",
            alreadyexist : false,
            username:false,
            name:false,
            email:false,
            location:false,
            biography:false,
            photo:false,
            password:false,
            danger:false,
            success:false,
            error:false,
        };
    },
    created(){
        this.getCsrfToken();
    }
    ,
    methods:{
        getCsrfToken(){
            let self = this;
            fetch('/api/csrf-token')
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    self.csrf_token = data.csrf_token;
                });
        },
        submitform(){
            console.log("Registration form submitted");
            let uploadForm = document.querySelector("#registrationForm")
            let form_data = new FormData(uploadForm);
            console.log(form_data);
            //let   = document.querySelector("#");
 

            fetch('/api/register', { method: 'POST', body: form_data ,headers: {'X-CSRFToken': this.csrf_token}})
            .then(response => response.json())
            .then(res => { 
            console.log( res);
                let keys = Object.keys(res);
                    if (keys.includes("message")){
                        

                        if( res.message == "New user profile created"){ 
                            this.newuseradded = true; 
                            setTimeout(()=>{this.newuseradded = false;},5000);
                            
                        }

                       else if( res.message == "user already exist"){ 
                           this.existmessage = res.status;
                            this.alreadyexist = true; 
                            setTimeout(()=>{this.alreadyexist = false;},5000);
                             
                        }
                        else if( res.message == "Form errors"){ 
                            let data = res["errors"]
                            
                                data.forEach(element => {

                                    if(element.includes("Username")){   this.username = true; }
                                    if(element.includes("Name")){       this.name = true; }
                                    if(element.includes("email")){      this.email = true; }
                                    if(element.includes("Location")){   this.location = true; }
                                    if(element.includes("Biography")){  this.biography = true; }
                                    if(element.includes("Photo")){      this.photo = true; }
                                    if(element.includes("Password")){   this.password = true; }

                                });

                                this.error = true;
                                this.success = false;
                                this.danger = true; 

                                setTimeout(()=>{
                                    this.error      = false;
                                    this.username   = false;
                                    this.name       = false;
                                    this.email      = false;
                                    this.location   = false;
                                    this.biography  = false;
                                    this.photo      = false;
                                    this.password   = false;
                                
                                
                                },5000);
                             
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
    <div class="registercontainer"> 
        <h1 class="registertitle">Register New User</h1>
        
        <h6 v-if="newuseradded" id="newuser" class="success">{{newuserprofile}}</h6>
        <h6 v-if="alreadyexist" id="newuser" class="danger">{{existmessage}}</h6>
        
        <hr>
        <form   @submit.prevent="submitform" id="registrationForm">
            <div class="loginformitems">                 
                <input id="username" type="text" name="username" class="loginformitems__input" placeholder=" " maxlength="80">
                <label for="username" class="loginformitems__label" placeholder=" " >Username</label>
                <h6 v-if=" (username && error)"      class="danger erroritem">required!</h6>
            </div>
            <div class="loginformitems">                
                <input id="name" type="text" name="name" class="loginformitems__input" placeholder=" " maxlength="80" >
                <label for="name" class="loginformitems__label" placeholder=" " >Name</label>
                <h6 v-if=" (name && error)"      class="danger erroritem">required!</h6>
            </div>
            <div class="loginformitems">                
                <input id="email" type="email" name="email" class="loginformitems__input" placeholder=" " maxlength="80">   
                <label for="email" class="loginformitems__label" placeholder=" "  >Email</label>
                <h6 v-if="(email && error)"      class="danger erroritem">required!</h6>
            </div>
            <div class="loginformitems">                
                <input id="location" type="text" name="location" class="loginformitems__input" placeholder=" " maxlength="80">
                <label for="location" class="loginformitems__label" placeholder=" " >Location</label>
                <h6 v-if="(location && error)"      class="danger erroritem">required!</h6>
            </div>
            <div class="loginformitems biographybox">                
                <textarea name="biography" id="biography" cols="30" rows="3" class="loginformitems__input" placeholder=" " maxlength="1000"></textarea>  
                <label for="biography" class="loginformitems__label" placeholder=" " >Biography</label>       
                <h6 v-if="(biography && error)"      class="danger erroritem">required!</h6>        
            </div>
            <div class="filestyle" >                
                <input id="photo" type="file" name="photo"  placeholder=" "> 
                <h6 v-if="(photo && error)"      class="danger erroritem photoerror">required!</h6>
            </div>
            <div class="loginformitems">                
                <input id="password" type="password" name="password" class="loginformitems__input" placeholder=" " maxlength="80">
                <label for="password" name="username" class="loginformitems__label" placeholder=" ">Password</label>
                <h6 v-if="(password && error)"      class="danger erroritem">required!</h6>
            </div>

            <button id="submit" class="loginsubmit">Submit</button>

        </form>
    
    </div>
</template>

<style>
/* Add any component specific styles here */
@import '../assets/css/register.css';
</style>