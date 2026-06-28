<template>
  <div class="stats-grid">
    <div class="stat-card">
      <div class="icon">🚗</div>
      <div>
        <h3>{{ totalCars }}</h3>
        <p>Total Cars</p>
      </div>
    </div>

    <div class="stat-card">
      <div class="icon">🏷️</div>
      <div>
        <h3>{{ brands }}</h3>
        <p>Brands</p>
      </div>
    </div>

    <div class="stat-card">
      <div class="icon">📂</div>
      <div>
        <h3>{{ categories }}</h3>
        <p>Categories</p>
      </div>
    </div>

    <div class="stat-card">
      <div class="icon">🏢</div>
      <div>
        <h3>{{ dealers }}</h3>
        <p>Dealers</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  totalCars: {
    type: Number,
    default: 0
  },
  brands: {
    type: Number,
    default: 0
  },
  categories: {
    type: Number,
    default: 0
  },
  dealers: {
    type: Number,
    default: 0
  }
})
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  padding: 22px;
  border-radius: 22px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
}

.icon {
  width: 54px;
  height: 54px;
  border-radius: 16px;
  background: #eff6ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
}

h3 {
  margin: 0;
  font-size: 28px;
  font-weight: 900;
  color: #0f172a;
}

p {
  margin: 4px 0 0;
  color: #64748b;
  font-weight: 600;
}

:global(.dark-mode) .stat-card {
  background: #0f172a;
}

:global(.dark-mode) h3 {
  color: #e5e7eb;
}

@media (max-width: 1000px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 650px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>