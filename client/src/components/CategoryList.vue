<script setup>
import { ref, onBeforeMount, computed } from "vue"
import axios from "axios"
import Cookies from "js-cookie"
import { useUserStore } from "@/stores/user"

import NotificationToast from "./dashboard/NotificationToast.vue"

const userStore = useUserStore()

const categories = ref([])
const search = ref("")

const categoryToAdd = ref({
  name: ""
})

const categoryToEdit = ref({})

const notification = ref({
  show: false,
  message: "",
  type: "success"
})

const filteredCategories = computed(() => {
  const keyword = search.value.toLowerCase()

  return categories.value.filter(category =>
    category.name.toLowerCase().includes(keyword)
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

async function fetchCategories() {
  const r = await axios.get("/api/categories/")
  categories.value = r.data
}

async function onCategoryAdd() {
  try {
    if (!categoryToAdd.value.name.trim()) {
      notify("Category name is required", "warning")
      return
    }

    await axios.post("/api/categories/", categoryToAdd.value)

    categoryToAdd.value = {
      name: ""
    }

    await fetchCategories()

    notify("Category added successfully")
  } catch (error) {
    notify("Could not add category", "error")
  }
}

async function onRemoveClick(category) {
  const confirmed = confirm(`Delete ${category.name}?`)

  if (!confirmed) return

  try {
    await axios.delete(`/api/categories/${category.id}/`)
    await fetchCategories()

    notify("Category deleted successfully")
  } catch (error) {
    notify("Could not delete category", "error")
  }
}

function onCategoryEditClick(category) {
  categoryToEdit.value = { ...category }
}

async function onUpdateCategory() {
  try {
    if (!categoryToEdit.value.name.trim()) {
      notify("Category name is required", "warning")
      return
    }

    await axios.put(`/api/categories/${categoryToEdit.value.id}/`, {
      ...categoryToEdit.value
    })

    categoryToEdit.value = {}

    await fetchCategories()

    notify("Category updated successfully")
  } catch (error) {
    notify("Could not update category", "error")
  }
}

onBeforeMount(async () => {
  axios.defaults.withCredentials = true
  axios.defaults.headers.common["X-CSRFToken"] =
    Cookies.get("csrftoken")

  await fetchCategories()
})
</script>

<template>
  <section class="category-page">
    <NotificationToast
      :show="notification.show"
      :message="notification.message"
      :type="notification.type"
    />

    <div class="summary-card">
      <div>
        <span class="eyebrow">Inventory Setup</span>
        <h1>Car Categories</h1>
        <p>
          Create and manage vehicle categories such as Sedan, SUV, Coupe, and more.
        </p>
      </div>

      <div class="summary-box">
        <span>📁</span>
        <div>
          <strong>{{ categories.length }}</strong>
          <p>Total Categories</p>
        </div>
      </div>
    </div>

    <form
      v-if="userStore.user?.role === 'admin'"
      class="form-card"
      @submit.prevent="onCategoryAdd"
    >
      <div>
        <h2>Add New Category</h2>
        <p>Use categories to organize vehicles clearly.</p>
      </div>

      <div class="form-row">
        <input
          v-model="categoryToAdd.name"
          placeholder="Example: SUV"
        />

        <button type="submit">
          Add Category
        </button>
      </div>
    </form>

    <div class="search-card">
      <div>
        <h2>Search Categories</h2>
        <p>Filter categories while typing.</p>
      </div>

      <input
        v-model="search"
        placeholder="Search category name"
      />
    </div>

    <div class="list-header">
      <h2>Category List</h2>
      <p>Showing {{ filteredCategories.length }} of {{ categories.length }}</p>
    </div>

    <div
      v-if="filteredCategories.length"
      class="category-grid"
    >
      <div
        v-for="item in filteredCategories"
        :key="item.id"
        class="category-card"
      >
        <div class="category-icon">
          📁
        </div>

        <div>
          <h3>{{ item.name }}</h3>
          <p>Category ID: {{ item.id }}</p>
        </div>

        <div
          v-if="userStore.user?.role === 'admin'"
          class="actions"
        >
          <button
            class="edit-btn"
            @click="onCategoryEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editCategoryModal"
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
      <div>📁</div>
      <h3>No categories found</h3>
      <p>Try another search or add a new category.</p>
    </div>

    <div
      v-if="userStore.user?.role === 'admin'"
      class="modal fade"
      id="editCategoryModal"
      tabindex="-1"
    >
      <div class="modal-dialog">
        <div class="modal-content rounded-4">
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
            <input
              class="form-control"
              v-model="categoryToEdit.name"
              placeholder="Category name"
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
              @click="onUpdateCategory"
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
.category-page {
  min-height: 100vh;
  padding-bottom: 40px;
}

.summary-card,
.form-card,
.search-card,
.category-card,
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
.category-icon {
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
  min-width: 160px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 16px;
  margin-bottom: 18px;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.category-card {
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  transition: 0.25s ease;
}

.category-card:hover {
  transform: translateY(-4px);
}

.category-card h3 {
  margin: 0;
  font-size: 22px;
  font-weight: 950;
  color: #0f172a;
}

.category-card p {
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

:global(.dark-mode) .summary-card,
:global(.dark-mode) .form-card,
:global(.dark-mode) .search-card,
:global(.dark-mode) .category-card,
:global(.dark-mode) .empty-state {
  background: #0f172a;
}

:global(.dark-mode) .summary-box {
  background: #020617;
}

:global(.dark-mode) .summary-card h1,
:global(.dark-mode) .summary-box strong,
:global(.dark-mode) .form-card h2,
:global(.dark-mode) .search-card h2,
:global(.dark-mode) .list-header h2,
:global(.dark-mode) .category-card h3,
:global(.dark-mode) .empty-state h3 {
  color: #e5e7eb;
}

:global(.dark-mode) input {
  background: #020617;
  color: #e5e7eb;
  border-color: #334155;
}

@media (max-width: 1000px) {
  .category-grid {
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
  .category-grid {
    grid-template-columns: 1fr;
  }

  .form-row,
  .list-header {
    flex-direction: column;
    align-items: stretch;
  }

  .summary-card h1 {
    font-size: 30px;
  }
}
</style>