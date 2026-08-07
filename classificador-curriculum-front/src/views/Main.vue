<script setup>
import Dropzone from '../components/drop-zone.vue';
</script>

<template>
  <div class="main">
    <h1>Classificador de Currículos</h1>
    <p>Bem-vindo ao Classificador de Currículos! Esta aplicação permite que você classifique currículos de forma eficiente e organizada.</p>
    <p>Para começar, clique no botão abaixo para carregar os currículos e iniciar o processo de classificação.</p>
    <Dropzone />
    <router-link to="/loading">Carregar Currículo</router-link>
  </div>
</template>