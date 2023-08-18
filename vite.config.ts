import legacy from '@vitejs/plugin-legacy';
import vue from '@vitejs/plugin-vue';
import path from 'path';
import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue(), legacy(), VitePWA({
        registerType: 'autoUpdate',
        manifest: {
            name: 'Right Stuf',
            display: 'standalone',
            short_name: 'Right Stuf',
            background_color: '#ed3f3e',
            theme_color: '#ed3f3e',
            start_url: ".",
            icons: [
                {
                    src: '/assets/icon/192.png',
                    sizes: '192x192',
                    type: 'image/png',
                    purpose: "maskable"
                },
                {
                    src: '/assets/icon/192.png',
                    sizes: '192x192',
                    type: 'image/png',
                },
                {
                    src: '/assets/icon/512.png',
                    sizes: '512x512',
                    type: 'image/png',
                },
                {
                    src: '/assets/icon/512.png',
                    sizes: '512x512',
                    type: 'image/png',
                    purpose: "maskable"
                },
            ]
        }
    })],
    server: {
        port: 8080,
    },
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
    test: {
        globals: true,
        environment: 'jsdom',
    },
});
