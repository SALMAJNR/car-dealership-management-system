<script setup>
import { ref, onBeforeMount, computed } from "vue"
import axios from "axios"
import Cookies from "js-cookie"
import { useUserStore } from "@/stores/user"

import NotificationToast from "./dashboard/NotificationToast.vue"

const userStore = useUserStore()

const brands = ref([])
const search = ref("")

const brandToAdd = ref({
  name: ""
})

const brandToEdit = ref({})

const notification = ref({
  show: false,
  message: "",
  type: "success"
})

const filteredBrands = computed(() => {
  const keyword = search.value.toLowerCase()

  return brands.value.filter(brand =>
    brand.name.toLowerCase().includes(keyword)
  )
})

function notify(message, type = "success") {
  notification.value = {
    show: true,
    message,
    type
  }

  setTimeout(() => {
    notification.value.show = false
  }, 3000)
}

async function fetchBrands() {
  const r = await axios.get("/api/brands/")
  brands.value = r.data
}

async function onBrandAdd() {
  try {
    if (!brandToAdd.value.name.trim()) {
      notify("Brand name is required", "warning")
      return
    }

    await axios.post("/api/brands/", brandToAdd.value)

    brandToAdd.value = {
      name: ""
    }

    await fetchBrands()

    notify("Brand added successfully")
  } catch (error) {
    notify("Could not add brand", "error")
  }
}

async function onRemoveClick(brand) {
  const confirmed = confirm(`Delete ${brand.name}?`)

  if (!confirmed) return

  try {
    await axios.delete(`/api/brands/${brand.id}/`)
    await fetchBrands()

    notify("Brand deleted successfully")
  } catch (error) {
    notify("Could not delete brand", "error")
  }
}

function onBrandEditClick(brand) {
  brandToEdit.value = { ...brand }
}

async function onUpdateBrand() {
  try {
    if (!brandToEdit.value.name.trim()) {
      notify("Brand name is required", "warning")
      return
    }

    await axios.put(`/api/brands/${brandToEdit.value.id}/`, {
      ...brandToEdit.value
    })

    brandToEdit.value = {}

    await fetchBrands()

    notify("Brand updated successfully")
  } catch (error) {
    notify("Could not update brand", "error")
  }
}

onBeforeMount(async () => {
  axios.defaults.withCredentials = true
  axios.defaults.headers.common["X-CSRFToken"] =
    Cookies.get("csrftoken")

  await fetchBrands()
})
</script>

<template>
  <section class="brand-page">
    <NotificationToast
      :show="notification.show"
      :message="notification.message"
      :type="notification.type"
    />

    <div class="page-header">
      <div>
        <span class="eyebrow">Inventory Setup</span>
        <h1>Brands</h1>
        <p>
          Manage all car brands used across the dealership inventory.
        </p>
      </div>

      <div class="count-card">
        <span>🏷️</span>
        <div>
          <strong>{{ brands.length }}</strong>
          <p>Total Brands</p>
        </div>
      </div>
    </div>

    <form
      v-if="userStore.user?.role === 'admin'"
      class="form-card"
      @submit.prevent="onBrandAdd"
    >
      <div>
        <h2>Add New Brand</h2>
        <p>Create a new vehicle brand for your inventory.</p>
      </div>

      <div class="form-row">
        <input
          v-model="brandToAdd.name"
          placeholder="Example: Toyota"
        />

        <button type="submit">
          Add Brand
        </button>
      </div>
    </form>

    <div class="search-card">
      <div>
        <h2>Search Brands</h2>
        <p>Search while typing.</p>
      </div>

      <input
        v-model="search"
        placeholder="Search brand name"
      />
    </div>

    <div class="list-header">
      <h2>Brand List</h2>
      <p>Showing {{ filteredBrands.length }} of {{ brands.length }}</p>
    </div>

    <div v-if="filteredBrands.length" class="brand-grid">
      <div
        v-for="item in filteredBrands"
        :key="item.id"
        class="brand-card"
      >
        <div class="brand-icon">
          🏷️
        </div>

        <div class="brand-info">
          <h3>{{ item.name }}</h3>
          <p>Brand ID: {{ item.id }}</p>
        </div>

        <div
          v-if="userStore.user?.role === 'admin'"
          class="actions"
        >
          <button
            class="edit-btn"
            @click="onBrandEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editBrandModal"
          >
            Edit
          </button>

          <button
            class="delete-btn"
            @click="onRemoveClick(item)"
          >
            Delete
          </button>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <div>🏷️</div>
      <h3>No brands found</h3>
      <p>Try another search or add a new brand.</p>
    </div>

    <div
      v-if="userStore.user?.role === 'admin'"
      class="modal fade"
      id="editBrandModal"
      tabindex="-1"
    >
      <div class="modal-dialog">
        <div class="modal-content rounded-4">
          <div class="modal-header">
            <h5 class="modal-title">
              Edit Brand
            </h5>

            <button
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>
          </div>

          <div class="modal-body">
            <input
              class="form-control"
              v-model="brandToEdit.name"
              placeholder="Brand name"
            />
          </div>

          <div class="modal-footer">
            <button
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>

            <button
              class="btn btn-primary"
              data-bs-dismiss="modal"
              @click="onUpdateBrand"
            >
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.brand-page {
  min-height: 100vh;
  padding-bottom: 40px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 22px;
  margin-bottom: 24px;
}

.eyebrow {
  color: #2563eb;
  font-weight: 900;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.08em;
}

.page-header h1 {
  margin: 6px 0;
  font-size: 38px;
  font-weight: 950;
  color: #0f172a;
}

.page-header p {
  color: #64748b;
  margin: 0;
  font-weight: 600;
}

.count-card,
.form-card,
.search-card,
.brand-card,
.empty-state {
  background: white;
  border-radius: 24px;
  box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
}

.count-card {
  min-width: 220px;
  padding: 22px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.count-card span,
.brand-icon {
  width: 54px;
  height: 54px;
  border-radius: 16px;
  background: #eff6ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
}

.count-card strong {
  font-size: 28px;
  font-weight: 950;
  color: #0f172a;
}

.count-card p {
  margin: 0;
}

.form-card,
.search-card {
  padding: 24px;
  margin-bottom: 24px;
}

.form-card h2,
.search-card h2,
.list-header h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 950;
  color: #0f172a;
}

.form-card p,
.search-card p,
.list-header p {
  margin: 4px 0 0;
  color: #64748b;
  font-weight: 600;
}

.form-row {
  margin-top: 18px;
  display: flex;
  gap: 14px;
}

input {
  width: 100%;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  padding: 13px 14px;
  border-radius: 14px;
  outline: none;
  font-weight: 600;
}

input:focus {
  border-color: #2563eb;
  background: white;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
}

.form-row button {
  border: none;
  background: #2563eb;
  color: white;
  padding: 13px 18px;
  border-radius: 14px;
  font-weight: 900;
  min-width: 140px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 16px;
  margin-bottom: 18px;
}

.brand-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.brand-card {
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  transition: 0.25s ease;
}

.brand-card:hover {
  transform: translateY(-4px);
}

.brand-info h3 {
  margin: 0;
  font-size: 22px;
  font-weight: 950;
  color: #0f172a;
}

.brand-info p {
  margin: 4px 0 0;
  color: #64748b;
  font-weight: 600;
}

.actions {
  display: flex;
  gap: 10px;
}

.actions button {
  flex: 1;
  border: none;
  padding: 11px 14px;
  border-radius: 12px;
  font-weight: 900;
}

.edit-btn {
  background: #2563eb;
  color: white;
}

.delete-btn {
  background: #ef4444;
  color: white;
}

.empty-state {
  padding: 50px;
  text-align: center;
}

.empty-state div {
  font-size: 52px;
}

.empty-state h3 {
  font-size: 24px;
  font-weight: 900;
  color: #0f172a;
  margin: 12px 0 6px;
}

.empty-state p {
  color: #64748b;
  margin: 0;
}

:global(.dark-mode) .page-header h1,
:global(.dark-mode) .count-card strong,
:global(.dark-mode) .form-card h2,
:global(.dark-mode) .search-card h2,
:global(.dark-mode) .list-header h2,
:global(.dark-mode) .brand-info h3,
:global(.dark-mode) .empty-state h3 {
  color: #e5e7eb;
}

:global(.dark-mode) .count-card,
:global(.dark-mode) .form-card,
:global(.dark-mode) .search-card,
:global(.dark-mode) .brand-card,
:global(.dark-mode) .empty-state {
  background: #0f172a;
}

:global(.dark-mode) input {
  background: #020617;
  color: #e5e7eb;
  border-color: #334155;
}

@media (max-width: 1000px) {
  .brand-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }
}

@media (max-width: 650px) {
  .brand-grid {
    grid-template-columns: 1fr;
  }

  .form-row,
  .list-header {
    flex-direction: column;
    align-items: stretch;
  }

  .page-header h1 {
    font-size: 30px;
  }
}
</style>