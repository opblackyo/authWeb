<template>
  <div class="base-input-wrapper">
    <label v-if="label" :for="inputId" class="input-label">
      {{ label }}
      <span v-if="required" class="required-mark">*</span>
    </label>
    
    <div class="input-container" :class="{ 'has-error': error, 'has-icon': icon }">
      <span v-if="icon" class="input-icon">{{ icon }}</span>
      
      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :class="['base-input', { 'has-icon': icon }]"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      />
      
      <span v-if="type === 'password' && showPasswordToggle" class="password-toggle" @click="togglePassword">
        {{ showPassword ? '👁️' : '👁️‍🗨️' }}
      </span>
    </div>
    
    <span v-if="error" class="error-message">{{ error }}</span>
    <span v-else-if="hint" class="hint-message">{{ hint }}</span>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: ''
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
  },
  showPasswordToggle: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'blur', 'focus'])

const showPassword = ref(false)
const inputId = computed(() => `input-${Math.random().toString(36).substr(2, 9)}`)

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}

const handleBlur = (event) => {
  emit('blur', event)
}

const handleFocus = (event) => {
  emit('focus', event)
}

const togglePassword = () => {
  showPassword.value = !showPassword.value
  const input = document.getElementById(inputId.value)
  input.type = showPassword.value ? 'text' : 'password'
}
</script>

<style scoped>
.base-input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.input-label {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
}

.required-mark {
  color: #e74c3c;
  margin-left: 4px;
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 16px;
  font-size: 18px;
  pointer-events: none;
  z-index: 1;
}

.base-input {
  width: 100%;
  padding: 12px 16px;
  font-size: 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-family: inherit;
  background: white;
}

.base-input.has-icon {
  padding-left: 48px;
}

.base-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.base-input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
  opacity: 0.6;
}

.input-container.has-error .base-input {
  border-color: #e74c3c;
}

.input-container.has-error .base-input:focus {
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

.password-toggle {
  position: absolute;
  right: 16px;
  cursor: pointer;
  font-size: 18px;
  user-select: none;
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

