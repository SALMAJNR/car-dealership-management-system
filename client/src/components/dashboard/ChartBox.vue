<template>
  <div class="chart-card">
    <h3>{{ title }}</h3>

    <div v-if="items?.length" class="chart-list">
      <div v-for="item in items" :key="item.name" class="chart-row">
        <div class="chart-label">
          <span>{{ item.name }}</span>
          <strong>{{ item.count }}</strong>
        </div>

        <div class="bar-track">
          <div
            class="bar-fill"
            :style="{ width: getWidth(item.count) + '%' }"
          ></div>
        </div>
      </div>
    </div>

    <p v-else class="empty">No data available</p>
  </div>
</template>

<script setup>
const props = defineProps({
  title: String,
  items: Array
})

function getWidth(count) {
  const max = Math.max(...props.items.map(i => i.count), 1)
  return (count / max) * 100
}
</script>

<style scoped>
.chart-card {
  background: white;
  border-radius: 22px;
  padding: 22px;
  box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
}

h3 {
  font-size: 18px;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 18px;
}

.chart-row {
  margin-bottom: 16px;
}

.chart-label {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  font-weight: 700;
  color: #334155;
  margin-bottom: 7px;
}

.bar-track {
  height: 9px;
  background: #e2e8f0;
  border-radius: 999px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #2563eb, #60a5fa);
  border-radius: 999px;
}

.empty {
  color: #64748b;
  margin: 0;
}

:global(.dark-mode) .chart-card {
  background: #0f172a;
}

:global(.dark-mode) h3,
:global(.dark-mode) .chart-label {
  color: #e5e7eb;
}
</style>