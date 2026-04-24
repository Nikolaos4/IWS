<template>
    <button><slot /></button>
</template>
<style lang="scss" scoped>
button {
    background-color: var(--color-primary);
    color: white;
    border-radius: 16px;
    border: none;
    outline: none;
    height: 3rem;
    padding: 0 2rem;
    font-family: inherit;
    font-weight: bold;
    cursor: pointer;
}
</style>
