<template>
    <nav>
        <ul>
            <li><NuxtLink to="/my">Профиль</NuxtLink></li>
            <li><NuxtLink to="/buy">Купить талоны</NuxtLink></li>
            <li><NuxtLink to="/use">Использовать талоны</NuxtLink></li>
        </ul>
        <ul class="bottom-links">
            <li><NuxtLink to="/verify">Верификация магазина</NuxtLink></li>
            <li><NuxtLink to="/settings">Настройки</NuxtLink></li>
        </ul>
    </nav>
</template>
<style lang="scss">
nav {
    display: flex;
    flex-direction: column;
    background-color: var(--color-background-secondary);
    border-radius: 0 16px 0 0;
    height: calc(100vh - 50px);
    min-width: 250px;

    ul {
        list-style: none;
        padding: 0;
        margin: 0;
        padding: 8px;

        &.bottom-links {
            margin-top: auto;
        }

        li {
            display: flex;

            a {
                color: inherit;
                text-decoration: none;
                padding: 8px;
                width: 100%;
                border-radius: 16px;

                &.router-link-active {
                    font-weight: bold;
                    color: var(--color-primary);
                }

                &:hover {
                    background-color: var(--color-background-pressed);
                }
            }
        }
    }
}
</style>
