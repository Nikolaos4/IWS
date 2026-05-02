<template>
    <header>
        <NuxtLink
            class="logo"
            to="/"
            >IWS</NuxtLink
        >

        <div
            v-if="auth.currentUser"
            class="current-account">
            {{ auth.currentUser.username }}
        </div>
    </header>
</template>
<script lang="ts" setup>
const auth = useAuthStore();
</script>
<style lang="scss" scoped>
header {
    height: 3rem;

    .logo {
        color: var(--color-primary);
        font-weight: bold;
        font-size: 2rem;
        text-decoration: none;
    }
}
</style>
