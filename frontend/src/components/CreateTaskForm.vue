<script setup lang="ts">
import { ref } from "vue";
import { useGameStore } from "../stores/game";

const gameStore = useGameStore();
const title = ref("");
const description = ref("");
const difficulty = ref(1);
const intensity = ref(1);
const isSubmitting = ref(false);

const handleSubmit = async () => {
  if (!title.value) return;
  isSubmitting.value = true;
  await gameStore.createTask(title.value, description.value, difficulty.value);
  title.value = "";
  description.value = "";
  difficulty.value = 1;
  intensity.value = 1;
  isSubmitting.value = false;
};
</script>
<template>
  <div class="create-task-form">
    <h2>Create New Task</h2>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="title">Title:</label>
        <input id="title" v-model="title" required />
      </div>
      <div>
        <label for="description">Description:</label>
        <textarea id="description" v-model="description"></textarea>
      </div>
      <div>
        <label for="difficulty">Difficulty:</label>
        <select id="difficulty" v-model.number="difficulty">
          <option :value="1">Easy</option>
          <option :value="2">Medium</option>
          <option :value="3">Hard</option>
          <option :value="4">Very Hard</option>
          <option :value="5">Extreme</option>
          <option :value="6">Legendary</option>
        </select>
      </div>
      <div>
        <label for="intensity">Intensity:</label>
        <select id="intensity" v-model.number="intensity">
          <option :value="1">Low</option>
          <option :value="2">Medium</option>
          <option :value="3">High</option>
          <option :value="4">Very High</option>
          <option :value="5">Extreme</option>
          <option :value="6">Legendary</option>
        </select>
      </div>
      <button type="submit" :disabled="isSubmitting">Create Task</button>
    </form>
  </div>
</template>
