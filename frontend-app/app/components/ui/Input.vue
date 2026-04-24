<template>
    <input v-model="model!.value" />
</template>
<script lang="ts" setup>
import z from "zod";

const model = defineModel<{
    value: string;
    error: string;
}>();

const props = defineProps<{
    schema: z.ZodType;
}>();

watch(model, () => {
    const result = z.safeParse(props.schema, model);
    if (result.success) {
        model.value!.error = "";
    } else {
        model.value!.error = result.error.message;
    }
});
</script>
<style lang="scss" scoped>
input {
    display: block;
    border: 1px solid #c1c1c1;
    border-radius: 16px;
    padding: 0 1rem;
    height: 3rem;
    outline: none;
}
</style>
