<template>
  <main>
    <div
      class="dropzone-scope"
      :class="{ 'dropzone-active': isDragging }"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="onDrop"
      @click="fileInput.click()"
    >
      <input
        ref="fileInput"
        type="file"
        accept=".pdf, .doc, .docx"
        class="hidden-input"
        @change="onFileSelect"
      />
      <p v-if="!selectedFile">Arraste e solte o arquivo aqui ou clique para selecionar</p>
      <p v-else>{{ selectedFile.name }}</p>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';

const isDragging = ref(false);
const selectedFile = ref(null);
const fileInput = ref(null);

const emit = defineEmits(['file-selected']);

function onDrop(event) {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  if (file && file.type === 'application/pdf') {
    selectedFile.value = file;
    emit('file-selected', file);
  }
}

function onFileSelect(event) {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
    emit('file-selected', file);
  }
}
</script>

<style scoped>
.dropzone-scope {
  height: 300px;
  width: 100%;
  border: 2px dashed #6366f1;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #202125;
  color: #fff;
  cursor: pointer;
  transition: border-color 0.2s, background-color 0.2s;
}

.dropzone-active {
  border-color: #a5a8ff;
  background-color: #2a2b30;
}

.hidden-input {
  display: none;
}
</style>