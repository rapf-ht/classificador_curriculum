<script setup>
import { ref } from 'vue';
import Dropzone from '../components/drop-zone.vue';
import { analisarCurriculo } from '../services/api';

const selectedFile = ref(null);
const vagaTexto = ref('');
const status = ref('idle'); // idle | loading | done | error
const resultado = ref(null);
const erro = ref('');

function onFileSelected(file) {
  selectedFile.value = file;
}

async function enviarAnalise() {
  if (!selectedFile.value || !vagaTexto.value.trim()) return;

  status.value = 'loading';
  erro.value = '';

  try {
    resultado.value = await analisarCurriculo(selectedFile.value, vagaTexto.value);
    status.value = 'done';
  } catch (e) {
    erro.value = e.message;
    status.value = 'error';
  }
}
</script>

<template>
  <div class="main" v-if="status === 'idle' || status === 'error'">
    <h1>Classificador de Currículos</h1>
    <p>Envie seu currículo em PDF e a descrição da vaga para receber uma análise de aderência.</p>

    <Dropzone @file-selected="onFileSelected" />

    <textarea
      v-model="vagaTexto"
      placeholder="Cole aqui a descrição da vaga..."
      rows="6"
    />

    <p v-if="erro" class="erro">{{ erro }}</p>

    <button :disabled="!selectedFile || !vagaTexto.trim()" @click="enviarAnalise">
      Analisar Currículo
    </button>
  </div>

  <div class="loading" v-else-if="status === 'loading'">
    <h1>Analisando...</h1>
    <p>Isso pode levar alguns segundos.</p>
    <div class="loading-spinner">
      <img src="../assets/loading-animation.gif" alt="Carregando" />
    </div>
  </div>

  <div class="resultado" v-else-if="status === 'done'">
    <h1>Score: {{ resultado.score }}/100</h1>
    <p>{{ resultado.job_apply ? '✅ Apto para a vaga' : '⚠️ Ainda não totalmente apto' }}</p>

    <h2>Pontos fortes</h2>
    <ul><li v-for="p in resultado.strong_points" :key="p">{{ p }}</li></ul>

    <h2>Pontos a melhorar</h2>
    <ul><li v-for="p in resultado.weak_points" :key="p">{{ p }}</li></ul>

    <h2>Recomendação</h2>
    <p>{{ resultado.help_if_needed }}</p>

    <button @click="status = 'idle'">Analisar outro currículo</button>
  </div>

  <div class="error" v-else-if="status === 'error'">
    <h1>Ocorreu um erro durante a análise</h1>
    <p>Refaça o processo e tente novamente</p>
    
    <div class="error-image">
      <img src="hamster-coffee.gif" alt="Erro Hamster" />
    </div>

  </div>
</template>