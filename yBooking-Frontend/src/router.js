import { createRouter, createWebHistory } from 'vue-router';
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: ()=>import("./components/Home.vue")
        },
        {
          path: '/login',
          name: 'login',
          component: ()=>import("./components/Login.vue")
        },
        {
            path: '/signup',
            name: 'signup',
            component: ()=>import("./components/SignUp.vue")
        },
        {
            path: '/product',
            name: 'product',
            component: ()=>import("./components/Product.vue")
        },
        {
            path: '/launchproduct',
            name: 'launchproduct',
            component: ()=>import("./components/LaunchProduct.vue")
        },
        {
            path: '/shoppingcart',
            name: 'shoppingcart',
            component: ()=>import("./components/ShoppingCart.vue")
        },
        { 
            path: '/product/:id', 
            component: ()=>import("./components/ProductDetail.vue") 
        },
        {
            path: '/order',
            name: 'order',
            component: ()=>import("./components/Order.vue")
        },
        {
            path: '/editproduct',
            name: 'editproduct',
            component: ()=>import("./components/EditProduct.vue")
        },
        {
            path: '/editproduct/:id',
            component: ()=>import("./components/EditProductDetail.vue")
        }
    ],
});
export default router;
