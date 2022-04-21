<script>
export default {
    data() {
        return {
            message: "Profile",
            csrf_token:"",
            getallresults:[], 
            user:{
            "id"         : "id",
            "username"   : "username",
            "name"       : "name", 
            "email"      : "email",
            "location"   : "location",
            "biography"  : "biography",
            "photo"      : "photo",
            "date_join"  : "date_join", 
            }
        };
    },
    
    created(){

        this.getCsrfToken();
        this.getall();
        this.getUser();
    }
    ,
    methods:{
      details(event){            
            let user  = event.target.getAttribute("name");
            console.log(`Details for ${user}`);
            location.href = `/detail/${user}`;

        },
        getCsrfToken(){
            let self = this;
            fetch('/api/csrf-token')
                .then((response) => response.json())
                .then((res) => {
                    console.log(res);
                    this.csrf_token = res.csrf_token;
                    
                });
        },
        getUser(){
          let user_id = localStorage.getItem("user_id");
          fetch(`/api/users/${user_id}`)
                .then((response) => response.json())
                .then((res) => {
                    console.log(res);
                    let keys = Object.keys(res);
                    if (keys.includes("success")){
                      let data             = res["success"]; 
                      this.user.id         = data.id;
                      this.user.username   = data.username;
                      this.user.name       = data.name; 
                      this.user.email      = data.email;
                      this.user.location   = data.location;
                      this.user.biography  = data.biography;
                      this.user.photo      = `/api/images/${data.photo}`
                      this.user.date_join  = data.date_join; 
                      
                    }

                    
                });
        },
        
        getFavourite(){
          let user = localStorage.getItem("user_id");
          let token = localStorage.getItem("jwt_token"); 
          fetch(`/api/users/${user}/favourite`, { method: 'GET', headers: { 'X-CSRFToken': this.csrf_token,'Authorization':`Bearer ${token}`} })
            .then((response) => response.json())
            .then((res) => {
                console.log( res);
                let keys = Object.keys(res);
                    if (keys.includes("favourites")){
                      let data = res["favourites"]; 
                      data.forEach((el)=>{

                        if(el.car_id == this.car.id){
                            this.favourite = true;
                        }
                      });                    
                    }
                
            }); 

      },
        getall(){
            let token = localStorage.getItem("jwt_token");
            let user = localStorage.getItem("user_id");
            fetch(`/api/users/${user}/favourites`, { method: 'GET',headers: {'Authorization':`Bearer ${token}`} })
            .then(response => response.json())
            .then(res => {
            console.log('Success:', res); 

            let keys = Object.keys(res);
            if (keys.includes("code")){
                if( res['code'] === "token_expired"){
                    localStorage.removeItem("jwt_token");
                    localStorage.removeItem("user");
                    localStorage.removeItem("user_id");
                    location.href="/"
                                    } 
            }

             
        if (keys.includes("favourites")){
                let self = this;
                let data = res["favourites"];
                // Empty array first
                self.getallresults.splice(0,self.getallresults.length);

                data.forEach((el)=>{
                    el["photo"] =`/api/images/${el["photo"]}`;
                    self.getallresults.push(el);
                });
                 
            }

            })
            .catch((error) => {
            console.error('Error:', error);
            });
        }, 
        
        searchOne(){

            let token = localStorage.getItem("jwt_token");
            fetch(`/api/search?make=${this.searchmake}&model=${this.searchmodel}`, { method: 'GET', headers: {'X-CSRFToken': this.csrf_token,'Authorization':`Bearer ${token}`} })
            .then(response => response.json())
            .then(data => {
            console.log('Success:', data); 

            let keys = Object.keys(data);
            if (keys.includes("code")){
                if( data['code'] === "token_expired"){
                    localStorage.removeItem("jwt_token");
                    localStorage.removeItem("user");
                    localStorage.removeItem("user_id");
                    location.href="/"
                                    } 
            }

            if (keys.includes("message")){
               if( data['message'] === "Login successfully"){
                   this.jwt_token = data['token'];
                   localStorage.setItem("jwt_token",this.jwt_token);
                   location.href="/"
               }  
            }

        if (keys.includes("results")){
                let self = this;
                self.getallresults.splice(0,self.getallresults.length);
                data["results"].forEach((el)=>{
                    el["photo"] =`/api/images/${el["photo"]}`;
                    self.getallresults.push(el)
                });
                 
            }

            })
            .catch((error) => {
            console.error('Error:', error);
            });

        },

        deleteAccount(){
          console.log("ABOUT TO DELETE ACCOUNT");
          console.log(`CSRF TOKEN IS ${this.csrf_token}`)
          let text = "Are you sure you want to delete your account \n Either OK or Cancel.";
          if (confirm(text) == true) {
            text = "You pressed OK!";
            console.log(text);

            
            let user = localStorage.getItem("user_id");
            let token = localStorage.getItem("jwt_token");
            let data = {"user_id":user}
            fetch(`/api/users/delete`, { method: 'POST', body:JSON.stringify(data), headers: {'Content-Type': 'application/json','X-CSRFToken': this.csrf_token,'Authorization':`Bearer ${token}`} })
              .then((response) => response.json())
              .then((res) => {
                  console.log( res);
                  let keys = Object.keys(res);
                      if (keys.includes("success")){
                        console.log(res.success); 
                        setInterval(()=>{
                          location.href = "/logout";
                        }) ,5000               
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
    <div class="usercontainer">
       <div id="profile">
         <div class="profilecard">
           
            <div id="profileimage">
              <img :src="user.photo" alt="">
                
            </div>

            <div id="profileinfo">
                <h1 id="name">{{user.name}}</h1>
                <h5 id="socialmedia">@{{user.username}}</h5>
                <p id="biography">{{user.biography}}</p>

                <div id="email">
                  <label for="emaildiv">E-mail</label>
                  <span id="emaildiv">{{user.email}}</span>
                </div>

                <div id="location"> 
                  <label for="locationdiv">Location</label>
                  <div id="locationdiv">{{user.location}}</div>
                </div>

                <div id="joined"> 
                  <label for="joineddatediv">Joined</label>
                  <span id="joineddatediv">{{user.date_join}}</span>
                </div>
                <div class="deleteaccount">
                  <button class="loginsubmit profiledeletebtn" @click="deleteAccount">Delete Account</button>
                </div>

            </div>
         </div>
       </div>
       <div id="favorited">  <h1>Cars Favourited</h1></div>
       <div id="favourites" >
         <div class="card" v-for="car in getallresults">
                <img :src="car.photo" alt="">
                <div class="description"> 
                    <div class="info">
                        <span id="left">{{car.year}} {{car.make}}</span> 
                        <span id="price"> <img id="priceicon" src="@/assets/images/tag.svg" alt="">   {{car.price.toLocaleString('en-US', {style: 'currency',  currency: 'USD',})}}</span>
                        
                    </div>
                    <div id="carmodel">
                            <p> {{car.model}}</p>
                    </div>
                    
                    <button class="submit" @click="details" :name="car.id">View more details</button>
                </div>
            </div>
       </div>
    </div>
</template>

<style>
/* Add any component specific styles here */
@import '../assets/css/profile.css';
</style>