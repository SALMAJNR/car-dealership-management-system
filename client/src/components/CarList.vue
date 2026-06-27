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

  for (let b of brands.value) {
    result[b.id] = b
  }

  return result
})

const categoryById = computed(() => {

  const result = {}

  for (let c of categories.value) {
    result[c.id] = c
  }

  return result
})

const dealerById = computed(() => {

  const result = {}

  for (let d of dealers.value) {
    result[d.id] = d
  }

  return result
})

const carsFiltered = computed(() => {

  const modelCI = modelFilter.value.toLowerCase()
  const brandCI = brandFilter.value.toLowerCase()
  const categoryCI = categoryFilter.value.toLowerCase()

  return cars.value.filter(item =>

    (!modelFilter.value ||
      item.model.toLowerCase().includes(modelCI)) &&

    (!brandFilter.value ||
      brandById.value[item.brand]?.name
        .toLowerCase()
        .includes(brandCI)) &&

    (!categoryFilter.value ||
      categoryById.value[item.category]?.name
        .toLowerCase()
        .includes(categoryCI)) &&

    (!dealerFilter.value ||
      item.dealer == dealerFilter.value)

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

    formData.append(
      "picture",
      carsPictureRef.value.files[0]
    )
  }

  formData.append("model", carToAdd.value.model)
  formData.append("brand", carToAdd.value.brand)
  formData.append("category", carToAdd.value.category)
  formData.append("dealer", carToAdd.value.dealer)
  formData.append("year", carToAdd.value.year)

  await axios.post(
    "/api/cars/",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    }
  )

  carToAdd.value = {
    model: "",
    brand: null,
    category: null,
    dealer: null,
    year: null
  }

  carAddImageUrl.value = null

  await fetchCars()
}

async function onRemoveClick(car) {

  await axios.delete(`/api/cars/${car.id}/`)

  await fetchCars()
}

function onCarEditClick(car) {

  carToEdit.value = {
    ...car
  }
}

async function onUpdateCar() {

  await axios.put(
    `/api/cars/${carToEdit.value.id}/`,
    {
      ...carToEdit.value
    }
  )

  carToEdit.value = {}

  await fetchCars()
}

async function onPurchaseClick(car) {

  await axios.post(
    "/api/customers/bind-car/",
    {
      car_id: car.id
    }
  )

  alert("Car purchased successfully")
}

function carsAddPictureChange() {

  carAddImageUrl.value =
    URL.createObjectURL(
      carsPictureRef.value.files[0]
    )
}

function onExportExcel() {

  window.open(
    "http://127.0.0.1:8000/api/cars/export_excel/"
  )
}

onBeforeMount(async () => {

  axios.defaults.withCredentials = true

  axios.defaults.headers.common["X-CSRFToken"] =
    Cookies.get("csrftoken")

  await fetchCars()
  await fetchBrands()
  await fetchCategories()
  await fetchDealers()
  await fetchStats()
})
</script>

<template>

<form
  v-if="userStore.user?.role === 'admin'"
  @submit.prevent.stop="onCarAdd"
  novalidate
>

  <div v-if="stats" class="mb-2">

    <h4>Stats</h4>

    <p>
      Total Cars: {{ stats.count }}
    </p>

    <button
      class="btn btn-success mb-3"
      @click="onExportExcel"
      type="button"
    >
      Export Excel
    </button>

  </div>

  <div class="row">

    <div class="col-auto">

      <input
        class="form-control"
        type="file"
        ref="carsPictureRef"
        @change="carsAddPictureChange"
      >

    </div>

    <div class="col-auto">

      <img
        :src="carAddImageUrl"
        style="max-height:60px;"
      >

    </div>

    <div class="col">

      <input
        class="form-control"
        v-model="carToAdd.model"
        placeholder="Model"
      >

    </div>

    <div class="col">

      <input
        class="form-control"
        type="number"
        v-model="carToAdd.year"
        placeholder="Year"
      >

    </div>

    <div class="col-auto">

      <select
        class="form-select"
        v-model.number="carToAdd.brand"
      >

        <option :value="null">
          Select Brand
        </option>

        <option
          v-for="b in brands"
          :key="b.id"
          :value="b.id"
        >
          {{ b.name }}
        </option>

      </select>

    </div>

    <div class="col-auto">

      <select
        class="form-select"
        v-model.number="carToAdd.category"
      >

        <option :value="null">
          Select Category
        </option>

        <option
          v-for="c in categories"
          :key="c.id"
          :value="c.id"
        >
          {{ c.name }}
        </option>

      </select>

    </div>

    <div class="col-auto">

      <select
        class="form-select"
        v-model.number="carToAdd.dealer"
      >

        <option :value="null">
          Select Dealer
        </option>

        <option
          v-for="d in dealers"
          :key="d.id"
          :value="d.id"
        >
          {{ d.name }}
        </option>

      </select>

    </div>

    <div class="col-auto">

      <button class="btn btn-primary">
        Add
      </button>

    </div>

  </div>

</form>

<div class="row mb-2 mt-3">

  <div class="col">

    <input
      class="form-control"
      v-model="modelFilter"
      placeholder="Model"
    >

  </div>

  <div class="col">

    <input
      class="form-control"
      v-model="brandFilter"
      placeholder="Brand"
    >

  </div>

  <div class="col">

    <input
      class="form-control"
      v-model="categoryFilter"
      placeholder="Category"
    >

  </div>

  <div class="col">

    <select
      class="form-select"
      v-model="dealerFilter"
    >

      <option :value="0">
        All
      </option>

      <option
        v-for="d in dealers"
        :key="d.id"
        :value="d.id"
      >
        {{ d.name }}
      </option>

    </select>

  </div>

</div>

<div
  v-for="item in carsFiltered"
  :key="item.id"
  class="row align-items-center border p-2 mt-1"
>

  <div class="col">

    {{ item.model }} -
    {{ brandById[item.brand]?.name }} -
    {{ categoryById[item.category]?.name }} -
    {{ dealerById[item.dealer]?.name }}

  </div>

  <div class="col-auto d-flex gap-2">

    <img
      v-if="item.picture"
      :src="item.picture"
      style="max-height:60px;"
    >

    <img
      v-for="img in item.images"
      :key="img.id"
      :src="img.image"
      style="max-height:60px;"
    >

  </div>

  <div
    v-if="userStore.user?.role === 'customer'"
    class="col-auto"
  >

    <button
      class="btn btn-primary"
      @click="onPurchaseClick(item)"
    >
      Purchase
    </button>

  </div>

  <div
    v-if="userStore.user?.role === 'admin'"
    class="col-auto d-flex gap-2"
  >

    <button
      class="btn btn-success"
      @click="onCarEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editCarModal"
    >
      <i class="bi bi-pen-fill"></i>
    </button>

    <button
      class="btn btn-danger"
      @click="onRemoveClick(item)"
    >
      <i class="bi bi-x"></i>
    </button>

  </div>

</div>

<div
  v-if="userStore.user?.role === 'admin'"
  class="modal fade"
  id="editCarModal"
  tabindex="-1"
>

  <div class="modal-dialog">

    <div class="modal-content">

      <div class="modal-header">

        <h5 class="modal-title">
          Edit Car
        </h5>

        <button
          class="btn-close"
          data-bs-dismiss="modal"
        ></button>

      </div>

      <div class="modal-body">

        <div class="row">

          <div class="col">

            <div class="form-floating">

              <input
                class="form-control"
                v-model="carToEdit.model"
                placeholder="Model"
              >

              <label>
                Model
              </label>

            </div>

          </div>

          <div class="col">

            <div class="form-floating">

              <input
                type="number"
                class="form-control"
                v-model="carToEdit.year"
                placeholder="Year"
              >

              <label>
                Year
              </label>

            </div>

          </div>

        </div>

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
          @click="onUpdateCar"
        >
          Save
        </button>

      </div>

    </div>

  </div>

</div>

</template>