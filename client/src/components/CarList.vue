<script setup>
import { ref, onBeforeMount, computed } from "vue"
import axios from "axios"
import Cookies from "js-cookie"
import { useUserStore } from "@/stores/user"

const userStore = useUserStore()

const cars = ref([])
const brands = ref([])
const categories = ref([])
const dealers = ref([])

const carToAdd = ref({
  model: "",
  brand: null,
  category: null,
  dealer: null,
  year: null
})

const carToEdit = ref({})
const carsPictureRef = ref()
const carAddImageUrl = ref()
const stats = ref(null)

const modelFilter = ref("")
const brandFilter = ref("")
const categoryFilter = ref("")
const dealerFilter = ref(0)

const brandById = computed(() => {
  const result = {}
  for (let b of brands.value) result[b.id] = b
  return result
})

const categoryById = computed(() => {
  const result = {}
  for (let c of categories.value) result[c.id] = c
  return result
})

const dealerById = computed(() => {
  const result = {}
  for (let d of dealers.value) result[d.id] = d
  return result
})

const carsFiltered = computed(() => {
  const modelCI = modelFilter.value.toLowerCase()
  const brandCI = brandFilter.value.toLowerCase()
  const categoryCI = categoryFilter.value.toLowerCase()

  return cars.value.filter(item =>
    (!modelFilter.value || item.model.toLowerCase().includes(modelCI)) &&
    (!brandFilter.value || brandById.value[item.brand]?.name.toLowerCase().includes(brandCI)) &&
    (!categoryFilter.value || categoryById.value[item.category]?.name.toLowerCase().includes(categoryCI)) &&
    (!dealerFilter.value || item.dealer == dealerFilter.value)
  )
})

async function fetchCars() {
  const r = await axios.get("/api/cars/")
  cars.value = r.data
}

async function fetchBrands() {
  const r = await axios.get("/api/brands/")
  brands.value = r.data
}

async function fetchCategories() {
  const r = await axios.get("/api/categories/")
  categories.value = r.data
}

async function fetchDealers() {
  const r = await axios.get("/api/dealers/")
  dealers.value = r.data
}

async function fetchStats() {
  const r = await axios.get("/api/cars/stats/")
  stats.value = r.data
}

async function onCarAdd() {
  const formData = new FormData()

  if (carsPictureRef.value?.files[0]) {
    formData.append("picture", carsPictureRef.value.files[0])
  }

  formData.append("model", carToAdd.value.model)
  formData.append("brand", carToAdd.value.brand)
  formData.append("category", carToAdd.value.category)
  formData.append("dealer", carToAdd.value.dealer)
  formData.append("year", carToAdd.value.year)

  await axios.post("/api/cars/", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  })

  carToAdd.value = {
    model: "",
    brand: null,
    category: null,
    dealer: null,
    year: null
  }

  carAddImageUrl.value = null
  await fetchCars()
  await fetchStats()
}

async function onRemoveClick(car) {
  await axios.delete(`/api/cars/${car.id}/`)
  await fetchCars()
  await fetchStats()
}

function onCarEditClick(car) {
  carToEdit.value = { ...car }
}

async function onUpdateCar() {
  await axios.put(`/api/cars/${carToEdit.value.id}/`, { ...carToEdit.value })
  carToEdit.value = {}
  await fetchCars()
}

async function onPurchaseClick(car) {
  await axios.post("/api/customers/bind-car/", { car_id: car.id })
  alert("Car purchased successfully")
}

function carsAddPictureChange() {
  carAddImageUrl.value = URL.createObjectURL(carsPictureRef.value.files[0])
}

function onExportExcel() {
  window.open("http://127.0.0.1:8000/api/cars/export_excel/")
}

onBeforeMount(async () => {
  axios.defaults.withCredentials = true
  axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken")

  await fetchCars()
  await fetchBrands()
  await fetchCategories()
  await fetchDealers()
  await fetchStats()
})
</script>

<template>
  <div class="dashboard-page">
    <div class="page-header">
      <div>
        <h1>🚗 Car Dashboard</h1>
        <p>Manage your dealership cars, brands, categories, and dealers.</p>
      </div>

      <button class="export-btn" @click="onExportExcel" type="button">
        Export Excel
      </button>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <span>🚗</span>
        <div>
          <h3>{{ stats?.count || 0 }}</h3>
          <p>Total Cars</p>
        </div>
      </div>

      <div class="stat-card">
        <span>🏷️</span>
        <div>
          <h3>{{ brands.length }}</h3>
          <p>Brands</p>
        </div>
      </div>

      <div class="stat-card">
        <span>📂</span>
        <div>
          <h3>{{ categories.length }}</h3>
          <p>Categories</p>
        </div>
      </div>

      <div class="stat-card">
        <span>🏢</span>
        <div>
          <h3>{{ dealers.length }}</h3>
          <p>Dealers</p>
        </div>
      </div>
    </div>

    <form
      v-if="userStore.user?.role === 'admin'"
      class="add-card"
      @submit.prevent.stop="onCarAdd"
      novalidate
    >
      <h2>Add New Car</h2>

      <div class="add-grid">
        <input class="form-control" v-model="carToAdd.model" placeholder="Car model" />
        <input class="form-control" type="number" v-model="carToAdd.year" placeholder="Year" />

        <select class="form-select" v-model.number="carToAdd.brand">
          <option :value="null">Select Brand</option>
          <option v-for="b in brands" :key="b.id" :value="b.id">
            {{ b.name }}
          </option>
        </select>

        <select class="form-select" v-model.number="carToAdd.category">
          <option :value="null">Select Category</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">
            {{ c.name }}
          </option>
        </select>

        <select class="form-select" v-model.number="carToAdd.dealer">
          <option :value="null">Select Dealer</option>
          <option v-for="d in dealers" :key="d.id" :value="d.id">
            {{ d.name }}
          </option>
        </select>

        <input
          class="form-control"
          type="file"
          ref="carsPictureRef"
          @change="carsAddPictureChange"
        />

        <button class="primary-btn">Add Car</button>
      </div>

      <img v-if="carAddImageUrl" :src="carAddImageUrl" class="preview-img" />
    </form>

    <div class="filter-card">
      <h2>Search & Filter</h2>

      <div class="filter-grid">
        <input class="form-control" v-model="modelFilter" placeholder="Search by model" />
        <input class="form-control" v-model="brandFilter" placeholder="Search by brand" />
        <input class="form-control" v-model="categoryFilter" placeholder="Search by category" />

        <select class="form-select" v-model="dealerFilter">
          <option :value="0">All Dealers</option>
          <option v-for="d in dealers" :key="d.id" :value="d.id">
            {{ d.name }}
          </option>
        </select>
      </div>
    </div>

    <div class="cars-grid">
      <div v-for="item in carsFiltered" :key="item.id" class="car-card">
        <div class="car-images">
          <img v-if="item.picture" :src="item.picture" />

          <img
            v-for="img in item.images"
            :key="img.id"
            :src="img.image"
          />

          <div v-if="!item.picture && (!item.images || item.images.length === 0)" class="no-image">
            🚗
          </div>
        </div>

        <div class="car-info">
          <h3>{{ item.model }}</h3>

          <p>
            <strong>Brand:</strong>
            {{ brandById[item.brand]?.name || "N/A" }}
          </p>

          <p>
            <strong>Category:</strong>
            {{ categoryById[item.category]?.name || "N/A" }}
          </p>

          <p>
            <strong>Dealer:</strong>
            {{ dealerById[item.dealer]?.name || "N/A" }}
          </p>

          <p>
            <strong>Year:</strong>
            {{ item.year || "N/A" }}
          </p>
        </div>

        <div class="card-actions">
          <button
            v-if="userStore.user?.role === 'customer'"
            class="primary-btn"
            @click="onPurchaseClick(item)"
          >
            Purchase
          </button>

          <template v-if="userStore.user?.role === 'admin'">
            <button
              class="edit-btn"
              @click="onCarEditClick(item)"
              data-bs-toggle="modal"
              data-bs-target="#editCarModal"
            >
              Edit
            </button>

            <button class="delete-btn" @click="onRemoveClick(item)">
              Delete
            </button>
          </template>
        </div>
      </div>
    </div>

    <div
      v-if="userStore.user?.role === 'admin'"
      class="modal fade"
      id="editCarModal"
      tabindex="-1"
    >
      <div class="modal-dialog">
        <div class="modal-content rounded-4">
          <div class="modal-header">
            <h5 class="modal-title">Edit Car</h5>
            <button class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <div class="form-floating mb-3">
              <input class="form-control" v-model="carToEdit.model" placeholder="Model" />
              <label>Model</label>
            </div>

            <div class="form-floating">
              <input type="number" class="form-control" v-model="carToEdit.year" placeholder="Year" />
              <label>Year</label>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">
              Close
            </button>

            <button
              class="btn btn-primary"
              data-bs-dismiss="modal"
              @click="onUpdateCar"
            >
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-page {
  padding: 32px;
  background: #f8fafc;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
}

.page-header p {
  color: #64748b;
  margin: 6px 0 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  padding: 22px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
}

.stat-card span {
  font-size: 30px;
  background: #eff6ff;
  padding: 14px;
  border-radius: 14px;
}

.stat-card h3 {
  margin: 0;
  font-size: 26px;
  font-weight: 800;
  color: #0f172a;
}

.stat-card p {
  margin: 4px 0 0;
  color: #64748b;
}

.add-card,
.filter-card {
  background: white;
  padding: 24px;
  border-radius: 18px;
  margin-bottom: 24px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
}

.add-card h2,
.filter-card h2 {
  font-size: 20px;
  font-weight: 800;
  margin-bottom: 18px;
  color: #0f172a;
}

.add-grid,
.filter-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

.primary-btn,
.export-btn,
.edit-btn,
.delete-btn {
  border: none;
  border-radius: 12px;
  padding: 12px 18px;
  font-weight: 700;
  cursor: pointer;
}

.primary-btn,
.export-btn {
  background: #2563eb;
  color: white;
}

.primary-btn:hover,
.export-btn:hover {
  background: #1d4ed8;
}

.edit-btn {
  background: #16a34a;
  color: white;
}

.delete-btn {
  background: #dc2626;
  color: white;
}

.preview-img {
  margin-top: 16px;
  max-height: 90px;
  border-radius: 12px;
}

.cars-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
}

.car-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 12px 35px rgba(15, 23, 42, 0.1);
  transition: 0.2s;
}

.car-card:hover {
  transform: translateY(-4px);
}

.car-images {
  height: 190px;
  background: #e2e8f0;
  display: flex;
  gap: 6px;
  overflow: hidden;
}

.car-images img {
  width: 100%;
  object-fit: cover;
}

.no-image {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 54px;
}

.car-info {
  padding: 20px;
}

.car-info h3 {
  font-size: 20px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 14px;
}

.car-info p {
  margin: 7px 0;
  color: #475569;
}

.card-actions {
  padding: 0 20px 20px;
  display: flex;
  gap: 10px;
}

@media (max-width: 1100px) {
  .stats-grid,
  .cars-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .add-grid,
  .filter-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 700px) {
  .dashboard-page {
    padding: 18px;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .stats-grid,
  .cars-grid,
  .add-grid,
  .filter-grid {
    grid-template-columns: 1fr;
  }
}
</style>