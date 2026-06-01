/** @type {import('tailwindcss').Config} */
export default {
    content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
    theme: {
        extend: {
            colors: {
                quest: {
                    bg: "#0f172a", // Slate 900
                    card: "#1e293b", // Slate 800
                    gold: "#eab308", // Yellow 500
                    xp: "#a855f7", // Purple 500
                },
            },
        },
    },
    plugins: [],
};
