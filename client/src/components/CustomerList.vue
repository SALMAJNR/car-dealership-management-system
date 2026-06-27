<script setup>
import { ref, onBeforeMount } from "vue"
import axios from "axios"
import Cookies from "js-cookie"
import { useUserStore } from "@/stores/user"

const userStore = useUserStore()

const customers = ref([])
const customerToEdit = ref({})

async function fetchCustomers() {

  const r = await axios.get("/api/customers/")

  customers.value = r.data
}

async function onRemoveClick(customer) {

  await axios.delete(
    `/api/customers/${customer.id}/`
  )

  await fetchCustomers()
}

function onCustomerEditClick(customer) {

  customerToEdit.value = {
    ...customer
  }
}

async function onUpdateCustomer() {

  await axios.put(
    `/api/customers/${customerToEdit.value.id}/`,
    {
      ...customerToEdit.value
    }
  )

  customerToEdit.value = {}

  await fetchCustomers()
}

onBeforeMount(async () => {

  axios.defaults.withCredentials = true

  axios.defaults.headers.common["X-CSRFToken"] =
    Cookies.get("csrftoken")

  await fetchCustomers()

})
</script>

<template>

<h3 class="mb-3">
  Customers
</h3>

<div
  v-for="item in customers"
  :key="item.id"
  class="row align-items-center border p-2 mb-2"
>

  <div class="col">

    {{ item.user }} -
    {{ item.purchased_car }}

  </div>

  <div
    v-if="userStore.user?.role === 'admin'"
    class="col-auto d-flex gap-2"
  >

    <button
      class="btn btn-success"
      @click="onCustomerEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editCustomerModal"
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
  id="editCustomerModal"
  tabindex="-1"
>

  <div class="modal-dialog">

    <div class="modal-content">

      <div class="modal-header">

        <h5 class="modal-title">
          Edit Customer
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
            v-model="customerToEdit.user"
            placeholder="Username"
          >

          <label>
            Username
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
          @click="onUpdateCustomer"
        >
          Save
        </button>

      </div>

    </div>

  </div>

</div>

</template>