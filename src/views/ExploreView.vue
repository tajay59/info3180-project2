<script>
export default {
    data() {
        return {
            searchmake:"",
            searchmodel:"",
            tagimage:"@/assets/images/tag.svg",
            csrf_token:"",
            getallresults:[]
        };
    },
    created(){

        this.getCsrfToken();
        this.getall();
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
                .then((data) => {
                    console.log(data);
                    self.csrf_token = data.csrf_token;
                });
        },
        getall(){
            let token = localStorage.getItem("jwt_token");
            fetch('/api/cars', { method: 'GET',headers: {'X-CSRFToken': this.csrf_token,'Authorization':`Bearer ${token}`} })//
            .then(response => response.json())
            .then(data => {
            console.log('Success:', data); 

            let keys = Object.keys(data);
            if (keys.includes("code")){
                if( data['code'] === "token_expired"){
                    localStorage.removeItem("jwt_token"); 
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
                // Empty array first
                self.getallresults.splice(0,self.getallresults.length);

                data["results"].splice(-3).forEach((el)=>{
                    el["photo"] =`/api/images/${el["photo"]}`;
                    self.getallresults.push(el)
                });
                 
            }

            })
            .catch((error) => {
            console.error('Error:', error);
            });
        }, searchOne(){

            let token = localStorage.getItem("jwt_token");
            fetch(`/api/search?make=${this.searchmake}&model=${this.searchmodel}`, { method: 'GET', headers: {'X-CSRFToken': this.csrf_token,'Authorization':`Bearer ${token}`} })//
            .then(response => response.json())
            .then(data => {
            console.log('Success:', data); 

            let keys = Object.keys(data);
            if (keys.includes("code")){
                if( data['code'] === "token_expired"){
                    localStorage.removeItem("jwt_token"); 
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
                    el["to"] = `/details/${el["id"]}`
                    self.getallresults.push(el)
                });
                 
            }

            })
            .catch((error) => {
            console.error('Error:', error);
            });

        }
    }
}
</script>

<template >

    
    <div class="explorecontainer">
        <div class="topbar">
            <div class="topbartitle"><h1 id="exploretitle">Explore</h1></div>
            
            <form @submit.prevent="searchOne" id="search">
                <div class="searchitems">
                    <label for="make">Make</label>
                    <input id="make" type="text" name="make" v-model="searchmake">
                </div>
                <div class="searchitems">
                    <label for="model">Model</label>
                    <input id="model" type="text" name="model" v-model="searchmodel">
                </div>
                <button > 
                    <img src="@/assets/images/search.svg" alt="">
                </button>
            </form>  
        </div>
         
        <div class="listresults" >
            <div class="card" v-for="car in getallresults" :key="car.id" >
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
@import '../assets/css/explore.css';
</style>