<script setup lang="ts">
import { ref } from "vue";
import { useGameStore } from "../stores/game";

const gameStore = useGameStore(); //use the game store to create new tasks
const title = ref("");
const description = ref("");
const difficulty = ref(1);
const intensity = ref(1);
const isSubmitting = ref(false);

const handleSubmit = async () => {
    //handle form submission to create a new task
    if (!title.value) return;
    isSubmitting.value = true;
    await gameStore.createTask(
        title.value,
        description.value,
        difficulty.value,
    );
    title.value = ""; //reset form fields after submission
    description.value = "";
    difficulty.value = 1;
    intensity.value = 1;
    isSubmitting.value = false;
};
</script>
<template>
    <div class="create-task-form">
        <h2>Create New Task</h2>
        <form
            @submit.prevent="handleSubmit"
            class="bg-slate-800 p-4 rounded-lg mb-6"
        >
            <h3 class="text-md font-bold mb-3 text-purple-400">
                📜 Forge New Quest
            </h3>
            <div class="flex flex-col gap-3 md:flex-row">
                <!-- Task Input -->
                <input
                    v-model="title"
                    type="text"
                    placeholder="Enter quest description..."
                    class="flex-1 bg-slate-700 text-white rounded p-2 text-sm border border-slate-600 focus:outline-none focus:border-purple-500"
                    required
                />
                <!-- Difficulty Select -->
                <select
                    v-model="difficulty"
                    class="bg-slate-700 text-white rounded p-2 text-sm border border-slate-600 focus:outline-none focus:border-purple-500"
                >
                    <option :value="1">Easy</option>
                    <option :value="2">Medium</option>
                    <option :value="3">Hard</option>
                    <option :value="4">Very Hard</option>
                    <option :value="5">Extreme</option>
                    <option :value="6">Legendary</option>
                </select>
                <!-- Intensity Select -->
                <select
                    v-model="intensity"
                    class="bg-slate-700 text-white rounded p-2 text-sm border border-slate-600 focus:outline-none focus:border-purple-500 mt-3 md:mt-0"
                >
                    <option :value="1">Low</option>
                    <option :value="2">Medium</option>
                    <option :value="3">High</option>
                    <option :value="4">Very High</option>
                    <option :value="5">Extreme</option>
                    <option :value="6">Legendary</option>
                </select>
                <!-- Submit Button -->
                <button
                    type="submit"
                    :disabled="isSubmitting"
                    class="bg-purple-600 hover:bg-purple-500 disabled:opacity-50 text-white text-sm font-bold px-4 py-2 rounded transition-colors"
                >
                    {{ isSubmitting ? "Forging..." : "Add Quest"
                    }}<!--change button text when submitting-->
                </button>
            </div>
        </form>
    </div>
</template>
