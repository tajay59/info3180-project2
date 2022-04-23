<script>
export default {
    data() {
        return {
            csrf_toke:"" ,
            newcaradded:false,
            newcar:"",
            make:false,
            model:false,
            colour:false,
            year:false,
            price:false,
            description:false,
            photo:false,
            error:false
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
        addcar(){
            let form = document.querySelector("#addForm");
            let form_data = new FormData(form);

            if(localStorage.jwt_token){
                let token = localStorage.getItem("jwt_token");
                fetch('/api/cars', { method: 'POST', body: form_data, headers: {'X-CSRFToken': this.csrf_token,'Authorization':`Bearer ${token}`} })//
                        .then(response => response.json())
                        .then(data => {
                        console.log('Success:', data);
                        let keys = Object.keys(data);
                        if (keys.includes("code")){
                        if( data['code'] === "token_expired"){
                            localStorage.removeItem("jwt_token");  
                            this.$router.push({name:"home"});
                                            } 
                        } 
                        
                        if (keys.includes("message")){
                            if( data['message'] === "New car added"){
                                
                                this.newcar = data['car'];
                                this.newcaradded = true;
                                setTimeout(()=>{this.newcaradded = false;},10000);                                
                            } 
                            else if(data['message'] === "Form errors"){
                                let res = data["errors"]
                                
                                res.forEach(element => {

                                    if(element.includes("Make")){       this.make = true; }
                                    if(element.includes("Model")){      this.model = true; }
                                    if(element.includes("Colour")){     this.colour = true; }
                                    if(element.includes("Year")){       this.year = true; }
                                    if(element.includes("Price")){      this.price = true; }
                                    if(element.includes("description")){this.description = true; }
                                    if(element.includes("Photo")){      this.photo  = true; }

                                });

                                this.error = true;
                                this.success = false;
                                this.danger = true; 

                                setTimeout(()=>{
                                    this.error          = false;
                                    this.make           = false;
                                    this.model          = false;
                                    this.colour         = false;
                                    this.year           = false;
                                    this.price          = false;
                                    this.description    = false;
                                    this.photo          = false;                                    
                                
                                
                                },5000);
                            } 
                        } 
                        
                        })
                        .catch((error) => {
                        console.error('Error:', error);
                        });
                        }
                        else{
                            console.log("CANT SEND REQUEST WITHOUT A TOKEN");
                        }
            

            


        }
    }
}
</script>

<template>
    <div id="addcar_container"> 
        
        <h1>Add New Car</h1>
        <form  @submit.prevent="addcar" id="addForm">
            <h6 v-if="newcaradded" id="newcar">{{newcar}}</h6>
            <hr>

            <div class="groupone">

                    <div class="loginformitems">                
                        <input id="make" type="text" name="make" class="loginformitems__input"  placeholder=" " maxlength="80">
                        <label for="make" class="loginformitems__label" >Make</label>
                        <h6 v-if="(make && error)"      class="danger erroritem">required!</h6>
                    </div>
                    <div class="loginformitems">
                        <input type="text" name="model" class="loginformitems__input"  placeholder=" " maxlength="80">
                        <label for="model" class="loginformitems__label">Model</label>
                        <h6 v-if="(model && error)"      class="danger erroritem">required!</h6>
                    </div>
                    <div class="loginformitems">                
                        <input id="colour" type="text" name="colour" class="loginformitems__input"  placeholder=" " maxlength="80">
                        <label for="colour" class="loginformitems__label" >Colour</label>
                        <h6 v-if="(colour && error)"      class="danger erroritem">required!</h6>
                    </div>
                    <div class="loginformitems">                
                        <input id="year" type="text" name="year" class="loginformitems__input"  placeholder=" " maxlength="4">
                        <label for="year" class="loginformitems__label">Year</label>
                        <h6 v-if="(year && error)"      class="danger erroritem">required!</h6>
                    </div>
                    <div class="loginformitems">                
                        <input id="price" type="text" name="price" class="loginformitems__input"  placeholder=" " maxlength="80">
                        <label for="price" class="loginformitems__label">Price</label>
                        <h6 v-if="(price && error)"      class="danger erroritem">required!</h6>
                    </div>
                    <div class="loginformitems">                
                        <select  name="car_type" id="car_type" class="loginformitems__input"  placeholder=" ">
                            <option value="suv">SUV</option>
                            <option value="sedan" >Sedan</option>
                            <option value="coupe">Coupe</option>
                            <option value="pickup">Pickup Truck</option>
                        </select>
                        <label for="car_type" class="loginformitems__label">Car Type</label>
                        
                    </div>
                    <div class="loginformitems">
                        <select name="transmission" id="transmission" class="loginformitems__input"  placeholder=" ">
                            <option value="automatic">Automatic</option>
                            <option value="manual">Manual</option> 
                        </select>
                        <label for="transmission" class="loginformitems__label">Tranmission</label>
                    </div>

            </div>
            
            <div class="loginformitems descriptionbox">                
                <textarea name="description" id="description" cols="30" rows="3" class="loginformitems__input addcardescription"  placeholder=" " maxlength="1000"></textarea>
                <label for="description" class="loginformitems__label">Description</label>
                <h6 v-if="(description && error)"      class="danger erroritem">required!</h6>
            </div> 

            <div class="filestyle" >                
                <input id="photo" type="file" name="photo"  placeholder=" "> 
                <h6 v-if="(photo  && error) "      class="danger erroritem photoerror">required!</h6>
            </div>


            <div class="addcarbtn" >
                <button class="loginsubmit addcarbutton">Save</button>
            </div>
            
            
        </form>
    </div>
</template>

<style>
@import '../assets/css/addcar.css'
/* Add any component specific styles here */
</style>