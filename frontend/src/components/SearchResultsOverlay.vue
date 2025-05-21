<template>
    <EmbeddedContentViewer @closeEmbeddedContentViewer="showEmbeddedContentViewer = false"
        v-if="showEmbeddedContentViewer" :contentUrl="embeddedContentUrl" :props-obj="embeddedContentProps" />
    <v-overlay v-model="$props.showOverlay" scrim="black" opacity=".92" content-class="fill-height">
        <v-container fluid class="justify-center align-center" min-width="100vw" max-width="100vw">

            <v-responsive class="justify-center">


                <v-menu v-model="menu" :close-on-content-click="false" location="end"
                    style="margin-left: 48px; margin-top: 64px;" persistent>
                    <template v-slot:activator="{ props }">
                        <v-fab icon="mdi-filter" location="top left" @click="menu = true" style="z-index: 1000" app>

                            <v-badge dot :color="activeFilters ? 'red' : 'transparent'">
                                <div class="w-100">
                                    <v-icon size="28">mdi-filter</v-icon>
                                </div>
                            </v-badge>
                        </v-fab>
                    </template>

                    <v-card min-width="300">
                        <v-list>
                            <v-list-item title="Filter Results">

                            </v-list-item>
                        </v-list>

                        <v-divider></v-divider>

                        <v-list>
                            <v-list-item>
                                <v-autocomplete :items="contentStore.uniqueContentTypes" v-model="contentTypesFilter"
                                    multiple label="Types" hide-details variant="outlined" density="compact"
                                    class="mt-2" chips closable-chips></v-autocomplete>
                            </v-list-item>

                        </v-list>

                        <v-card-actions>
                            <v-spacer></v-spacer>

                            <v-btn variant="text" @click="menu = false">
                                Close
                            </v-btn>

                        </v-card-actions>
                    </v-card>
                </v-menu>
                <v-fab icon="mdi-close" location="top right" @click="backToSearch" style="z-index: 1000" app>
                </v-fab>
                <div style="height: 100vh; overflow-y: auto;">
                    <div class="d-flex justify-center align-center">
                        <v-img src="../../public/logo_small.png" max-width="32" class="mx-8" />

                        <v-text-field placeholder="Search" variant="solo-filled" hide-details max-width="800px" rounded
                            clearable v-model="contentStore.searchTerm" density="compact" @keyup.enter="doSearch"
                            @click:clear="contentStore.resetSearchResults">
                        </v-text-field>


                        <v-btn color="transparent" :ripple="false" flat elevation="0" class="mx-2"
                            :loading="contentStore.isLoading">
                            <v-icon size="30" @click="doSearch" :loading="contentStore.isLoading">mdi-magnify</v-icon>
                        </v-btn>
                    </div>
                    <v-container fluid app class="w-100">
                        <v-row>
                            <v-col cols="12"></v-col>
                        </v-row>

                        <!-- BEGIN VIEWS -->
                        <template
                            v-if="contentTypesFilter.includes('View') && contentStore.searchResults.filter(e => e.content.type === 'view').length > 0">
                            <v-row class="mt-12"></v-row>
                            <v-row>
                                <v-col cols="1"></v-col>
                                <v-col cols="10">
                                    <div class="d-flex justify-center align-center flex-grow-1 flex-wrap">

                                        <ExpanderNew :title="'Views'"
                                            :items-list="contentStore.formattedSearchResultsByType('view')"
                                            :show-all="false" :item-type="'View'"
                                            @openContentPreviewModal="(e) => { openInEmbeddedViewer(e) }"
                                            :is-search-results="true" />
                                    </div>
                                </v-col>
                                <v-col cols="1"></v-col>
                            </v-row>
                        </template>

                        <!-- BEGIN WORKBOOKS -->
                        <template
                            v-if="contentTypesFilter.includes('Workbook') && contentStore.searchResults.filter(e => e.content.type === 'workbook').length > 0">
                            <v-row class="mt-12"></v-row>
                            <v-row>
                                <v-col cols="1"></v-col>
                                <v-col cols="10">
                                    <div class="d-flex justify-center align-center flex-grow-1 flex-wrap">

                                        <ExpanderNew :title="'Workbooks'"
                                            :items-list="contentStore.formattedSearchResultsByType('workbook')"
                                            :show-all="false" :item-type="'Workbook'"
                                            @openContentPreviewModal="(e) => { openInEmbeddedViewer(e) }"
                                            :is-search-results="true" />
                                    </div>
                                </v-col>
                                <v-col cols="1"></v-col>
                            </v-row>
                        </template>

                        <!-- BEGIN DATASOURCES -->
                        <template
                            v-if="contentTypesFilter.includes('Datasource') && contentStore.searchResults.filter(e => e.content.type === 'datasource').length > 0">
                            <v-row class="mt-12"></v-row>
                            <v-row>
                                <v-col cols="1"></v-col>
                                <v-col cols="10">
                                    <div class="d-flex justify-center align-center flex-grow-1 flex-wrap">

                                        <ExpanderNew :title="'Datasources'"
                                            :items-list="contentStore.formattedSearchResultsByType('datasource')"
                                            :show-all="false" :item-type="'Datasource'"
                                            @openContentPreviewModal="(e) => { openInEmbeddedViewer(e) }"
                                            :is-search-results="true" />
                                    </div>
                                </v-col>
                                <v-col cols="1"></v-col>
                            </v-row>
                        </template>

                        <!-- BEGIN PROJECTS -->
                        <template
                            v-if="contentTypesFilter.includes('Project') && contentStore.searchResults.filter(e => e.content.type === 'project').length > 0">
                            <v-row class="mt-12"></v-row>
                            <v-row>
                                <v-col cols="1"></v-col>
                                <v-col cols="10">
                                    <div class="d-flex justify-center align-center flex-grow-1 flex-wrap">

                                        <ExpanderNew :title="'Projects'"
                                            :items-list="contentStore.formattedSearchResultsByType('project')"
                                            :show-all="false" :item-type="'Project'"
                                            @openContentPreviewModal="(e) => { openInEmbeddedViewer(e) }"
                                            :is-search-results="true" />
                                    </div>
                                </v-col>
                                <v-col cols="1"></v-col>
                            </v-row>
                        </template>

                    </v-container>



                </div>
            </v-responsive>
        </v-container>
    </v-overlay>
</template>

<script>
import { useContentStore } from '@/stores/content';
import ContentPreviewNew from './ContentPreviewNew.vue';
import { tableauUrlRoot, tableauSite } from '@/stores/consts';
import EmbeddedContentViewer from './EmbeddedContentViewer.vue';
import Expander from './Expander.vue';
import ExpanderNew from './ExpanderNew.vue';

export default {
    name: 'SearchResultsOverlay',
    setup() {
        const contentStore = useContentStore();

        return { contentStore };
    },
    props: {
        showOverlay: { type: Boolean, default: false },
    },
    components: {
        ContentPreviewNew,
        EmbeddedContentViewer,
        Expander,
        ExpanderNew
    },
    data: () => ({
        urlRoot: tableauUrlRoot,
        site: tableauSite,
        menu: false,
        contentTypesFilter: ['View', 'Workbook', 'Datasource', 'Project'],
        contentLikedFilter: false,
        contentFavoritedFilter: false,
        showEmbeddedContentViewer: false,
        embeddedContentUrl: '',
        embeddedContentProps: {},
        showFilteredResults: false,
    }),
    computed: {
        activeFilters() {
            if (this.contentTypesFilter.length !== 4) {
                return true
            }

            if (this.contentLikedFilter) {
                return true
            }
            if (this.contentFavoritedFilter) {
                return true
            }
        }
    },
    methods: {
        async doSearch() {
            let searchObj = {
                searchTerm: this.contentStore.searchTerm,
                searchLimit: 5,
            }

            this.contentStore.isLoading = true;
            this.contentStore.resetSearchResults();
            this.contentStore.resetSearchResultsCountsByType();

            for (const type of this.contentStore.uniqueContentTypes) {
                searchObj.objectType = type;

                await this.contentStore.searchForContent(searchObj);
            }

            this.contentStore.isLoading = false;
        },

        backToSearch() {
            this.$emit('closeSearchResultsOverlay');

        },
        buildImgUrl(itemContent) {
            let urlBase = `${this.urlRoot}/t/${this.site}/views`;

            switch (itemContent.type) {
                case 'workbook':
                    return `${urlBase}/${itemContent.defaultViewUrl}.png`;

                case 'view':
                    return `${urlBase}/${itemContent.path}.png`;

                case 'datasource':
                    return `${this.urlRoot}/t/${this.site}/datasources/${itemContent.id}.png`;
                default:
                    return `${this.urlRoot}/t/${this.site}/views/${itemContent.defaultViewUrl}.png`;
            }
        },
        filterSearchResults() {
            let filterObj = {
                types: this.contentTypesFilter,
                likedByMe: this.contentLikedFilter,
                favoritedByMe: this.contentFavoritedFilter
            }

            this.contentStore.getFilteredSearchResults(filterObj)
        },
        getContentUrl(luid, itemType) {
            //
        },
        openInEmbeddedViewer(e) {


            if (e[e.type].contentUrl.slice(0, 5) === 'https') {
                this.embeddedContentUrl = e[e.type].contentUrl.replace("sheets/", "")
            } else {
                this.embeddedContentUrl = `${tableauUrlRoot}/#/site/${tableauSite}/views/${e[e.type].contentUrl}`.replace("sheets/", "")
            }
            this.embeddedItem = e
            this.embeddedContentProps = e
            this.showEmbeddedContentViewer = true
        }
    },
    async mounted() {
        //

    }
}
</script>

<style scoped>
/* */
</style>