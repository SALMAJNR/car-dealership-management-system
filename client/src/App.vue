<template>
  <div :class="['app-layout', { 'dark-mode': darkMode }]">
    <aside v-if="$route.path !== '/login'" class="sidebar">
      <div class="sidebar-brand">
        <div class="logo">🚗</div>
        <div>
          <h2>Car Dealer</h2>
          <p>Admin Dashboard</p>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/">🚗 Cars</router-link>
        <router-link to="/brands">🏷️ Brands</router-link>
        <router-link to="/categories">📁 Categories</router-link>
        <router-link to="/dealers">🏬 Dealers</router-link>
        <router-link to="/customers">👤 Customers</router-link>
      </nav>
    </aside>

    <div class="content-area">
      <header v-if="$route.path !== '/login'" class="topbar">
        <div>
          <h1>{{ pageTitle }}</h1>
          <p>{{ pageSubtitle }}</p>
        </div>

        <div class="topbar-actions">
          <button class="theme-btn" @click="toggleDarkMode">
            {{ darkMode ? "☀️" : "🌙" }}
          </button>

          <div v-if="userStore.isAuthenticated" class="dropdown">
            <button class="user-btn dropdown-toggle" data-bs-toggle="dropdown">
              <span class="avatar">👤</span>
              <div>
                <strong>{{ userStore.user?.username }}</strong>
                <small>{{ userStore.user?.role }}</small>
              </div>
            </button>

            <ul class="dropdown-menu dropdown-menu-end">
              <li v-if="userStore.user?.role === 'admin'">
                <a class="dropdown-item" href="http://localhost:8000/admin" target="_blank">
                  Admin Panel
                </a>
              </li>

              <li>
                <button class="dropdown-item" @click="logout">
                  Logout
                </button>
              </li>
            </ul>
          </div>
        </div>
      </header>

      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useUserStore } from "@/stores/user"

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const darkMode = ref(localStorage.getItem("darkMode") === "true")

const pageTitle = computed(() => {
  if (route.path === "/") return "Car Inventory"
  if (route.path === "/brands") return "Brands"
  if (route.path === "/categories") return "Categories"
  if (route.path === "/dealers") return "Dealers"
  if (route.path === "/customers") return "Customers"
  return "Dashboard"
})

const pageSubtitle = computed(() => {
  if (route.path === "/") return "Manage cars, images, brands, dealers, and exports."
  if (route.path === "/brands") return "Manage all vehicle brands."
  if (route.path === "/categories") return "Organize cars by category."
  if (route.path === "/dealers") return "Manage dealership partners."
  if (route.path === "/customers") return "View customers and purchased cars."
  return "Manage your dealership professionally."
})

function toggleDarkMode() {
  darkMode.value = !darkMode.value
  localStorage.setItem("darkMode", darkMode.value)
}

async function logout() {
  await userStore.logout()
  router.push("/login")
}

onMounted(async () => {
  if (!userStore.checked) {
    await userStore.fetchMy()
  }
})
</script>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: #f8fafc;
  font-family: Arial, sans-serif;
}

.app-layout {
  min-height: 100vh;
  background: #f8fafc;
  color: #0f172a;
}

.sidebar {
  width: 260px;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  min-height: 100vh;
  background: #020617;
  color: white;
  padding: 25px;
  overflow-y: auto;
  z-index: 200;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 36px;
}

.logo {
  width: 54px;
  height: 54px;
  background: linear-gradient(135deg, #2563eb, #60a5fa);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
}

.sidebar-brand h2 {
  margin: 0;
  font-size: 21px;
  font-weight: 900;
}

.sidebar-brand p {
  margin: 3px 0 0;
  color: #94a3b8;
  font-size: 13px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.sidebar-nav a {
  text-decoration: none;
  color: #cbd5e1;
  padding: 15px 16px;
  border-radius: 16px;
  font-weight: 800;
}

.sidebar-nav a:hover,
.sidebar-nav a.router-link-active {
  background: #2563eb;
  color: white;
}

.content-area {
  margin-left: 260px;
  width: calc(100% - 260px);
  min-height: 100vh;
}

.topbar {
  min-height: 82px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 34px;
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(18px);
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  z-index: 100;
}

.topbar h1 {
  margin: 0;
  font-size: 25px;
  font-weight: 950;
}

.topbar p {
  margin: 4px 0 0;
  color: #64748b;
  font-weight: 600;
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.theme-btn {
  width: 48px;
  height: 48px;
  border: none;
  background: #f1f5f9;
  border-radius: 15px;
  font-size: 20px;
}

.user-btn {
  border: none;
  background: #f1f5f9;
  color: #0f172a;
  padding: 8px 14px;
  border-radius: 15px;
  font-weight: 900;
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  width: 36px;
  height: 36px;
  background: #e0edff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-btn div {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-btn small {
  color: #64748b;
  text-transform: capitalize;
  font-size: 11px;
}

.main-content {
  padding: 34px;
  max-width: 1600px;
  margin: 0 auto;
}

.dark-mode {
  background: #020617;
  color: #e5e7eb;
}

.dark-mode .content-area {
  background: #020617;
}

.dark-mode .topbar {
  background: rgba(15, 23, 42, 0.94);
  border-bottom-color: #1e293b;
}

.dark-mode .topbar h1 {
  color: #e5e7eb;
}

.dark-mode .theme-btn,
.dark-mode .user-btn {
  background: #1e293b;
  color: #e5e7eb;
}

.dark-mode .avatar {
  background: #334155;
}

@media (max-width: 900px) {
  .sidebar {
    position: relative;
    width: 100%;
    min-height: auto;
  }

  .content-area {
    margin-left: 0;
    width: 100%;
  }

  .sidebar-nav {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }

  .topbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .main-content {
    padding: 20px;
  }
}
</style>