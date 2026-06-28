<template>
  <div class="charts-grid">
    <ChartBox title="Cars by Brand" :items="brandData" />
    <ChartBox title="Cars by Category" :items="categoryData" />
    <ChartBox title="Cars by Dealer" :items="dealerData" />
  </div>
</template>

<script setup>
import ChartBox from "./ChartBox.vue"

defineProps({
  brandData: Array,
  categoryData: Array,
  dealerData: Array
})
</script>

<style scoped>
.charts-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin-bottom: 24px;
}

@media (max-width: 1000px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>