<script setup>
import { ref, onBeforeMount } from "vue"
import axios from "axios"
import Cookies from "js-cookie"
import { useUserStore } from "@/stores/user"

const userStore = useUserStore()

const brands = ref([])

const brandToAdd = ref({
  name: ""
})

const brandToEdit = ref({})

async function fetchBrands() {
  const r = await axios.get("/api/brands/")
  brands.value = r.data
}

async function onBrandAdd() {
  await axios.post("/api/brands/", brandToAdd.value)

  brandToAdd.value = {
    name: ""
  }

  await fetchBrands()
}

async function onRemoveClick(brand) {
  await axios.delete(`/api/brands/${brand.id}/`)
  await fetchBrands()
}

function onBrandEditClick(brand) {
  brandToEdit.value = { ...brand }
}

async function onUpdateBrand() {
  await axios.put(`/api/brands/${brandToEdit.value.id}/`, {
    ...brandToEdit.value
  })

  brandToEdit.value = {}

  await fetchBrands()
}

onBeforeMount(async () => {
  axios.defaults.withCredentials = true

  axios.defaults.headers.common["X-CSRFToken"] =
    Cookies.get("csrftoken")

  await fetchBrands()
})
</script>

<template>

<h3 class="mb-3">
  Brands
</h3>

<form
  v-if="userStore.user?.role === 'admin'"
  @submit.prevent="onBrandAdd"
  class="mb-3"
>

  <div class="row">

    <div class="col">
      <input
        class="form-control"
        v-model="brandToAdd.name"
        placeholder="Brand name"
      >
    </div>

    <div class="col-auto">
      <button class="btn btn-primary">
        Add
      </button>
    </div>

  </div>

</form>

<div
  v-for="item in brands"
  :key="item.id"
  class="row align-items-center border p-2 mb-2"
>

  <div class="col">
    {{ item.name }}
  </div>

  <div
    v-if="userStore.user?.role === 'admin'"
    class="col-auto d-flex gap-2"
  >

    <button
      class="btn btn-success"
      @click="onBrandEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editBrandModal"
    >
      Edit
    </button>

    <button
      class="btn btn-danger"
      @click="onRemoveClick(item)"
    >
      Delete
    </button>

  </div>

</div>

<div
  v-if="userStore.user?.role === 'admin'"
  class="modal fade"
  id="editBrandModal"
  tabindex="-1"
>
  <div class="modal-dialog">
    <div class="modal-content">

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

        <div class="form-floating">

          <input
            class="form-control"
            v-model="brandToEdit.name"
            placeholder="Brand"
          >

          <label>Brand</label>

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
          @click="onUpdateBrand"
        >
          Save
        </button>

      </div>

    </div>
  </div>
</div>

</template>