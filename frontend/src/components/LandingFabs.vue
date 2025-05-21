<template>
    <v-app-bar app color="transparent" dark elevation="0" elevate>
        <v-spacer></v-spacer>
        <div>
            <v-avatar size="50" @click="$emit('showSearch')">
                <v-btn icon color="grey-darken-3" variant="flat">
                    <v-icon>mdi-magnify</v-icon>
                </v-btn>
            </v-avatar>
        </div>
        <div class="px-4">
            <v-avatar :color="userStore.selectedUser.color" size="50">
                <v-avatar size="46">
                    <v-img :src="userStore.selectedUser.imgUrl" style="position: absolute;" fill />
                </v-avatar>
            </v-avatar>

        </div>


    </v-app-bar>

</template>

<script>
import { useUserStore } from '@/stores/user';

export default {
    name: 'LandingFabs',
    setup() {
        const userStore = useUserStore();

        return { userStore };
    },

    data: () => ({
        showMenuDial: false,
    }),
    props: {
        //
    },
    components: {
        //
    },
    computed: {
        //
    },
    methods: {
        //
    }
}
</script>

<style scoped>
.speed-dial-item {
    background-color: rgb(22, 22, 29, .85);
    padding: 12px 24px;
    border-radius: 10px;
}
</style>