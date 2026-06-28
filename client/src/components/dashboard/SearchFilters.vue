<template>
  <div class="filter-card">
    <div class="filter-header">
      <div>
        <h2>Search & Filter</h2>
        <p>Find cars by model, brand, category, or dealer.</p>
      </div>

      <button class="clear-btn" @click="$emit('clear')">
        Clear
      </button>
    </div>

    <div class="filter-grid">
      <input
        :value="modelFilter"
        @input="$emit('update:modelFilter', $event.target.value)"
        placeholder="Search model"
      />

      <input
        :value="brandFilter"
        @input="$emit('update:brandFilter', $event.target.value)"
        placeholder="Search brand"
      />

      <input
        :value="categoryFilter"
        @input="$emit('update:categoryFilter', $event.target.value)"
        placeholder="Search category"
      />

      <select
        :value="dealerFilter"
        @change="$emit('update:dealerFilter', Number($event.target.value))"
      >
        <option :value="0">All Dealers</option>
        <option
          v-for="dealer in dealers"
          :key="dealer.id"
          :value="dealer.id"
        >
          {{ dealer.name }}
        </option>
      </select>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelFilter: String,
  brandFilter: String,
  categoryFilter: String,
  dealerFilter: Number,
  dealers: Array
})

defineEmits([
  "update:modelFilter",
  "update:brandFilter",
  "update:categoryFilter",
  "update:dealerFilter",
  "clear"
])
</script>

<style scoped>
.filter-card {
  background: white;
  padding: 24px;
  border-radius: 22px;
  margin-bottom: 24px;
  box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
}

.filter-header {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: center;
  margin-bottom: 18px;
}

h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 900;
  color: #0f172a;
}

p {
  margin: 4px 0 0;
  color: #64748b;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

input,
select {
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  padding: 13px 14px;
  border-radius: 14px;
  outline: none;
  font-weight: 600;
}

input:focus,
select:focus {
  border-color: #2563eb;
  background: white;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
}

.clear-btn {
  border: none;
  background: #e2e8f0;
  color: #0f172a;
  padding: 11px 16px;
  border-radius: 12px;
  font-weight: 800;
}

:global(.dark-mode) .filter-card {
  background: #0f172a;
}

:global(.dark-mode) h2 {
  color: #e5e7eb;
}

:global(.dark-mode) input,
:global(.dark-mode) select {
  background: #020617;
  border-color: #334155;
  color: #e5e7eb;
}

@media (max-width: 900px) {
  .filter-grid {
    grid-template-columns: 1fr;
  }

  .filter-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>