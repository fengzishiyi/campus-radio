// 主 JavaScript 文件 — Vue 3 + Vuetify 3

const { createApp } = Vue;
const { createVuetify } = Vuetify;

const vuetify = createVuetify({
    theme: {
        defaultTheme: 'light',
        themes: {
            light: {
                colors: {
                    primary: '#3F51B5',
                },
            },
        },
    },
});

const app = createApp({
    // 使用 [[ ]] 作为模板分隔符，避免与 Django 模板 {{ }} 冲突
    delimiters: ['[[', ']]'],
});

app.use(vuetify);
app.mount('#app');
