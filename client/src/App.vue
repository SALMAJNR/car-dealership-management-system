<template>
  <div class="container mt-3">

    <ul
      class="nav nav-tabs mb-3"
      v-if="$route.path !== '/login'"
    >

      <li class="nav-item">
        <router-link
          to="/"
          class="nav-link"
          active-class="active"
        >
          Cars
        </router-link>
      </li>

      <li
        class="nav-item"
        
      >
        <router-link
          to="/brands"
          class="nav-link"
          active-class="active"
        >
          Brands
        </router-link>
      </li>

      <li class="nav-item">
        <router-link
          to="/categories"
          class="nav-link"
          active-class="active"
        >
          Categories
        </router-link>
      </li>

      <li class="nav-item">
        <router-link
          to="/dealers"
          class="nav-link"
          active-class="active"
        >
          Dealers
        </router-link>
      </li>

      <li class="nav-item">

  <router-link
    to="/customers"
    class="nav-link"
    active-class="active"
  >
    Customers
  </router-link>

</li>

      <li
        v-if="userStore.isAuthenticated"
        class="nav-item dropdown ms-auto"
      >

        <a
          class="nav-link dropdown-toggle"
          href="#"
          role="button"
          data-bs-toggle="dropdown"
        >
          {{ userStore.user?.username }}
          ({{ userStore.user?.role }})
        </a>

        <ul class="dropdown-menu dropdown-menu-end">

          <li v-if="userStore.user?.role === 'admin'">
            <a
              class="dropdown-item"
              href="http://localhost:8000/admin"
            >
              Admin Panel
            </a>
          </li>

          <li>
            <button
              class="dropdown-item"
              @click="logout"
            >
              Logout
            </button>
          </li>

        </ul>

      </li>

    </ul>

    <router-view />

  </div>
</template>

<script setup>
import { onBeforeMount } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useUserStore } from "@/stores/user"

const $route = useRoute()
const router = useRouter()
const userStore = useUserStore()

onBeforeMount(async () => {
  await userStore.fetchMy()
})

async function logout() {
  await userStore.logout()
  router.push("/login")
}
</script>