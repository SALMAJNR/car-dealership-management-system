<script setup>
import { ref, onBeforeMount, computed } from "vue"
import axios from "axios"
import Cookies from "js-cookie"
import { useUserStore } from "@/stores/user"

import NotificationToast from "./dashboard/NotificationToast.vue"

const userStore = useUserStore()

const customers = ref([])
const search = ref("")
const customerToEdit = ref({})

const notification = ref({
  show: false,
  message: "",
  type: "success"
})

const filteredCustomers = computed(() => {
  const keyword = search.value.toLowerCase()

  return customers.value.filter(customer =>
    String(customer.user || "").toLowerCase().includes(keyword) ||
    String(customer.purchased_car || "").toLowerCase().includes(keyword)
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

async function fetchCustomers() {
  const r = await axios.get("/api/customers/")
  customers.value = r.data
}

async function onRemoveClick(customer) {
  const confirmed = confirm("Delete this customer record?")

  if (!confirmed) return

  try {
    await axios.delete(`/api/customers/${customer.id}/`)
    await fetchCustomers()

    notify("Customer deleted successfully")
  } catch (error) {
    notify("Could not delete customer", "error")
  }
}

function onCustomerEditClick(customer) {
  customerToEdit.value = { ...customer }
}

async function onUpdateCustomer() {
  try {
    await axios.put(`/api/customers/${customerToEdit.value.id}/`, {
      ...customerToEdit.value
    })

    customerToEdit.value = {}

    await fetchCustomers()

    notify("Customer updated successfully")
  } catch (error) {
    notify("Could not update customer", "error")
  }
}

onBeforeMount(async () => {
  axios.defaults.withCredentials = true
  axios.defaults.headers.common["X-CSRFToken"] =
    Cookies.get("csrftoken")

  await fetchCustomers()
})
</script>

<template>
  <section class="customer-page">
    <NotificationToast
      :show="notification.show"
      :message="notification.message"
      :type="notification.type"
    />

    <div class="summary-card">
      <div>
        <span class="eyebrow">Customers</span>
        <h1>Customer Records</h1>
        <p>
          View customers and purchased vehicles linked to the dealership system.
        </p>
      </div>

      <div class="summary-box">
        <span>👤</span>
        <div>
          <strong>{{ customers.length }}</strong>
          <p>Total Customers</p>
        </div>
      </div>
    </div>

    <div class="search-card">
      <div>
        <h2>Search Customers</h2>
        <p>Search by user or purchased car.</p>
      </div>

      <input
        v-model="search"
        placeholder="Search customer or car"
      />
    </div>

    <div class="list-header">
      <h2>Customer List</h2>
      <p>Showing {{ filteredCustomers.length }} of {{ customers.length }}</p>
    </div>

    <div
      v-if="filteredCustomers.length"
      class="customer-grid"
    >
      <div
        v-for="item in filteredCustomers"
        :key="item.id"
        class="customer-card"
      >
        <div class="customer-top">
          <div class="avatar">
            👤
          </div>

          <div>
            <h3>
              Customer #{{ item.id }}
            </h3>
            <p>Customer profile</p>
          </div>
        </div>

        <div class="info-list">
          <div>
            <span>User</span>
            <strong>{{ item.user || "N/A" }}</strong>
          </div>

          <div>
            <span>Purchased Car</span>
            <strong>{{ item.purchased_car || "N/A" }}</strong>
          </div>
        </div>

        <div
          v-if="userStore.user?.role === 'admin'"
          class="actions"
        >
          <button
            class="edit-btn"
            @click="onCustomerEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editCustomerModal"
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

    <div
      v-else
      class="empty-state"
    >
      <div>👤</div>
      <h3>No customers found</h3>
      <p>No customer purchase records are available yet.</p>
    </div>

    <div
      v-if="userStore.user?.role === 'admin'"
      class="modal fade"
      id="editCustomerModal"
      tabindex="-1"
    >
      <div class="modal-dialog">
        <div class="modal-content rounded-4">
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
            <input
              class="form-control mb-3"
              v-model="customerToEdit.user"
              placeholder="Username"
            />

            <input
              class="form-control"
              v-model="customerToEdit.purchased_car"
              placeholder="Purchased car"
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
              @click="onUpdateCustomer"
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
.customer-page {
  min-height: 100vh;
  padding-bottom: 40px;
}

.summary-card,
.search-card,
.customer-card,
.empty-state {
  background: white;
  border-radius: 24px;
  box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
}

.summary-card {
  padding: 26px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: center;
}

.eyebrow {
  color: #2563eb;
  font-weight: 900;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.08em;
}

.summary-card h1 {
  margin: 6px 0;
  font-size: 34px;
  font-weight: 950;
  color: #0f172a;
}

.summary-card p {
  color: #64748b;
  margin: 0;
  font-weight: 600;
}

.summary-box {
  min-width: 230px;
  background: #f8fafc;
  border-radius: 20px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.summary-box span,
.avatar {
  width: 54px;
  height: 54px;
  border-radius: 16px;
  background: #eff6ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
}

.summary-box strong {
  font-size: 28px;
  font-weight: 950;
  color: #0f172a;
}

.summary-box p {
  margin: 0;
}

.search-card {
  padding: 24px;
  margin-bottom: 24px;
}

.search-card h2,
.list-header h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 950;
  color: #0f172a;
}

.search-card p,
.list-header p {
  margin: 4px 0 0;
  color: #64748b;
  font-weight: 600;
}

input {
  margin-top: 18px;
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

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 16px;
  margin-bottom: 18px;
}

.customer-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.customer-card {
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  transition: 0.25s ease;
}

.customer-card:hover {
  transform: translateY(-4px);
}

.customer-top {
  display: flex;
  align-items: center;
  gap: 14px;
}

.customer-top h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 950;
  color: #0f172a;
}

.customer-top p {
  margin: 4px 0 0;
  color: #64748b;
  font-weight: 600;
}

.info-list {
  display: grid;
  gap: 12px;
}

.info-list div {
  background: #f8fafc;
  border-radius: 16px;
  padding: 14px;
}

.info-list span {
  display: block;
  color: #64748b;
  font-size: 13px;
  font-weight: 800;
  margin-bottom: 4px;
}

.info-list strong {
  color: #0f172a;
  font-weight: 900;
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

:global(.dark-mode) .summary-card,
:global(.dark-mode) .search-card,
:global(.dark-mode) .customer-card,
:global(.dark-mode) .empty-state {
  background: #0f172a;
}

:global(.dark-mode) .summary-box,
:global(.dark-mode) .info-list div {
  background: #020617;
}

:global(.dark-mode) .summary-card h1,
:global(.dark-mode) .summary-box strong,
:global(.dark-mode) .search-card h2,
:global(.dark-mode) .list-header h2,
:global(.dark-mode) .customer-top h3,
:global(.dark-mode) .info-list strong,
:global(.dark-mode) .empty-state h3 {
  color: #e5e7eb;
}

:global(.dark-mode) input {
  background: #020617;
  color: #e5e7eb;
  border-color: #334155;
}

@media (max-width: 1000px) {
  .customer-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .summary-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .summary-box {
    width: 100%;
  }
}

@media (max-width: 650px) {
  .customer-grid {
    grid-template-columns: 1fr;
  }

  .list-header {
    flex-direction: column;
    align-items: stretch;
  }

  .summary-card h1 {
    font-size: 30px;
  }
}
</style>