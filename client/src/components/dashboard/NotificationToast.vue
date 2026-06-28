<template>
  <transition name="toast">
    <div
      v-if="show"
      :class="['toast-box', type]"
    >
      <span>{{ icon }}</span>
      <p>{{ message }}</p>
    </div>
  </transition>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  show: Boolean,
  message: String,
  type: {
    type: String,
    default: "success"
  }
})

const icon = computed(() => {
  if (props.type === "error") return "❌"
  if (props.type === "warning") return "⚠️"
  return "✅"
})
</script>

<style scoped>
.toast-box {
  position: fixed;
  top: 90px;
  right: 25px;
  z-index: 9999;
  min-width: 280px;
  padding: 16px 18px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: white;
  font-weight: 700;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
}

.toast-box p {
  margin: 0;
}

.success {
  background: #16a34a;
}

.error {
  background: #dc2626;
}

.warning {
  background: #f59e0b;
}

.toast-enter-active,
.toast-leave-active {
  transition: 0.25s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
</style>