<template>
  <button 
    :class="['base-button', `base-button--${variant}`, `base-button--${size}`, { 'base-button--loading': loading, 'base-button--disabled': disabled }]"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <span v-if="loading" class="button-spinner"></span>
    <span v-if="icon && !loading" class="button-icon">{{ icon }}</span>
    <span class="button-text"><slot /></span>
  </button>
</template>

<script setup>
const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'success', 'danger', 'warning', 'outline', 'ghost'].includes(value)
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  icon: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
.base-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
  position: relative;
  overflow: hidden;
}

.base-button:hover:not(.base-button--disabled):not(.base-button--loading) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.base-button:active:not(.base-button--disabled):not(.base-button--loading) {
  transform: translateY(0);
}

/* Sizes */
.base-button--small {
  padding: 8px 16px;
  font-size: 14px;
}

.base-button--medium {
  padding: 12px 24px;
  font-size: 16px;
}

.base-button--large {
  padding: 16px 32px;
  font-size: 18px;
}

/* Variants */
.base-button--primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.base-button--primary:hover:not(.base-button--disabled) {
  background: linear-gradient(135deg, #5568d3 0%, #6a4190 100%);
}

.base-button--secondary {
  background: #6c757d;
  color: white;
}

.base-button--secondary:hover:not(.base-button--disabled) {
  background: #5a6268;
}

.base-button--success {
  background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
  color: white;
}

.base-button--success:hover:not(.base-button--disabled) {
  background: linear-gradient(135deg, #4a9428 0%, #95ca56 100%);
}

.base-button--danger {
  background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
  color: white;
}

.base-button--danger:hover:not(.base-button--disabled) {
  background: linear-gradient(135deg, #d42d3f 0%, #dc5139 100%);
}

.base-button--warning {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.base-button--warning:hover:not(.base-button--disabled) {
  background: linear-gradient(135deg, #e07fe8 0%, #e24a5f 100%);
}

.base-button--outline {
  background: transparent;
  border: 2px solid #667eea;
  color: #667eea;
}

.base-button--outline:hover:not(.base-button--disabled) {
  background: #667eea;
  color: white;
}

.base-button--ghost {
  background: transparent;
  color: #667eea;
}

.base-button--ghost:hover:not(.base-button--disabled) {
  background: rgba(102, 126, 234, 0.1);
}

/* States */
.base-button--disabled,
.base-button--loading {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.button-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>

