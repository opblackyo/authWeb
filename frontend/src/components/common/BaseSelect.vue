<template>
  <div class="base-select-wrapper">
    <label v-if="label" :for="selectId" class="select-label">
      {{ label }}
      <span v-if="required" class="required-mark">*</span>
    </label>
    
    <div class="select-container" :class="{ 'has-error': error }">
      <select
        :id="selectId"
        :value="modelValue"
        :disabled="disabled"
        :required="required"
        class="base-select"
        @change="handleChange"
      >
        <option value="" disabled>{{ placeholder }}</option>
        <option 
          v-for="option in options" 
          :key="option.value" 
          :value="option.value"
        >
          {{ option.label }}
        </option>
      </select>
      <span class="select-arrow">▼</span>
    </div>
    
    <span v-if="error" class="error-message">{{ error }}</span>
    <span v-else-if="hint" class="hint-message">{{ hint }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '請選擇'
  },
  options: {
    type: Array,
    required: true,
    default: () => []
  },
  error: {
    type: String,
    default: ''
  },
  hint: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const selectId = computed(() => `select-${Math.random().toString(36).substr(2, 9)}`)

const handleChange = (event) => {
  emit('update:modelValue', event.target.value)
  emit('change', event.target.value)
}
</script>

<style scoped>
.base-select-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.select-label {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
}

.required-mark {
  color: #e74c3c;
  margin-left: 4px;
}

.select-container {
  position: relative;
}

.base-select {
  width: 100%;
  padding: 12px 40px 12px 16px;
  font-size: 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-family: inherit;
  background: white;
  cursor: pointer;
  appearance: none;
}

.base-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.base-select:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
  opacity: 0.6;
}

.select-container.has-error .base-select {
  border-color: #e74c3c;
}

.select-container.has-error .base-select:focus {
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

.select-arrow {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  font-size: 12px;
  color: #7f8c8d;
}

.error-message {
  font-size: 14px;
  color: #e74c3c;
}

.hint-message {
  font-size: 14px;
  color: #7f8c8d;
}
</style>

