<template>
  <form
    v-if="role === 'admin'"
    class="add-card"
    @submit.prevent="$emit('add')"
  >
    <div class="form-header">
      <div>
        <h2>Add New Car</h2>
        <p>Upload a car and connect it to a brand, category, and dealer.</p>
      </div>
    </div>

    <div class="add-grid">
      <input
        :value="car.model"
        @input="$emit('update:model', $event.target.value)"
        placeholder="Car model"
        required
      />

      <input
        :value="car.year"
        @input="$emit('update:year', Number($event.target.value))"
        type="number"
        placeholder="Year"
        required
      />

      <select
        :value="car.brand"
        @change="$emit('update:brand', Number($event.target.value))"
        required
      >
        <option :value="null">Select Brand</option>
        <option v-for="b in brands" :key="b.id" :value="b.id">
          {{ b.name }}
        </option>
      </select>

      <select
        :value="car.category"
        @change="$emit('update:category', Number($event.target.value))"
        required
      >
        <option :value="null">Select Category</option>
        <option v-for="c in categories" :key="c.id" :value="c.id">
          {{ c.name }}
        </option>
      </select>

      <select
        :value="car.dealer"
        @change="$emit('update:dealer', Number($event.target.value))"
        required
      >
        <option :value="null">Select Dealer</option>
        <option v-for="d in dealers" :key="d.id" :value="d.id">
          {{ d.name }}
        </option>
      </select>

      <input
        type="file"
        @change="$emit('image-change', $event)"
      />

      <button type="submit">
        Add Car
      </button>
    </div>

    <img
      v-if="imagePreview"
      :src="imagePreview"
      class="preview"
    />
  </form>
</template>

<script setup>
defineProps({
  role: String,
  car: Object,
  brands: Array,
  categories: Array,
  dealers: Array,
  imagePreview: String
})

defineEmits([
  "add",
  "image-change",
  "update:model",
  "update:year",
  "update:brand",
  "update:category",
  "update:dealer"
])
</script>

<style scoped>
.add-card {
  background: white;
  padding: 24px;
  border-radius: 22px;
  margin-bottom: 24px;
  box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
}

.form-header {
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

.add-grid {
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

button {
  border: none;
  background: #2563eb;
  color: white;
  padding: 13px 16px;
  border-radius: 14px;
  font-weight: 900;
}

.preview {
  margin-top: 18px;
  max-height: 120px;
  border-radius: 16px;
}

:global(.dark-mode) .add-card {
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
  .add-grid {
    grid-template-columns: 1fr;
  }
}
</style>