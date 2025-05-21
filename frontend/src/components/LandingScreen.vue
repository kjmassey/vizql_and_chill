<template>

  <template v-if="showLoadingOverlay">
    <LoadingOverlay :showOverlay="showLoadingOverlay" @loadingComplete="showLoadingOverlay = false" />
  </template>
  <template v-show="showSearchOverlay">
    <SearchOverlay :showOverlay="showSearchOverlay" @openSearchResults="showSearchResultsOverlay = true"
      @closeSearchOverlay="showSearchOverlay = false" />
  </template>
  <template v-show="showSearchResultsOverlay">
    <SearchResultsOverlay :showOverlay="showSearchResultsOverlay"
      @closeSearchResultsOverlay="showSearchResultsOverlay = false; showSearchOverlay = false"
      @showSearchOverlay="showSearchOverlay = true" />
  </template>
  <template v-if="contentStore.allSiteContent.length > 0">
    <LandingFabs @showSearch="showSearchOverlay = true" />
    <HeroCarousel @show-embedded-view="(e) => { openInEmbeddedViewer(e) }" />
    <v-container class="fill-height" fluid>

      <v-responsive class=" fill-height fill-width w-100 mx-auto">
        <div class="py-4 px-2">
          <ExpanderNew :title="'🔖 My Favorites'"
            :items-list="contentStore.userFavorites.favorites && contentStore.userFavorites.favorites.favorite"
            :show-all="false" @openContentPreviewModal="(e) => { openInEmbeddedViewer(e) }" />

        </div>

        <div class="py-4 px-2">
          <ExpanderNew :title="'👍 Liked by Me'"
            :items-list="contentStore.formattedUserRatings().filter(e => e.rating === 1)" :show-all="false"
            @openContentPreviewModal="(e) => { openInEmbeddedViewer(e) }" />

        </div>

        <template v-if="contentStore.showFeaturedAuthorContent">
          <div class="py-4 px-2">
            <ExpanderNew :title="'🫶🏻 Featured Author: Lindsay Betzendahl'"
              :items-list="contentStore.featuredAuthorContent && contentStore.featuredAuthorContent" :show-all="false"
              @openContentPreviewModal="(e) => { showEmbeddedContentViewer = true; embeddedContentUrl = e }" />

          </div>
        </template>

        <template v-if="contentStore.showNewContent">
          <div class="py-4 px-2">
            <ExpanderNew :title="'🆕 New Content'" :items-list="contentStore.newContent && contentStore.newContent"
              :show-all="false"
              @openContentPreviewModal="(e) => { showEmbeddedContentViewer = true; embeddedContentUrl = e }" />

          </div>
        </template>


        <template v-if="contentStore.showFeaturedContent1">
          <div class="py-4 px-2">
            <ExpanderNew :title="'🧭 Featuring Maps'"
              :items-list="contentStore.featuredContent1 && contentStore.featuredContent1" :show-all="false"
              @openContentPreviewModal="(e) => { showEmbeddedContentViewer = true; embeddedContentUrl = e }" />

          </div>
        </template>

        <template v-if="contentStore.showFeaturedContent5">
          <div class="py-4 px-2">
            <ExpanderNew :title="'🍿 Movies'"
              :items-list="contentStore.featuredContent5 && contentStore.featuredContent5" :show-all="false"
              @openContentPreviewModal="(e) => { showEmbeddedContentViewer = true; embeddedContentUrl = e }" />

          </div>
        </template>

        <template v-if="contentStore.showFeaturedContent2">
          <div class="py-4 px-2">
            <ExpanderNew :title="'🏈 Sports'"
              :items-list="contentStore.featuredContent2 && contentStore.featuredContent2" :show-all="false"
              @openContentPreviewModal="(e) => { showEmbeddedContentViewer = true; embeddedContentUrl = e }" />

          </div>
        </template>

        <template v-if="contentStore.showFeaturedContent3">
          <div class="py-4 px-2">
            <ExpanderNew :title="'🗄️ Business'"
              :items-list="contentStore.featuredContent3 && contentStore.featuredContent3" :show-all="false"
              @openContentPreviewModal="(e) => { showEmbeddedContentViewer = true; embeddedContentUrl = e }" />

          </div>
        </template>

        <template v-if="contentStore.showAgedContent">
          <div class="py-4 px-2">
            <ExpanderNew :title="'👴🏻 Aged Content'" :items-list="contentStore.agedContent && contentStore.agedContent"
              :show-all="false"
              @openContentPreviewModal="(e) => { showEmbeddedContentViewer = true; embeddedContentUrl = e }" />

          </div>
        </template>


        <template v-if="localIsLoading">
          <div class="py-4 px-2 w-100 d-flex justify-center align-center">
            <v-progress-circular indeterminate color="red" size="48" width="8"></v-progress-circular>
          </div>
        </template>

        <EmbeddedContentViewer @closeEmbeddedContentViewer="showEmbeddedContentViewer = false"
          v-if="showEmbeddedContentViewer" :contentUrl="embeddedContentUrl" :props-obj="embeddedItem" />

      </v-responsive>
    </v-container>
  </template>
</template>

<script>
import ContentPreview from './ContentPreview.vue'
import EmbeddedContentViewer from './EmbeddedContentViewer.vue'
import SearchFab from './SearchFab.vue'
import MainSpeedDial from './MainSpeedDial.vue'
import { useUserStore } from '@/stores/user'
import LoadingOverlay from './LoadingOverlay.vue'
import SearchOverlay from './SearchOverlay.vue'
import SearchResultsOverlay from './SearchResultsOverlay.vue'
import { useContentStore } from '@/stores/content'
import ContentPreviewNew from './ContentPreviewNew.vue'
import LandingFabs from './LandingFabs.vue'
import HeroCarousel from './HeroCarousel.vue'
import ExpanderNew from './ExpanderNew.vue'
import { VSkeletonLoader } from 'vuetify/components/VSkeletonLoader'
import { tableauUrlRoot, tableauSite } from '@/stores/consts'

export default {
  setup() {
    const userStore = useUserStore()
    const contentStore = useContentStore()

    return { userStore, contentStore }
  },
  name: 'LandingScreen',
  data: () => ({
    showLoadingOverlay: false,
    showSearchOverlay: false,
    showSearchResultsOverlay: false,
    showEmbeddedContentViewer: false,
    embeddedContentUrl: '',
    embeddedContentProps: {},
    showMenuDial: false,
    embeddedItem: null,
    localIsLoading: false
  }),
  props: {
    userHasAccess: { type: Boolean, default: false },
    imgUrl: { type: String, default: '' },
  },
  components: {
    ContentPreview,
    ContentPreviewNew,
    EmbeddedContentViewer,
    MainSpeedDial,
    SearchFab,
    LoadingOverlay,
    SearchOverlay,
    SearchResultsOverlay,
    LandingFabs,
    HeroCarousel,
    ExpanderNew,
    VSkeletonLoader
  },
  computed: {
    showLoader() {
      let loadingStatuses = [
        this.contentStore.showFeaturedContent1,
        this.contentStore.showFeaturedContent2,
        this.contentStore.showFeaturedContent3,
        this.contentStore.showFeaturedContent4
      ]

      let anyFalse = loadingStatuses.some(status => status === false)

      return anyFalse ? true : false
    }
  },
  methods: {

    handleShowEmbeddedViewer(e) {
      this.embeddedContentUrl = e
      this.showEmbeddedContentViewer = true
    },
    getCarouselImgUrl(item) {
      return `${item['Item Hyperlink'].replace('/#/site/', '/t/')}.png`
    },
    getViewUrlStr(url) {
      return url && url.replace("sheets/", "")
    },
    openInEmbeddedViewer(e) {
      console.log("OPENING IN EMBEDDED VIEWER")
      console.log("ITEM", e)

      if (e[e.type].contentUrl.slice(0, 5) === 'https') {
        this.embeddedContentUrl = e[e.type].contentUrl.replace("sheets/", "")
      } else {
        this.embeddedContentUrl = `${tableauUrlRoot}/#/site/${tableauSite}/views/${e[e.type].contentUrl}`.replace("sheets/", "")
      }
      
      this.embeddedItem = e
      this.showEmbeddedContentViewer = true
    }

  },
  async mounted() {
    if (!this.userStore.selectedUser.name) {
      this.showLoadingOverlay = false
      this.$router.push('/')
    } else {
      this.showLoadingOverlay = true
      await this.userStore.fetchUserJwt()

    }
    

  },
  watch: {
    showLoadingOverlay: {
      async handler(newVal, oldVal) {


        this.localIsLoading = true

        if (!newVal) {

          if (this.contentStore.featuredAuthorContent.length === 0) {
            await this.contentStore.getFeaturedAuthorContent()
            this.contentStore.updateFeaturedAuthorContent()
          }

          if (this.contentStore.newContent.length === 0) {
            await this.contentStore.getNewContent()
            this.contentStore.updateNewContent()
          }


          if (this.contentStore.featuredContent1.length === 0) {
            await this.contentStore.getContentByTag('maps')
            this.contentStore.updateFeatured1()
          }

          if (this.contentStore.featuredContent5.length === 0) {
            await this.contentStore.getContentByTag('movie')
            this.contentStore.updateFeatured5()
          }

          if (this.contentStore.featuredContent2.length === 0) {
            await this.contentStore.getContentByTag('sports')
            this.contentStore.updateFeatured2()
          }

          if (this.contentStore.featuredContent3.length === 0) {
            await this.contentStore.getContentByTag('business')
            this.contentStore.updateFeatured3()
          }

          if (this.contentStore.agedContent.length === 0) {
            await this.contentStore.getOldContent()
            this.contentStore.updateOldContent()
          }
          
          this.localIsLoading = false


        }
      },
    }
  }
}
</script>

<style scoped></style>
