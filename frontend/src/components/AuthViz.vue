<template>
    <template v-if="userStore.userJwt && userStore.userJwt">
        <div style="position: relative; top: 0; left: 0; opacity: 1; height: 100px; border:1px solid red">
            <tableau-viz src="https://YOUR-SITE-PATH/views/auth_viz/Auth" device="desktop"
                hide-tabs toolbar="hidden" :token="userStore.userJwt && userStore.userJwt" width="300px" height="200">
            </tableau-viz>
        </div>
    </template>
</template>

<script>
import { useUserStore } from '@/stores/user';

export default {
    name: 'AuthViz',
    setup() {
        const userStore = useUserStore();

        return { userStore };
    },
    methods: {
        async initViz() {


            // This is required when the page loads and any time the embedded viz changes in order for it to be interactive!

            // Set the <tableau-viz> component to be our embedded viz for interactivity -- this all works because of the import added to index.html
            const viz = document.querySelector("tableau-viz");

            this.embeddedViz = viz;

            // Add an event listener to verify the viz becomes interactive
            await new Promise((resolve) => {
                this.embeddedViz.addEventListener("firstinteractive", () => {
                    resolve();

                    this.$emit('vizIsInteractive')
                });
            });
        }
    },
    async mounted() {
        await this.initViz();
    }

};

</script>