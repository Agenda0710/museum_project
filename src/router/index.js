import Vue from 'vue'
import Router from 'vue-router'
import LayOut from '@/views/LayOut.vue'
import MuseumEast from '@/views/MuseumEast.vue'
import MuseumPeople from '@/views/MuseumPeople.vue'
import TestChart from '@/views/TestChart.vue'
import Category from "@/views/Category.vue";
import getAllRelics from "@/views/GetAllRelics.vue";
import museumUsers from "@/views/MuseumUsers.vue";
import userLogin from "@/views/UserLogin.vue";
import PeoplePrediction from "@/views/PeoplePrediction.vue";


Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            component: LayOut,
            children: [
                {
                    path: '',
                    redirect: 'login'
                },
                {
                    path: 'eastMuseum',
                    component: MuseumEast
                },
                {
                    path: 'peopleMuseum',
                    component: MuseumPeople
                },
                {
                    path: 'category',
                    component: Category
                },
                {
                    path: 'getAllRelics',
                    component: getAllRelics
                },
                {
                    path: 'users',
                    component: museumUsers
                },
                {
                    path: 'peoplePrediction',
                    component: PeoplePrediction
                }
            ]
        },
        {
            path: '/testChart',
            component: TestChart
        },
        {
            path: '/login',
            component: userLogin
        }
    ]
})



