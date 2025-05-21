<template>
    <v-overlay v-model="$props.showOverlay" scrim="black" opacity=".9" content-class="fill-height w-100">
        <v-container class="fill-height justify-center align-center">

            <v-responsive class="mt-0" max-width="1100px">


                <v-fab icon="mdi-close" location="top right" @click="$emit('closeSearchOverlay')" style="z-index: 1000"
                    app>
                </v-fab>
                <div id="searchResultsContainer">
                    <v-card v-show="$props.showOverlay" class="pa-4 flex-grow-1" color="transparent" max-height="100%">
                        <v-card-text class="d-flex align-center justify-center">
                            <v-img src="../../public/logo.png" max-width="750" contain></v-img>
                        </v-card-text>
                        <v-card-text class="d-flex align-center justify-center">
                            <v-text-field variant="solo-filled"
                                placeholder="Search workbooks, datasources, connections, and more..."
                                label="Find your next bingeable data experience..." hide-details
                                v-model="contentStore.searchTerm" clearable
                                @click:clear="contentStore.resetSearchResults" @keyup.enter="doSearch"
                                rounded></v-text-field>
                            <v-btn color="transparent" :ripple="false" flat elevation="0" class="mx-2" @click="doSearch"
                                :loading="contentStore.isLoading">
                                <v-icon size="30">mdi-magnify</v-icon>
                            </v-btn>
                        </v-card-text>
                    </v-card>
                </div>

            </v-responsive>
        </v-container>
    </v-overlay>
</template>

<script>
import { useContentStore } from '@/stores/content';

export default {
    name: 'SearchOverlay',
    setup() {
        const contentStore = useContentStore();

        return { contentStore };
    },
    props: {
        showOverlay: { type: Boolean, default: false },


    },
    data: () => ({
        searchTerm: '',
        cardTextHeight: 0,
        selfIsShown: false,
    }),
    computed: {
        //
    },
    methods: {
        async handleMutation(mutations) {

            for (const mutation in mutations) {
            }
        },
        async doSearch() {
            let searchObj = {
                searchTerm: this.contentStore.searchTerm,
                searchLimit: 4,
            }

            this.contentStore.isLoading = true;

            for (const type of this.contentStore.uniqueContentTypes) {
                searchObj.objectType = type;

                await this.contentStore.searchForContent(searchObj);

                if (this.contentStore.searchResults.length > 0) {
                    this.$emit('openSearchResults');
                }
            }

            // await this.contentStore.searchForContent(searchObj);
            this.contentStore.isLoading = false;

            this.$emit('closeSearchOverlay');
        },
    },
    async mounted() {
        // WATCH FOR RESULTS


    }
}


</script>

<style scoped>
.zero-height {
    height: 0px;
}
</style>