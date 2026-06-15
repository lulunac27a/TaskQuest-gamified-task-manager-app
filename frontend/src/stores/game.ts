import { defineStore } from "pinia";
import axios from "axios";
interface UserState {
    //user state interface to track level and xp
    level: number;
    xp: number;
}
interface Task {
    //task interface to define the structure of a task
    id: number;
    title: string;
    description: string;
    difficulty: number;
    intensity: number;
    completed: boolean;
}
export const useGameStore = defineStore("game", {
    //define a Pinia store named 'game'
    state: () => ({
        user: {
            level: 1,
            xp: 0,
        } as UserState,
        tasks: [] as Task[],
    }),
    getters: {
        xpProgress(): number {
            //get the percentage of XP progress towards the next level
            const xpForNextLevel = this.user.level * 100;
            return (this.user.xp / xpForNextLevel) * 100;
        },
    },
    actions: {
        async fetchProfile() {
            //fetch user profile and tasks from the backend
            try {
                // Fetch user profile from the backend
                const profileRes = await axios.get("/api/user/profile");
                this.user = profileRes.data;

                // Simultaneously fetch tasks from our new route
                const tasksRes = await axios.get("/api/tasks");
                this.tasks = tasksRes.data;
            } catch (error) {
                // Handle errors gracefully
                console.error("Failed to load initial dataset:", error);
            }
        },
        async createTask(
            title: string,
            description: string,
            difficulty: number,
            intensity: number,
        ) {
            //create a new task by sending a POST request to the backend
            try {
                const res = await axios.post("/api/tasks/create", {
                    title,
                    description,
                    difficulty,
                });
                this.tasks.push(res.data);
            } catch (error) {
                console.error("Error creating task:", error);
            }
        },
        async completeTask(taskId: number) {
            //mark a task as completed by sending a POST request to the backend and update user state accordingly
            try {
                const res = await axios.post(`/api/tasks/${taskId}/complete`);
                this.user = res.data.user;
                const task = this.tasks.find((t) => t.id === taskId);
                if (task) {
                    task.completed = true;
                }
                if (res.data.leveledUp) {
                    alert("Congratulations! You leveled up!");
                }
            } catch (error) {
                console.error("Error completing task:", error);
            }
        },
        async deleteTask(taskId: number) {
            //delete a task by sending a DELETE request to the backend and remove it from the local state
            try {
                await axios.delete(`/api/tasks/${taskId}/delete`);
                this.tasks = this.tasks.filter((t) => t.id !== taskId);
            } catch (error) {
                console.error("Error deleting task:", error);
            }
        },
    },
});
