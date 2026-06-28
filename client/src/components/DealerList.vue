<script setup>
import { ref, onBeforeMount, computed } from "vue"
import axios from "axios"
import Cookies from "js-cookie"
import { useUserStore } from "@/stores/user"

import NotificationToast from "./dashboard/NotificationToast.vue"

const userStore = useUserStore()

const dealers = ref([])
const search = ref("")

const dealerToAdd = ref({
  name: "",
  city: ""
})

const dealerToEdit = ref({})

const notification = ref({
  show: false,
  message: "",
  type: "success"
})

const filteredDealers = computed(() => {
  const keyword = search.value.toLowerCase()

  return dealers.value.filter(dealer =>
    dealer.name.toLowerCase().includes(keyword) ||
    dealer.city.toLowerCase().includes(keyword)
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

async function fetchDealers() {
  const r = await axios.get("/api/dealers/")
  dealers.value = r.data
}

async function onDealerAdd() {
  try {
    if (!dealerToAdd.value.name.trim() || !dealerToAdd.value.city.trim()) {
      notify("Dealer name and city are required", "warning")
      return
    }

    await axios.post("/api/dealers/", dealerToAdd.value)

    dealerToAdd.value = {
      name: "",
      city: ""
    }

    await fetchDealers()

    notify("Dealer added successfully")
  } catch (error) {
    notify("Could not add dealer", "error")
  }
}

async function onRemoveClick(dealer) {
  const confirmed = confirm(`Delete ${dealer.name}?`)

  if (!confirmed) return

  try {
    await axios.delete(`/api/dealers/${dealer.id}/`)
    await fetchDealers()

    notify("Dealer deleted successfully")
  } catch (error) {
    notify("Could not delete dealer", "error")
  }
}

function onDealerEditClick(dealer) {
  dealerToEdit.value = { ...dealer }
}

async function onUpdateDealer() {
  try {
    if (!dealerToEdit.value.name.trim() || !dealerToEdit.value.city.trim()) {
      notify("Dealer name and city are required", "warning")
      return
    }

    await axios.put(`/api/dealers/${dealerToEdit.value.id}/`, {
      ...dealerToEdit.value
    })

    dealerToEdit.value = {}

    await fetchDealers()

    notify("Dealer updated successfully")
  } catch (error) {
    notify("Could not update dealer", "error")
  }
}

onBeforeMount(async () => {
  axios.defaults.withCredentials = true
  axios.defaults.headers.common["X-CSRFToken"] =
    Cookies.get("csrftoken")

  await fetchDealers()
})
</script>

<template>
  <section class="dealer-page">
    <NotificationToast
      :show="notification.show"
      :message="notification.message"
      :type="notification.type"
    />

    <div class="summary-card">
      <div>
        <span class="eyebrow">Dealer Network</span>
        <h1>Dealership Partners</h1>
        <p>
          Manage dealership partners, branch locations, and cities connected to your inventory.
        </p>
      </div>

      <div class="summary-box">
        <span>🏬</span>
        <div>
          <strong>{{ dealers.length }}</strong>
          <p>Total Dealers</p>
        </div>
      </div>
    </div>

    <form
      v-if="userStore.user?.role === 'admin'"
      class="form-card"
      @submit.prevent="onDealerAdd"
    >
      <div>
        <h2>Add New Dealer</h2>
        <p>Create a dealer branch and connect it to cars in your inventory.</p>
      </div>

      <div class="form-row">
        <input
          v-model="dealerToAdd.name"
          placeholder="Dealer name"
        />

        <input
          v-model="dealerToAdd.city"
          placeholder="City"
        />

        <button type="submit">
          Add Dealer
        </button>
      </div>
    </form>

    <div class="search-card">
      <div>
        <h2>Search Dealers</h2>
        <p>Search by dealer name or city.</p>
      </div>

      <input
        v-model="search"
        placeholder="Search dealer or city"
      />
    </div>

    <div class="list-header">
      <h2>Dealer List</h2>
      <p>Showing {{ filteredDealers.length }} of {{ dealers.length }}</p>
    </div>

    <div
      v-if="filteredDealers.length"
      class="dealer-grid"
    >
      <div
        v-for="item in filteredDealers"
        :key="item.id"
        class="dealer-card"
      >
        <div class="dealer-top">
          <div class="dealer-icon">
            🏬
          </div>

          <div>
            <h3>{{ item.name }}</h3>
            <p>Dealer ID: {{ item.id }}</p>
          </div>
        </div>

        <div class="info-list">
          <div>
            <span>City</span>
            <strong>{{ item.city || "N/A" }}</strong>
          </div>

          <div>
            <span>Status</span>
            <strong>Active Partner</strong>
          </div>
        </div>

        <div
          v-if="userStore.user?.role === 'admin'"
          class="actions"
        >
          <button
            class="edit-btn"
            @click="onDealerEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editDealerModal"
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
      <div>🏬</div>
      <h3>No dealers found</h3>
      <p>Try another search or add a new dealer.</p>
    </div>

    <div
      v-if="userStore.user?.role === 'admin'"
      class="modal fade"
      id="editDealerModal"
      tabindex="-1"
    >
      <div class="modal-dialog">
        <div class="modal-content rounded-4">
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
            <input
              class="form-control mb-3"
              v-model="dealerToEdit.name"
              placeholder="Dealer name"
            />

            <input
              class="form-control"
              v-model="dealerToEdit.city"
              placeholder="City"
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
              @click="onUpdateDealer"
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
.dealer-page {
  min-height: 100vh;
  padding-bottom: 40px;
}

.summary-card,
.form-card,
.search-card,
.dealer-card,
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
.dealer-icon {
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
  display: grid;
  grid-template-columns: 1fr 1fr auto;
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
  min-width: 145px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 16px;
  margin-bottom: 18px;
}

.dealer-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.dealer-card {
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  transition: 0.25s ease;
}

.dealer-card:hover {
  transform: translateY(-4px);
}

.dealer-top {
  display: flex;
  align-items: center;
  gap: 14px;
}

.dealer-top h3 {
  margin: 0;
  font-size: 21px;
  font-weight: 950;
  color: #0f172a;
}

.dealer-top p {
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
:global(.dark-mode) .form-card,
:global(.dark-mode) .search-card,
:global(.dark-mode) .dealer-card,
:global(.dark-mode) .empty-state {
  background: #0f172a;
}

:global(.dark-mode) .summary-box,
:global(.dark-mode) .info-list div {
  background: #020617;
}

:global(.dark-mode) .summary-card h1,
:global(.dark-mode) .summary-box strong,
:global(.dark-mode) .form-card h2,
:global(.dark-mode) .search-card h2,
:global(.dark-mode) .list-header h2,
:global(.dark-mode) .dealer-top h3,
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
  .dealer-grid {
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
  .dealer-grid {
    grid-template-columns: 1fr;
  }

  .form-row,
  .list-header {
    grid-template-columns: 1fr;
    flex-direction: column;
    align-items: stretch;
  }

  .summary-card h1 {
    font-size: 30px;
  }
}
</style>