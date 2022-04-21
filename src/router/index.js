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
    let csrf_token = "";
    fetch('/api/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(`CSRF response ${data}`);
            csrf_token = data.csrf_token;
        });

    if(localStorage.jwt_token){
      let token = localStorage.getItem("jwt_token");
      fetch('/api/jwt-token',{ method: 'GET',headers: {'X-CSRFToken': csrf_token,'Authorization':`Bearer ${token}`} })
            .then((response) => response.json())
            .then((data) => {
              let keys = Object.keys(data);
              if (keys.includes("message")){
                  if (data["message"] === "User already logged in"){
                    console.log("User already logged in"); 

                    if(to.name == "/explore"){
                      next({ name: 'explore' });
                    }
                    else if(to.name == "/profile"){
                      next({ name: 'profile' });
                    }
                    else if(to.name == "/addcar"){
                      next({ name: 'addcar' });
                    }
                    else{
                      next()
                    } 
                  } 
              }else if (keys.includes("code")){
                if(localStorage.jwt_token) {
                  localStorage.removeItem("jwt_token");
                  localStorage.removeItem("user");
                  localStorage.removeItem("user_id");
                }
                 next({ name: 'login' });
              }
              else{
                next({ name: 'login' });
              }

            }); 
    }
    else{
      next('/login')
    }

  } 

  const logout= (to, from, next) =>{

   
    console.log('loggingout in real progress');

      
      if(localStorage.jwt_token){

            localStorage.removeItem("jwt_token");
            localStorage.removeItem("user");
            localStorage.removeItem("user_id");
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
      component: RegisterView
    },
    {
      path: '/login',
      name:'login',
      component: LoginView
    },
    {
      path: '/logout',
      name:'logout',
      component: LogoutView,
      beforeEnter: logout
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
