<script setup>
import { ref, onBeforeMount } from "vue"
import axios from "axios"
import Cookies from "js-cookie"
import { useUserStore } from "@/stores/user"

const userStore = useUserStore()

const dealers = ref([])

const dealerToAdd = ref({
  name: "",
  city: ""
})

const dealerToEdit = ref({})

async function fetchDealers() {
  const r = await axios.get("/api/dealers/")
  dealers.value = r.data
}

async function onDealerAdd() {
  await axios.post("/api/dealers/", dealerToAdd.value)

  dealerToAdd.value = {
    name: "",
    city: ""
  }

  await fetchDealers()
}

async function onRemoveClick(dealer) {
  await axios.delete(`/api/dealers/${dealer.id}/`)
  await fetchDealers()
}

function onDealerEditClick(dealer) {
  dealerToEdit.value = { ...dealer }
}

async function onUpdateDealer() {
  await axios.put(`/api/dealers/${dealerToEdit.value.id}/`, {
    ...dealerToEdit.value
  })

  dealerToEdit.value = {}

  await fetchDealers()
}

onBeforeMount(async () => {
  axios.defaults.withCredentials = true

  axios.defaults.headers.common["X-CSRFToken"] =
    Cookies.get("csrftoken")

  await fetchDealers()
})
</script>

<template>

<h3 class="mb-3">
  Dealers
</h3>

<form
  v-if="userStore.user?.role === 'admin'"
  @submit.prevent="onDealerAdd"
  class="mb-3"
>

  <div class="row">

    <div class="col">
      <input
        class="form-control"
        v-model="dealerToAdd.name"
        placeholder="Name"
      >
    </div>

    <div class="col">
      <input
        class="form-control"
        v-model="dealerToAdd.city"
        placeholder="City"
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
  v-for="item in dealers"
  :key="item.id"
  class="row align-items-center border p-2 mb-2"
>

  <div class="col">
    {{ item.name }} ({{ item.city }})
  </div>

  <div
    v-if="userStore.user?.role === 'admin'"
    class="col-auto d-flex gap-2"
  >

    <button
      class="btn btn-success"
      @click="onDealerEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editDealerModal"
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
  id="editDealerModal"
  tabindex="-1"
>
  <div class="modal-dialog">
    <div class="modal-content">

      <div class="modal-header">

        <h5 class="modal-title">
          Edit Dealer
        </h5>

        <button
          class="btn-close"
          data-bs-dismiss="modal"
        ></button>

      </div>

      <div class="modal-body">

        <div class="form-floating mb-3">

          <input
            class="form-control"
            v-model="dealerToEdit.name"
            placeholder="Name"
          >

          <label>Name</label>

        </div>

        <div class="form-floating">

          <input
            class="form-control"
            v-model="dealerToEdit.city"
            placeholder="City"
          >

          <label>City</label>

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
          @click="onUpdateDealer"
        >
          Save
        </button>

      </div>

    </div>
  </div>
</div>

</template>