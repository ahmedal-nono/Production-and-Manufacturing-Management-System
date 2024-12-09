<template>
    <div v-if="visible" class="popup-overlay" @click="handleOverlayClick">
      <div class="popup-content" @click.stop>
        <button @click="$emit('update:visible', false)" class="close-button">
          ✕
        </button>
        <slot></slot>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { defineProps, defineEmits } from 'vue';
  
  defineProps({
    visible: {
      type: Boolean,
      required: true,
    },
  });
  
  const emit = defineEmits();
  
  function handleOverlayClick() {
    emit('update:visible', false);
  }
  </script>
  
  <style scoped>
  .popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5); 
    z-index: 1000; 
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .popup-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    width: 90%; 
    max-width: 900px; 
    max-height: 150%; 
    overflow-y: auto; 
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
    position: relative;
    scale: 70%;
  }
  
  .close-button {
    position: sticky;
    top: 10px;
    left: 100%;
    background: transparent;
    border: none;
    font-size: 18px;
    cursor: pointer;
    color: #333;
  }
  </style>
  