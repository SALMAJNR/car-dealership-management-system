<template>
  <div class="modal fade" id="editCarModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content rounded-4">
        <div class="modal-header">
          <h5 class="modal-title">Edit Car</h5>
          <button class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">
          <input
            class="form-control mb-3"
            :value="car.model"
            @input="$emit('update:model', $event.target.value)"
            placeholder="Model"
          />

          <input
            class="form-control"
            type="number"
            :value="car.year"
            @input="$emit('update:year', Number($event.target.value))"
            placeholder="Year"
          />
        </div>

        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">
            Close
          </button>

          <button class="btn btn-primary" data-bs-dismiss="modal" @click="$emit('save')">
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  car: Object
})

defineEmits(["save", "update:model", "update:year"])
</script>