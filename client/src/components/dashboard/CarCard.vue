<template>
  <div class="car-card">
    <div class="image-wrap">
      <img v-if="car.picture" :src="car.picture" />

      <img
        v-else-if="car.images?.length"
        :src="car.images[0].image"
      />

      <div v-else class="placeholder">
        🚗
      </div>
    </div>

    <div class="content">
      <div class="title-row">
        <h3>{{ car.model }}</h3>
        <span>{{ car.year || "N/A" }}</span>
      </div>

      <div class="info-grid">
        <p><strong>Brand</strong>{{ brand || "N/A" }}</p>
        <p><strong>Category</strong>{{ category || "N/A" }}</p>
        <p><strong>Dealer</strong>{{ dealer || "N/A" }}</p>
      </div>

      <div class="actions">
        <button
          v-if="role === 'customer'"
          class="purchase-btn"
          @click="$emit('purchase', car)"
        >
          Purchase
        </button>

        <template v-if="role === 'admin'">
          <button
            class="edit-btn"
            data-bs-toggle="modal"
            data-bs-target="#editCarModal"
            @click="$emit('edit', car)"
          >
            Edit
          </button>

          <button
            class="delete-btn"
            @click="$emit('delete', car)"
          >
            Delete
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  car: Object,
  brand: String,
  category: String,
  dealer: String,
  role: String
})

defineEmits(["edit", "delete", "purchase"])
</script>

<style scoped>
.car-card {
  background: white;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.1);
  transition: 0.25s ease;
}

.car-card:hover {
  transform: translateY(-5px);
}

.image-wrap {
  height: 210px;
  background: linear-gradient(135deg, #e2e8f0, #f8fafc);
}

.image-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 58px;
}

.content {
  padding: 22px;
}

.title-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-bottom: 18px;
}

h3 {
  margin: 0;
  font-size: 22px;
  font-weight: 900;
  color: #0f172a;
}

.title-row span {
  background: #eff6ff;
  color: #2563eb;
  padding: 7px 11px;
  border-radius: 999px;
  font-weight: 900;
  font-size: 13px;
}

.info-grid {
  display: grid;
  gap: 10px;
}

p {
  margin: 0;
  color: #475569;
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

strong {
  color: #0f172a;
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 22px;
}

button {
  border: none;
  padding: 11px 16px;
  border-radius: 12px;
  font-weight: 900;
  flex: 1;
}

.purchase-btn,
.edit-btn {
  background: #2563eb;
  color: white;
}

.delete-btn {
  background: #ef4444;
  color: white;
}

:global(.dark-mode) .car-card {
  background: #0f172a;
}

:global(.dark-mode) h3,
:global(.dark-mode) strong {
  color: #e5e7eb;
}

:global(.dark-mode) p {
  color: #cbd5e1;
}
</style>