import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue' 
import LogoutView from '../views/LogoutView.vue'
import AddcarView from '../views/AddcarView.vue'
import ExploreView from '../views/ExploreView.vue'
import ProfileView from '../views/ProfileView.vue'  
import DetailView from '../views/DetailView.vue'

const requireAuth = (to, from, next) =>{   
        
    // GET CSRF TOKEN
    /*
    let csrf_token = "";
    fetch('/api/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(`CSRF response ${data}`);
            csrf_token = data.csrf_token;
        });*/

    if(localStorage.jwt_token){
      let token = localStorage.getItem("jwt_token"); 

      
      fetch('/api/jwt-token',{ method: 'GET',headers: {'Authorization':`Bearer ${token}`} })  // ,headers: {'X-CSRFToken': csrf_token,'Authorization':`Bearer ${token}`}
            .then((response) => response.json())
            .then((data) => {
              let keys = Object.keys(data);
              if (keys.includes("message")){
                  if (data["message"] === "User already logged in"){
                    // console.log(`User already logged in, going to ${to.name}    from  ${from.path}`); 

                    if(to.name == "explore"){
                      return next();
                    }
                    else if(to.name == "profile"){
                      return next();
                    }
                    else if(to.name == "addcar"){
                      return next();
                    }
                    else if(to.name == "register"){ 
                      return next({ name: "home" });
                    }
                    else if(to.name == "login"){ 
                      console.log('LOGIN CALLED');
                      return next({ name: "home" });
                    }
                    else{
                      return next()
                    } 
                  } 
              }else if (keys.includes("code")){
                if(localStorage.jwt_token) {
                  localStorage.clear();
                }
                return next({ name: 'login' });
              }
              else{
                return next({ name: 'login' });
              }

            }).catch((error) => {
              console.error('Error:', error);
              return next({ name: 'home' });
            }); 
    }
    else{
      //console.log(`User NOT logged in, going to ${to.name}   from  ${from.name}`); 
        localStorage.clear(); 
        if(to.name == "explore"){ 
          return next({ name: 'home' });
        }
        else if(to.name == "profile"){ 
          return next( { name: 'home' });
        }
        else if(to.name == "addcar"){ 
          return next({ name: 'home' });
        }
        else if(to.name == "login"){ 
          return next();
        }
        else if(to.name == "register"){ 
          return next();
        } 
    }

    

  } 


  const logout= (to, from, next) =>{

   
    console.log('loggingout in real progress');

      
      if(localStorage.jwt_token){

            localStorage.clear();
            next({ name: 'login' });
          } 
          else{
            next({ name: 'home' });
          }
        
  }





  

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },{
      path: '/register',
      name: 'register',
      component: RegisterView,
      beforeEnter: requireAuth
    },
    {
      path: '/login',
      name:'login',
      component: LoginView,
      beforeEnter: requireAuth
    },
    {
      path: '/logout',
      name:'logout',
      component: LogoutView,
      /*beforeEnter: logout*/
    },  
    {
      path:"/explore",
      name:"explore",
      component: ExploreView,
      beforeEnter: requireAuth
    },
    {
      path: '/addcar',
      name: 'addcar',
      component: AddcarView,
      beforeEnter: requireAuth
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      beforeEnter: requireAuth
    },
    {
      path: '/detail/:id',
      name: 'detail',
      component: DetailView,
      beforeEnter: requireAuth
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
