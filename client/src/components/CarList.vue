<script setup>
import { ref, onBeforeMount, computed, watch } from "vue"
import axios from "axios"
import Cookies from "js-cookie"
import { useUserStore } from "@/stores/user"

import NotificationToast from "./dashboard/NotificationToast.vue"
import DashboardStats from "./dashboard/DashboardStats.vue"
import DashboardCharts from "./dashboard/DashboardCharts.vue"
import SearchFilters from "./dashboard/SearchFilters.vue"
import PaginationControls from "./dashboard/PaginationControls.vue"
import CarCard from "./dashboard/CarCard.vue"
import AddCarForm from "./dashboard/AddCarForm.vue"
import EditCarModal from "./dashboard/EditCarModal.vue"

const userStore = useUserStore()

const cars = ref([])
const brands = ref([])
const categories = ref([])
const dealers = ref([])
const stats = ref(null)

const carToAdd = ref({
  model: "",
  brand: null,
  category: null,
  dealer: null,
  year: null
})

const carToEdit = ref({})
const carsPictureRef = ref(null)
const carAddImageUrl = ref("")

const modelFilter = ref("")
const brandFilter = ref("")
const categoryFilter = ref("")
const dealerFilter = ref(0)

const debouncedModelFilter = ref("")
const debouncedBrandFilter = ref("")
const debouncedCategoryFilter = ref("")

const currentPage = ref(1)
const itemsPerPage = ref(6)

const notification = ref({
  show: false,
  message: "",
  type: "success"
})

let debounceTimer = null

watch(
  [modelFilter, brandFilter, categoryFilter, dealerFilter],
  () => {
    clearTimeout(debounceTimer)

    debounceTimer = setTimeout(() => {
      debouncedModelFilter.value = modelFilter.value
      debouncedBrandFilter.value = brandFilter.value
      debouncedCategoryFilter.value = categoryFilter.value
      currentPage.value = 1
    }, 300)
  }
)

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

const brandById = computed(() => {
  const result = {}
  for (const brand of brands.value) result[brand.id] = brand
  return result
})

const categoryById = computed(() => {
  const result = {}
  for (const category of categories.value) result[category.id] = category
  return result
})

const dealerById = computed(() => {
  const result = {}
  for (const dealer of dealers.value) result[dealer.id] = dealer
  return result
})

const carsFiltered = computed(() => {
  const modelCI = debouncedModelFilter.value.toLowerCase()
  const brandCI = debouncedBrandFilter.value.toLowerCase()
  const categoryCI = debouncedCategoryFilter.value.toLowerCase()

  return cars.value.filter(car =>
    (!debouncedModelFilter.value ||
      car.model?.toLowerCase().includes(modelCI)) &&

    (!debouncedBrandFilter.value ||
      brandById.value[car.brand]?.name?.toLowerCase().includes(brandCI)) &&

    (!debouncedCategoryFilter.value ||
      categoryById.value[car.category]?.name?.toLowerCase().includes(categoryCI)) &&

    (!dealerFilter.value || car.dealer == dealerFilter.value)
  )
})

const totalPages = computed(() => {
  return Math.ceil(carsFiltered.value.length / itemsPerPage.value) || 1
})

const paginatedCars = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value

  return carsFiltered.value.slice(start, end)
})

const brandChart = computed(() => {
  return brands.value.map(brand => ({
    name: brand.name,
    count: cars.value.filter(car => car.brand === brand.id).length
  }))
})

const categoryChart = computed(() => {
  return categories.value.map(category => ({
    name: category.name,
    count: cars.value.filter(car => car.category === category.id).length
  }))
})

const dealerChart = computed(() => {
  return dealers.value.map(dealer => ({
    name: dealer.name,
    count: cars.value.filter(car => car.dealer === dealer.id).length
  }))
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

async function refreshData() {
  await fetchCars()
  await fetchStats()
}

async function onCarAdd() {
  try {
    const formData = new FormData()

    if (carsPictureRef.value?.files?.[0]) {
      formData.append("picture", carsPictureRef.value.files[0])
    }

    formData.append("model", carToAdd.value.model)
    formData.append("brand", carToAdd.value.brand)
    formData.append("category", carToAdd.value.category)
    formData.append("dealer", carToAdd.value.dealer)
    formData.append("year", carToAdd.value.year)

    await axios.post("/api/cars/", formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    })

    carToAdd.value = {
      model: "",
      brand: null,
      category: null,
      dealer: null,
      year: null
    }

    carsPictureRef.value = null
    carAddImageUrl.value = ""

    await refreshData()

    notify("Car added successfully")
  } catch (error) {
    notify("Could not add car", "error")
  }
}

function onImageChange(event) {
  const fileInput = event.target
  carsPictureRef.value = fileInput

  if (fileInput.files?.[0]) {
    carAddImageUrl.value = URL.createObjectURL(fileInput.files[0])
  }
}

function onCarEditClick(car) {
  carToEdit.value = { ...car }
}

async function onUpdateCar() {
  try {
    await axios.put(`/api/cars/${carToEdit.value.id}/`, {
      ...carToEdit.value
    })

    await fetchCars()

    notify("Car updated successfully")
  } catch (error) {
    notify("Could not update car", "error")
  }
}

async function onRemoveClick(car) {
  const confirmed = confirm(`Delete ${car.model}?`)

  if (!confirmed) return

  try {
    await axios.delete(`/api/cars/${car.id}/`)
    await refreshData()

    notify("Car deleted successfully")
  } catch (error) {
    notify("Could not delete car", "error")
  }
}

async function onPurchaseClick(car) {
  try {
    await axios.post("/api/customers/bind-car/", {
      car_id: car.id
    })

    notify("Car purchased successfully")
  } catch (error) {
    notify("Could not purchase car", "error")
  }
}

function onExportExcel() {
  window.open("http://localhost:8000/api/cars/export_excel/")
}

function clearFilters() {
  modelFilter.value = ""
  brandFilter.value = ""
  categoryFilter.value = ""
  dealerFilter.value = 0
  debouncedModelFilter.value = ""
  debouncedBrandFilter.value = ""
  debouncedCategoryFilter.value = ""
  currentPage.value = 1
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

function previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--
  }
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
  <section class="cars-page">
    <NotificationToast
      :show="notification.show"
      :message="notification.message"
      :type="notification.type"
    />

    <div class="page-header">
      <div>
        <span class="eyebrow">Dashboard</span>
        <h1>Car Inventory</h1>
        <p>
          Manage cars, brands, categories, dealers, images, exports, and customer purchases.
        </p>
      </div>

      <button class="export-btn" @click="onExportExcel">
        Export Excel
      </button>
    </div>

    <DashboardStats
      :total-cars="stats?.count || 0"
      :brands="brands.length"
      :categories="categories.length"
      :dealers="dealers.length"
    />

    <DashboardCharts
      :brand-data="brandChart"
      :category-data="categoryChart"
      :dealer-data="dealerChart"
    />

    <AddCarForm
      :role="userStore.user?.role"
      :car="carToAdd"
      :brands="brands"
      :categories="categories"
      :dealers="dealers"
      :image-preview="carAddImageUrl"
      @add="onCarAdd"
      @image-change="onImageChange"
      @update:model="carToAdd.model = $event"
      @update:year="carToAdd.year = $event"
      @update:brand="carToAdd.brand = $event"
      @update:category="carToAdd.category = $event"
      @update:dealer="carToAdd.dealer = $event"
    />

    <SearchFilters
      v-model:modelFilter="modelFilter"
      v-model:brandFilter="brandFilter"
      v-model:categoryFilter="categoryFilter"
      v-model:dealerFilter="dealerFilter"
      :dealers="dealers"
      @clear="clearFilters"
    />

    <div class="results-header">
      <h2>Available Cars</h2>
      <p>
        Showing {{ paginatedCars.length }} of {{ carsFiltered.length }} cars
      </p>
    </div>

    <div v-if="paginatedCars.length" class="cars-grid">
      <CarCard
        v-for="car in paginatedCars"
        :key="car.id"
        :car="car"
        :brand="brandById[car.brand]?.name"
        :category="categoryById[car.category]?.name"
        :dealer="dealerById[car.dealer]?.name"
        :role="userStore.user?.role"
        @edit="onCarEditClick"
        @delete="onRemoveClick"
        @purchase="onPurchaseClick"
      />
    </div>

    <div v-else class="empty-state">
      <div>🚗</div>
      <h3>No cars found</h3>
      <p>Try changing your search filters or add a new car.</p>
    </div>

    <PaginationControls
      :current-page="currentPage"
      :total-pages="totalPages"
      @previous="previousPage"
      @next="nextPage"
    />

    <EditCarModal
      :car="carToEdit"
      @save="onUpdateCar"
      @update:model="carToEdit.model = $event"
      @update:year="carToEdit.year = $event"
    />
  </section>
</template>

<style scoped>
.cars-page {
  min-height: 100vh;
  padding-bottom: 40px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  gap: 22px;
  align-items: center;
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
  max-width: 680px;
  margin: 0;
  font-weight: 600;
}

.export-btn {
  border: none;
  background: #2563eb;
  color: white;
  padding: 13px 18px;
  border-radius: 14px;
  font-weight: 900;
  box-shadow: 0 12px 30px rgba(37, 99, 235, 0.25);
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 18px;
  margin-bottom: 18px;
}

.results-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 950;
  color: #0f172a;
}

.results-header p {
  margin: 0;
  color: #64748b;
  font-weight: 700;
}

.cars-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
}

.empty-state {
  background: white;
  border-radius: 24px;
  padding: 50px;
  text-align: center;
  box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
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
:global(.dark-mode) .results-header h2,
:global(.dark-mode) .empty-state h3 {
  color: #e5e7eb;
}

:global(.dark-mode) .empty-state {
  background: #0f172a;
}

@media (max-width: 1050px) {
  .cars-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }
}

@media (max-width: 700px) {
  .cars-grid {
    grid-template-columns: 1fr;
  }

  .page-header h1 {
    font-size: 30px;
  }

  .results-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .export-btn {
    width: 100%;
  }
}
</style>