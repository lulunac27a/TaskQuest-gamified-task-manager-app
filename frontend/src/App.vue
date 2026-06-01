<script setup lang="ts">
import Dashboard from "./components/Dashboard.vue";
import CreateTaskForm from "./components/CreateTaskForm.vue";
</script>

<template>
    <main class="min-h-screen bg-slate-950 py-8 px-4">
        <div class="max-w-xl mx-auto space-y-6">
            <!-- App Header -->
            <header class="text-center mb-8">
                <h1
                    class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-amber-400"
                >
                    ⚔️ TASKQUEST
                </h1>
                <p class="text-slate-400 text-sm mt-1">
                    Turn your daily grind into an epic adventure
                </p>
            </header>

            <!-- App Core UI Components -->
            <CreateTaskForm />
            <Dashboard />
        </div>
    </main>
</template>
