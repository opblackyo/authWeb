<template>
  <div 
    :class="['base-card', `base-card--${variant}`, { 'base-card--hoverable': hoverable, 'base-card--clickable': clickable }]"
    @click="handleClick"
  >
    <div v-if="$slots.header || title" class="card-header">
      <slot name="header">
        <h3 class="card-title">{{ title }}</h3>
      </slot>
    </div>
    
    <div class="card-body" :class="{ 'no-padding': noPadding }">
      <slot />
    </div>
    
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'bordered', 'elevated', 'flat'].includes(value)
  },
  hoverable: {
    type: Boolean,
    default: false
  },
  clickable: {
    type: Boolean,
    default: false
  },
  noPadding: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const handleClick = (event) => {
  if (props.clickable) {
    emit('click', event)
  }
}
</script>

<style scoped>
.base-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.base-card--default {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.base-card--bordered {
  border: 2px solid #e0e0e0;
}

.base-card--elevated {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.base-card--flat {
  box-shadow: none;
  background: #f8f9fa;
}

.base-card--hoverable:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.base-card--clickable {
  cursor: pointer;
}

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e0e0e0;
  background: #f8f9fa;
}

.card-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
}

.card-body {
  padding: 24px;
}

.card-body.no-padding {
  padding: 0;
}

.card-footer {
  padding: 16px 24px;
  border-top: 1px solid #e0e0e0;
  background: #f8f9fa;
}
</style>

