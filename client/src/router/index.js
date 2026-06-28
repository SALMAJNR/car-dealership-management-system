import { createRouter, createWebHistory } from "vue-router"

import CarList from "../components/CarList.vue"
import BrandList from "../components/BrandList.vue"
import CategoryList from "../components/CategoryList.vue"
import DealerList from "../components/DealerList.vue"
import CustomerList from "../components/CustomerList.vue"
import Login from "../components/Login.vue"

import { useUserStore } from "../stores/user"

const routes = [
  { path: "/", component: CarList },
  { path: "/brands", component: BrandList },
  { path: "/categories", component: CategoryList },
  { path: "/dealers", component: DealerList },
  { path: "/customers", component: CustomerList },
  { path: "/login", component: Login }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to) => {
  const userStore = useUserStore()

  if (!userStore.checked) {
    await userStore.fetchMy()
  }

  if (to.path !== "/login" && !userStore.isAuthenticated) {
    return "/login"
  }

  if (to.path === "/login" && userStore.isAuthenticated) {
    return "/"
  }
})

export default router