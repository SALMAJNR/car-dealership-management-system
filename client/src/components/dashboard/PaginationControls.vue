<template>
  <div class="pagination-card">
    <button :disabled="currentPage <= 1" @click="$emit('previous')">
      Previous
    </button>

    <span>
      Page {{ currentPage }} of {{ totalPages }}
    </span>

    <button :disabled="currentPage >= totalPages" @click="$emit('next')">
      Next
    </button>
  </div>
</template>

<script setup>
defineProps({
  currentPage: Number,
  totalPages: Number
})

defineEmits(["previous", "next"])
</script>

<style scoped>
.pagination-card {
  margin-top: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 18px;
}

button {
  border: none;
  background: #2563eb;
  color: white;
  padding: 11px 18px;
  border-radius: 12px;
  font-weight: 800;
}

button:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

span {
  font-weight: 800;
  color: #475569;
}

:global(.dark-mode) span {
  color: #e5e7eb;
}
</style>