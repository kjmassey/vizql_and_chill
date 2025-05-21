<template>
    <v-overlay v-model="$props.showOverlay" opacity="1" scrim="black" class="align-center justify-center">
        <div class="d-flex align-center justify-center">
            <v-progress-circular color="red" size="88" width="10" :model-value="(loadingStep / loadingStepCount) * 100"
                rotate="360"></v-progress-circular>
        </div>
        <div class="d-flex justify-center mt-4 text-h6 w-100">
            <div>{{ loadingMessage }}</div>
            <div :class="dotCount < 2 ? 'zero-opacity' : null">.</div>
            <div :class="dotCount < 3 ? 'zero-opacity' : null">.</div>
            <div :class="dotCount <= 3 ? 'zero-opacity' : null">.</div>
        </div>
        <div id="authViz">
            <template v-if="userStore.userJwt && loadingStep === 4">
                <div style="position: relative; top: 0; left: 0; opacity: 1; height: 0px; opacity: 0;" id="authViz">
                    <tableau-viz src="https://YOUR-SITE-PATH/views/auth_viz/Auth" device="desktop"
                        hide-tabs toolbar="hidden" :token="userStore.userJwt" width="300px" height="200">
                    </tableau-viz>
                </div>
            </template>
        </div>
    </v-overlay>

</template>

<script>
import { useUserStore } from '@/stores/user';
import { useContentStore } from '@/stores/content';
import { toRaw } from 'vue';

export default {
    name: 'LoadingOverlay',
    setup() {
        const userStore = useUserStore();
        const contentStore = useContentStore();

        return { userStore, contentStore };
    },
    data: () => ({
        loadingMessage: "Loading...",
        dotCount: 1,
        dotInterval: null,
        elippsisStr: "...",
        loadingStepCount: 5,
        loadingStep: 0,
    }),
    props: {
        showOverlay: { type: Boolean, default: true },
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
                    this.loadingStep += 1;
                });
            });
        },
        async handleMutation(mutationsList) {
            for (const mutation of mutationsList) {

                if (mutation.target.localName === 'tableau-viz') {
                    await this.initViz();
                    this.loadingStep += 1;

                    setTimeout(() => {
                        clearInterval(this.dotInterval)
                        this.$emit('loadingComplete')
                    }, 500)
                }
            }
        },
        getRandomInt(min, max) {
            return Math.floor(Math.random() * (max - min + 1) + min);
        },
        async randomArrayFromIds(arrLength) {
            let contentNoWorkbooks = this.contentStore.allSiteContent.filter(e => e.contentType !== 'workbook')
            let randArr = Array.from({ length: arrLength }, () => this.getRandomInt(0, contentNoWorkbooks.length - 1))

            this.contentStore.carouselItems = randArr.map(e => toRaw(this.contentStore.allSiteContent[e]))
        },
    },
    async mounted() {
        if (!this.userStore.selectedUser) {
            this.$router.push('/')
        } else {


            // MAKE ELIPPSIS DO ITS THING
            this.dotInterval = setInterval(() => { this.dotCount > 3 ? this.dotCount = 1 : this.dotCount += 1 }, 250)


            // WATCH FOR VIZ
            const targetNode = document.getElementById("authViz");
            const config = { attributes: true, childList: true, subtree: true };

            this.observer = new MutationObserver(this.handleMutation);
            this.observer.observe(targetNode, config);

            // GET USER JWT
            this.loadingMessage = "Getting User Token";
            await this.userStore.fetchUserJwt();
            this.loadingStep += 1;

            // GET SITE CONTENT
            this.loadingMessage = "Getting Site Content";
            await this.userStore.fetchUserJwt()
            await this.contentStore.vdsGetAllSiteContent(true);
            await this.userStore.fetchUserJwt()
            // console.log("+++++ STARTING SECOND CONTENT CALL")
            // this.contentStore.vdsGetAllSiteContent(false);
            this.loadingStep += 1;

            // GET USER RATINGS
            this.loadingMessage = "Getting User Ratings";
            await this.userStore.fetchUserContentRatings();

            for (const item of this.userStore.userContentRatings) {
                this.contentStore.getContentDetails(item.item)
            }
            this.loadingStep += 1;

            // GET USER FAVORITES
            this.loadingMessage = "Getting User Favorites"
            await this.contentStore.getUserFavorites(this.userStore.selectedUser.userLuid);
            this.loadingStep += 1

            // TABLEAU AUTH
            await this.userStore.fetchUserJwt()
            this.loadingMessage = "Authenticating w/ Tableau"
        }
    }

};

</script>

<style scope>
.zero-opacity {
    opacity: 0;
}
</style>