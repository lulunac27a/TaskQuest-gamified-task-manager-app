<script setup lang="ts">
import { onMounted } from 'vue';
import { useGameStore } from '../stores/game';
const gameStore = useGameStore();
onMounted(() => {
  gameStore.fetchProfile();
});
</script>

<template>
    <div class="dashboard">
        <h1>Dashboard</h1>
        <p>Welcome, {{ gameStore.profile?.username }}</p>
        <p>Level: {{ gameStore.profile?.level }}</p>
        <p>Experience: {{ gameStore.profile?.experience }}</p>
    </div>
    <div class="progress">
        <div :style="{ width: gameStore.xpProgress + '%' }" class="progress-bar"></div>
    </div>
    <div>
        <h2>Quests</h2>
        <ul>
            <li v-for="task in gameStore.tasks" :key="task.id">
                {{ task.title }} - {{ task.difficulty }} - {{ task.intensity }} - {{ task.completed ? 'Completed' : 'Incomplete' }}
                <button v-if="!task.completed" @click="gameStore.completeTask(task.id)">Complete</button>
            </li>
        </ul>
    </div>
</template>