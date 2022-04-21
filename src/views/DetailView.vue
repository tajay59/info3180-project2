<script>
export default {
    data() {
        return {
            message: "Detail",
            csrf_token:"",
            id:this.$route.params.id,
            favourite:false,
            updateFav:false,
            car:{
               
            "id"                : 0,
            "description"       : "Car.description",
            "make"              : "Car.make",
            "model"             : "Car.model",
            "colour"            : "Car.colour",
            "year"              : "Car.year",
            "transmission"      : "Car.transmission",
            "car_type"          : "Car.car_type",
            "price"             : "Car.price",
            "photo"             : "@/assets/images/bk.jpg",
            "user_id"           : "Car.user_id"
                
            }
        };
    },
    created(){
      this.getCsrfToken();
      this.getCar();
      this.checkFavStatus();
      
    }, 
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
      getCar(){
        
        fetch(`/api/cars/${this.id}`)
            .then((response) => response.json())
            .then((res) => {
             
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

            if (keys.includes("message")){
              console.log(res["message"]);
            }

        if (keys.includes("success")){
            let data              = res["success"]; 
            this.car.id           = data.id;
            this.car.description  = data.description;
            this.car.make         = data.make;
            this.car.model        = data.model;
            this.car.colour       = data.colour;
            this.car.year         = data.year;
            this.car.transmission = data.transmission;
            this.car.car_type     = data.car_type;
            this.car.price        = data.price;
            this.car.photo        = `/api/images/${data.photo}`;
            this.car.user_id      = data.user_id; 
                 
            }
                 
            });
      },

      sendfav(event){
        let fav  = event.target.getAttribute("name");
        console.log(`Favourite request ${fav}`);
        if(fav === "fav"){
          let user = localStorage.getItem("user_id");
          let token = localStorage.getItem("jwt_token");
          let data = {"car_id":this.car.id,"user_id":parseInt(user)};
          fetch(`/api/cars/${this.car.id}/favourite`, { method: 'POST', body:JSON.stringify(data), headers: {'Content-Type': 'application/json','X-CSRFToken': this.csrf_token,'Authorization':`Bearer ${token}`} })
            .then((response) => response.json())
            .then((res) => {
                console.log( res);
                let keys = Object.keys(res);
                    if (keys.includes("success")){
                      this.favourite = true;                   
                    }
                
            }); 
        } 
      }
      ,
      deletefav(event){
        let fav  = event.target.getAttribute("name"); 
        if(fav === "notfav"){
          let user = localStorage.getItem("user_id");
          let token = localStorage.getItem("jwt_token");
          let data = {"car_id":this.car.id,"user_id":parseInt(user)};
          fetch(`/api/cars/${this.car.id}/favourite/delete`, { method: 'POST', body:JSON.stringify(data), headers: {'Content-Type': 'application/json','X-CSRFToken': this.csrf_token,'Authorization':`Bearer ${token}`} })
            .then((response) => response.json())
            .then((res) => {
                console.log( res);
                let keys = Object.keys(res);
                    if (keys.includes("success")){
                      this.favourite = false;                   
                    }
                
            }); 
        } 
      }
      ,
      
      getFavourite(){
        if(this.updateFav === false){

          let user = localStorage.getItem("user_id");
          let token = localStorage.getItem("jwt_token"); 
          fetch(`/api/users/${user}/favouriteid`, { method: 'GET', headers: { 'X-CSRFToken': this.csrf_token,'Authorization':`Bearer ${token}`} })
            .then((response) => response.json())
            .then((res) => {
                console.log( res);
                let keys = Object.keys(res);
                    if (keys.includes("favourites")){
                      let data = res["favourites"]; 
                      data.forEach((el)=>{

                        if(el.car_id == this.car.id){
                          console.log("GOT A FAVOURITE");
                            this.favourite = true;
                            
                        }
                      });  
                      this.updateFav = true;                  
                    }
                    else if(keys.includes("message")){
                        let data = res["message"]; 
                        console.log(data);
                        this.updateFav = true;
                    }
                
            }); 

        }
          

      },

      checkFavStatus(){            
          setInterval(this.getFavourite ,1000);        
    }
    }
}
</script>

<template>
    <div class="container">
      <div id="carprofile">
         <div class="carcard">
           
           <div id="carimage">
             <img :src="car.photo" alt="">
               
           </div>
           <div id="carprofileinfo">
             <div class="carinformation">
                <h1 id="name">{{car.year}} {{car.make}}</h1> 
                <h4>{{car.model}}</h4>
                <p id="cardescription">{{car.description}}</p>

                <div class="params">
                    <div id="paramsitem">
                      <label for="colour">Color</label>
                      <span id="colour">{{car.colour}}</span>
                    </div>

                    <div id="paramsitem"> 
                      <label for="bodytype">Body Type</label>
                      <span id="bodytype">{{car.car_type}}</span>
                    </div>

                 

                    <div id="paramsitem"> 
                      <label for="price">Price</label>
                      <span id="price">{{car.price}}</span>
                    </div>

                    <div id="paramsitem"> 
                      <label for="transmission">transmission</label>
                      <span id="transmission">{{car.transmission}}</span>
                    </div>
                </div>
             </div>
             
             
             <div id="contact">
               <button> <span class="emailowner">Email Owner</span> </button>
               <img id="favicon" v-if="favourite" src="@/assets/images/favorite1.svg" alt="" name="notfav" @click.prevent="deletefav">
               <img id="favicon" v-else src="@/assets/images/favorite.svg" alt="" name="fav" @click.prevent="sendfav">

             </div>

           </div>
         </div>
       </div>
    </div>
</template>

<style>
/* Add any component specific styles here */
@import '../assets/css/detail.css';
</style>