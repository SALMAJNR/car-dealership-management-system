<script setup>
import { ref, onBeforeMount } from "vue"
import axios from "axios"
import Cookies from "js-cookie"
import { useUserStore } from "@/stores/user"

const userStore = useUserStore()

const categories = ref([])

const categoryToAdd = ref({
  name: ""
})

const categoryToEdit = ref({})

async function fetchCategories() {
  const r = await axios.get("/api/categories/")
  categories.value = r.data
}

async function onCategoryAdd() {
  await axios.post("/api/categories/", categoryToAdd.value)

  categoryToAdd.value = {
    name: ""
  }

  await fetchCategories()
}

async function onRemoveClick(category) {
  await axios.delete(`/api/categories/${category.id}/`)
  await fetchCategories()
}

function onCategoryEditClick(category) {
  categoryToEdit.value = { ...category }
}

async function onUpdateCategory() {
  await axios.put(`/api/categories/${categoryToEdit.value.id}/`, {
    ...categoryToEdit.value
  })

  categoryToEdit.value = {}

  await fetchCategories()
}

onBeforeMount(async () => {
  axios.defaults.withCredentials = true
  axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken")

  await fetchCategories()
})
</script>

<template>

<h3 class="mb-3">Categories</h3>

<form
  v-if="userStore.user?.role === 'admin'"
  @submit.prevent="onCategoryAdd"
  class="mb-3"
>
  <div class="row">

    <div class="col">
      <input
        class="form-control"
        v-model="categoryToAdd.name"
        placeholder="Category name"
      />
    </div>

    <div class="col-auto">
      <button class="btn btn-primary">
        Add
      </button>
    </div>

  </div>
</form>


<div
  v-for="item in categories"
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
      @click="onCategoryEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editCategoryModal"
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
  id="editCategoryModal"
  tabindex="-1"
>
  <div class="modal-dialog">
    <div class="modal-content">

      <div class="modal-header">
        <h5 class="modal-title">
          Edit Category
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
            v-model="categoryToEdit.name"
            placeholder="Category"
          />

          <label>
            Category
          </label>

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
          @click="onUpdateCategory"
        >
          Save
        </button>

      </div>

    </div>
  </div>
</div>

</template>