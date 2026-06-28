<template>
  <div :class="['app-shell', { 'dark-mode': darkMode }]">
    <nav v-if="$route.path !== '/login'" class="top-nav">
      <div class="brand">
        <span class="brand-icon">🚗</span>
        <div>
          <h1>Car Dealership</h1>
          <p>Management System</p>
        </div>
      </div>

      <div class="nav-links">
        <router-link to="/">Cars</router-link>
        <router-link to="/brands">Brands</router-link>
        <router-link to="/categories">Categories</router-link>
        <router-link to="/dealers">Dealers</router-link>
        <router-link to="/customers">Customers</router-link>
      </div>

      <div class="nav-actions">
        <button class="theme-btn" @click="toggleDarkMode">
          {{ darkMode ? "☀️ Light" : "🌙 Dark" }}
        </button>

        <div v-if="userStore.isAuthenticated" class="dropdown">
          <button
            class="user-btn dropdown-toggle"
            data-bs-toggle="dropdown"
          >
            {{ userStore.user?.username }}
            <span>{{ userStore.user?.role }}</span>
          </button>

          <ul class="dropdown-menu dropdown-menu-end">
            <li v-if="userStore.user?.role === 'admin'">
              <a
                class="dropdown-item"
                href="http://localhost:8000/admin"
                target="_blank"
              >
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
    </nav>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { useUserStore } from "@/stores/user"

const router = useRouter()
const userStore = useUserStore()

const darkMode = ref(localStorage.getItem("darkMode") === "true")

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
}

.app-shell {
  min-height: 100vh;
  background: #f8fafc;
  color: #0f172a;
  transition: 0.25s ease;
}

.app-shell.dark-mode {
  background: #020617;
  color: #e5e7eb;
}

.top-nav {
  max-width: 1180px;
  margin: 0 auto;
  padding: 18px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 22px;
  border-bottom: 1px solid #e2e8f0;
}

.dark-mode .top-nav {
  border-bottom-color: #1e293b;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-icon {
  width: 46px;
  height: 46px;
  background: #eff6ff;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.brand h1 {
  font-size: 18px;
  margin: 0;
  font-weight: 800;
}

.brand p {
  margin: 2px 0 0;
  color: #64748b;
  font-size: 13px;
}

.nav-links {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.nav-links a {
  text-decoration: none;
  color: #475569;
  font-weight: 700;
  padding: 10px 14px;
  border-radius: 12px;
}

.nav-links a.router-link-active {
  background: #2563eb;
  color: white;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.theme-btn,
.user-btn {
  border: none;
  background: white;
  color: #0f172a;
  padding: 10px 14px;
  border-radius: 12px;
  font-weight: 700;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
}

.dark-mode .theme-btn,
.dark-mode .user-btn {
  background: #0f172a;
  color: #e5e7eb;
}

.user-btn span {
  margin-left: 6px;
  color: #64748b;
  font-size: 12px;
  text-transform: capitalize;
}

.main-content {
  max-width: 1180px;
  margin: 0 auto;
  padding: 24px;
}

.dark-mode .main-content {
  background: #020617;
}

@media (max-width: 900px) {
  .top-nav {
    flex-direction: column;
    align-items: flex-start;
  }

  .nav-actions {
    width: 100%;
    justify-content: space-between;
  }

  .main-content {
    padding: 16px;
  }
}
</style>