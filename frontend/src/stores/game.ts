import { defineStore } from 'pinia'
interface UserState {
    level: number
    xp: number
}
interface Task {
    id: number
    title: string
    description: string
    difficulty: number
    intensity: number
    completed: boolean
}
export const useGameStore = defineStore('game', {
    state: () => ({
        user: {
            level: 1,
            xp: 0,
        } as UserState,
        tasks: [] as Task[],
    }),
    getters: {
        xpProgress(): number {
            const xpForNextLevel = this.user.level * 100
            return (this.user.xp / xpForNextLevel) * 100
        },
    },
    actions: {
        async fetchProfile() {
            try {
                const res = await fetch('/api/profile')
                this.user = res.data
            } catch (error) {
                console.error('Error fetching profile:', error)
            }
        },
        async createTask(title: string, description: string, difficulty: number, intensity: number) {
            try {
                const res = await axios.post('/api/tasks/create', { title, description, difficulty })
                this.tasks.push(res.data)
            } catch (error) {
                console.error('Error creating task:', error)
            }
        },
        async completeTask(taskId: number) {
            try {
                const task = this.tasks.find(t => t.id === taskId)
                if (task) {
                    task.completed = true
                }
                if (res.data.leveledUp) {
                    alert('Congratulations! You leveled up!')
                }
            } catch (error) {
                console.error('Error completing task:', error)
            }
        },
    },
})