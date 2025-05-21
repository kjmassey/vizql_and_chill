<template>

    <v-fab :color="$props.color" icon="mdi-menu" app location="top right" class="pl-4" @click="showMenuDial = true"
        style="z-index: 1000" size="70">


        <v-avatar color="primary" size="64">
            <v-img :src="userStore.selectedUser.imgUrl" style="position: absolute;" fill />
        </v-avatar>
        <v-speed-dial v-model="showMenuDial" location="bottom" activator="parent"
            transition="slide-y-reverse-transition">

            <div class="d-flex justify-start align-center pl-2 speed-dial-item" key="1">
                <v-btn key="1" color="primary" icon>
                    <v-icon size="24">mdi-account</v-icon>
                </v-btn>
                <div class="pl-2 text-subtitle-2">
                    My Stuff
                </div>
            </div>

            <div class="d-flex justify-start align-center pl-2 speed-dial-item" key="1">
                <v-btn key="1" color="red-darken-3" icon>
                    <v-icon size="24">mdi-timeline</v-icon>
                </v-btn>
                <div class="pl-2 text-subtitle-2">
                    User Activity
                </div>
            </div>

            <div class="d-flex justify-start align-center pl-2 speed-dial-item" key="1">
                <v-btn key="1" color="amber-darken-1" icon>
                    <v-icon size="24">mdi-folder-multiple</v-icon>
                </v-btn>
                <div class="pl-2 text-subtitle-2">
                    Projects & Content
                </div>
            </div>

            <div class="d-flex justify-start align-center pl-2 speed-dial-item" key="2">
                <v-btn key="2" color="secondary" icon>
                    <v-icon size="24">mdi-trending-up</v-icon>
                </v-btn>
                <div class="pl-2 text-subtitle-2">
                    Trending
                </div>
            </div>

            <div class="d-flex justify-start align-center pl-2 speed-dial-item" key="3">
                <v-btn key="3" color="purple-darken-3" icon>
                    <v-icon size="24">mdi-new-box</v-icon>
                </v-btn>
                <div class="pl-2 text-subtitle-2">
                    New Content
                </div>
            </div>

            <div class="d-flex justify-start align-center pl-2 speed-dial-item" key="4">
                <v-btn key="4" color="error" icon>
                    <v-icon size="24">mdi-alert-octagram</v-icon>
                </v-btn>
                <div class="pl-2 text-subtitle-2">
                    My Alert(s)
                </div>
            </div>
        </v-speed-dial>

    </v-fab>
    <SearchFab />


</template>

<script>
import { useUserStore } from '@/stores/user'
import SearchFab from './SearchFab.vue';

export default {
    name: "MainSpeedDial",
    setup() {
        const userStore = useUserStore()

        return { userStore }
    },
    components: {
        SearchFab
    },
    data: () => ({
        showMenuDial: false
    }),
    props: {
        color: { type: String, default: 'darkgrey' }
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