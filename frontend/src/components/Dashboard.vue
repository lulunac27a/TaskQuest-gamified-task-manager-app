<script setup lang="ts">
import { onMounted } from "vue";
import { useGameStore } from "../stores/game";
const gameStore = useGameStore();
onMounted(() => {
    gameStore.fetchProfile();
});
</script>

<template>
    <div
        class="p-6 max-w-xl mx-auto bg-slate-900 text-white rounded-xl shadow-md"
    >
        <!-- Character Stats Panel -->
        <div class="mb-6 border-b border-slate-700 pb-4">
            <h2 class="text-2xl font-bold mb-2">🛡️ Hero Dashboard</h2>
            <div class="flex justify-between text-sm mb-1">
                <span>Level {{ gameStore.user.level }}</span>
            </div>
            <!-- XP Progress Bar -->
            <div class="w-full bg-slate-700 h-4 rounded-full overflow-hidden">
                <div
                    class="bg-purple-500 h-full transition-all duration-500"
                    :style="{ width: `${gameStore.xpProgress}%` }"
                ></div>
            </div>
            <p class="text-xs text-slate-400 mt-1 text-right">
                {{ gameStore.user.xp }} / {{ gameStore.user.level * 100 }} XP
            </p>
        </div>
        <!-- Active Quests -->
        <div>
            <h3 class="text-xl font-semibold mb-3">📜 Active Quests</h3>
            <ul class="space-y-2">
                <li
                    v-for="task in gameStore.tasks"
                    :key="task.id"
                    class="flex justify-between items-center bg-slate-800 p-3 rounded"
                >
                    <!--repeat for each task in task list-->
                    <div>
                        <span
                            :class="{
                                'line-through text-slate-500':
                                    task.is_completed,
                            }"
                        >
                            {{ task.title }}
                        </span>
                        <span
                            class="ml-2 text-xs px-2 py-0.5 rounded bg-amber-600"
                        >
                            {{ task.difficulty }}
                        </span>
                    </div>
                    <div class="flex gap-2">
                        <button
                            v-if="!task.is_completed"
                            @click="gameStore.completeTask(task.id)"
                            class="bg-emerald-600 hover:bg-emerald-500 text-xs px-3 py-1.5 rounded font-bold"
                        >
                            <!--display complete button if task is not completed-->
                            Complete
                        </button>
                        <button
                            @click="gameStore.deleteTask(task.id)"
                            class="bg-red-600 hover:bg-red-500 text-xs px-3 py-1.5 rounded font-bold"
                        >
                            Delete
                        </button>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>
