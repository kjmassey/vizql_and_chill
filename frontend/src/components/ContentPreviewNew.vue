<template>

  <div class="container" @mouseover="showDetails = true" @mouseleave="showDetails = false"
    :style="`width: ${$props.imgHeight}px; height: ${$props.imgHeight}px;`">
    <div style="position: relative; overflow: hidden;"
      :class="[$props.contentType === 'datasource' ? 'no-preview-background' : '']">
      <v-img :src="computedImageUrl" lazy-src="../../public/chart-lazy-load.png" :width="$props.imgHeight"
        :height="$props.imgHeight" cover :class="excludedContent ? 'blurred-image' : null" />
    </div>
    <div class="px-2" style="position: absolute; bottom: 0; width: 100%;">
      <div>
        <v-card>
          <v-card-text class="text-body-1 font-weight-bold my-2 py-0">
            <div class="d-flex align-center justify-space-between w-100">
              <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">

                <v-btn size="18" class="mr-2" @click="addRemoveFavorite" :loading="localFaveLoading"
                  :disabled="localFaveLoading">
                  <v-tooltip activator="parent" :text="isFavorited ? 'Remove Favorite' : 'Add Favorite'"
                    location="top"></v-tooltip>
                  <v-icon :color="isFavorited ? 'green' : null" size="18">{{ isFavorited ? 'mdi-check' : 'mdi-plus'
                  }}</v-icon>
                </v-btn>{{ computedItemName }}
              </div>
              <div class="d-flex">
                <div class="px-1">
                  <v-btn size="20"
                    @click="userStore.rateContent(userStore.selectedUser.userLuid, $props.itemObj[$props.itemObj.type].id, 0, $props.itemObj.type)">
                    <v-icon size="18" :color="isLikedDisliked == 0 ? 'error' : null">{{ isLikedDisliked === 0 ?
                      'mdi-thumb-down' :
                      'mdi-thumb-down-outline'
                    }}</v-icon>
                  </v-btn>
                </div>
                <div class="px-1">
                  <v-btn size="20"
                    @click="userStore.rateContent(userStore.selectedUser.userLuid, $props.itemObj[$props.itemObj.type].id, 1, $props.itemObj.type)">
                    <v-icon size="18" :color="isLikedDisliked == 1 ? 'primary' : null">{{ isLikedDisliked === 1 ?
                      'mdi-thumb-up' :
                      'mdi-thumb-up-outline' }}</v-icon>
                  </v-btn>
                </div>
              </div>
            </div>

          </v-card-text>
          <v-expand-transition>
            <v-card-text v-show="showDetails" class="my-0 py-0">
              <!-- OWNER AND DATES -->
              <div :style="`height: ${shadeHeight}px`">

                <div class="text-overline mt-0 pt-0">{{ computedItemType }}</div>

                <div class="d-flex align-center justify-space-between w-100">
                  <div class="d-flex align-center justify-start">

                    <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                      <v-icon>mdi-account-circle-outline</v-icon>
                      <span class="ml-2">{{ itemInContentStore ? itemInContentStore.owner_name : computedOwnerName
                        }}</span>
                    </div>
                  </div>
                  <div class="mr-2 d-flex align-center"
                    style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                    <v-icon>mdi-calendar</v-icon>
                    <span class="ml-2">{{ computedModifiedDate }}</span>

                  </div>

                </div>

                <div class="mt-6">
                  <div>
                    {{ itemInContentStore ? itemInContentStore.description : $props.contentDescription }}
                  </div>

                </div>

              </div>
            </v-card-text>

          </v-expand-transition>
          <v-fade-transition>
            <v-footer v-show="showDetails" flat>
              <div class="d-flex align-center justify-start w-100"
                v-if="['view', 'dashboard', 'workbook'].includes(computedItemType)">
                <v-icon>mdi-eye-outline</v-icon>
                <div class="text-subtitle-2 mx-2">
                  {{ itemInContentStore ? itemInContentStore.views : "-" }}
                </div>
              </div>
              <div class="d-flex align-center justify-end w-100" id="footer-icons">
                <div>
                  <v-menu location="top" style="z-index: 9999" attach class="mx-2">
                    <template v-slot:activator="{ props }">
                      <v-btn size="24" id="inner-menu-button" v-bind="props" flat>
                        <v-badge dot :color="computedItemTags.length > 0 ? 'red' : 'transparent'">
                          <v-icon>mdi-tag-outline</v-icon>
                        </v-badge>
                      </v-btn>
                    </template>

                    <v-list min-width="200" style="z-index: 9999; margin-left: -80px">
                      <v-list-item v-if="contentStore.tagsLoading">
                        <v-progress-circular indeterminate size="24"></v-progress-circular>
                      </v-list-item>
                      <v-list-item v-for="item, i in computedItemTags" :key="i" :value="i" density="compact">
                        <v-list-item-title><v-icon class="mr-4" size="18">mdi-tag</v-icon>{{ item }}</v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-menu>
                </div>
                <div v-if="excludedContent">
                  <v-btn size="20" flat>
                    <v-icon size="20">mdi-lock</v-icon>
                    <v-tooltip activator="parent" :text="'You can\'t access this content'" location="top"></v-tooltip>
                  </v-btn>
                </div>
                <div v-else-if="['view', 'dashboard'].includes(computedItemType)">
                  <v-btn size="28" flat @click="openContentInPreviewModal">
                    <v-icon size="28">mdi-fullscreen</v-icon>
                  </v-btn>
                </div>
                <div v-else-if="!['view', 'dashboard'].includes(computedItemType)">
                  <v-btn size="20" flat @click="openContentInNewTab($props.itemObj[$props.itemObj.type].id)"
                    :loading="localOpenLoading">
                    <v-icon size="20">mdi-open-in-new</v-icon>
                  </v-btn>
                </div>
              </div>
            </v-footer>
          </v-fade-transition>

        </v-card>

      </div>
    </div>
  </div>

</template>

<script>
import { useUserStore } from '@/stores/user'
import { useContentStore } from '@/stores/content'
import StarRating from 'vue-star-rating'
import { computed } from 'vue'
import { tableauUrlRoot, tableauSite } from '@/stores/consts'

export default {
  name: 'ContentPreviewNew',
  setup() {
    const userStore = useUserStore()
    const contentStore = useContentStore()

    return { userStore, contentStore }
  },
  data: () => ({
    showLockText: false,
    showFooter: false,
    showTooltip: false,
    rating: 3.6,
    showDetails: false,
    openInnerMenu: false,
    localFaveLoading: false,
    localOpenLoading: false,
    urlRoot: tableauUrlRoot,
    site: tableauSite,
  }),
  props: {
    userHasAccess: { type: Boolean, default: false },
    contentUrl: { type: String, default: '' },
    contentType: { type: String, default: null },
    imgUrl: { type: String, default: null },
    ownerName: { type: String, default: null },
    viewCount: { type: String, default: '12345' },
    imgHeight: { type: Number, default: 400 },
    contentName: { type: String, default: null },
    contentDescription: { type: String, default: 'This is the content desciption. This is the content desciption. This is the content desciption.' },
    modifiedDate: { type: String, default: null },
    luid: { type: String, default: '12345' },
    itemObj: { type: Object, default: {}, required: true },
  },
  components: {
    StarRating
  },
  computed: {
    excludedContent() {
      try {
        let excludedLuids = this.contentStore.getUserExcludedContentLuids(this.userStore.selectedUser.userLuid)
        return excludedLuids.includes(this.$props.itemObj[this.$props.itemObj.type].id)
      }
      catch (e) {
        return false
      }

      return excludedLuids.includes(this.$props.itemObj[this.$props.itemObj.type].id)
    },
    pillClass() {
      switch (this.contentType) {
        case 'workbook':
          return 'workbook-pill'
        case 'dashboard':
          return 'dashboard-pill'
        case 'datasource':
          return 'datasource-pill'
        case 'view':
          return 'view-pill'
        default:
          return 'workbook-pill'
      }
    },
    itemInContentStore() {
      try {
        return this.contentStore.contentDetails.find(e => e.luid === this.$props.itemObj[this.$props.itemObj.type].id)
      }
      catch (e) {
        return {}
      }
    },
    computedItemUrl() {
      if (['project', 'workbook'].includes(this.computedItemType)) {
        return this.itemInContentStore.url
      }

      else {
        return ''
      }
    }
    ,
    computedItemTags() {
      try {
        if (this.itemInContentStore) {
          return this.itemInContentStore.tags.split(',').map(e => e.trim())
        } else {
          return []
        }
      } catch {
        return []
      }
    },
    computedItemName() {
      try {
        if (this.$props.contentName) {
          return this.$props.contentName
        } else {
          return this.$props.itemObj[this.$props.itemObj.type].name
        }
      } catch (e) {
        return ''
      }
    },
    computedItemType() {
      try {
        if (this.$props.contentType) {
          return this.$props.contentType
        } else {
          return this.$props.itemObj.type
        }
      } catch {
        return ''
      }
    },
    computedOwnerName() {
      try {
        if (this.$props.ownerName) {
          return this.$props.ownerName
        } else {

          return this.$props.itemObj[this.$props.itemObj.type].owner.id.slice(0, 20)
        }
      }
      catch (e) {

        return ''
      }
    },
    computedModifiedDate() {
      try {
        if (this.$props.modifiedDate) {
          return this.$props.modifiedDate
        }
        else {
          return this.$props.itemObj[this.$props.itemObj.type].updatedAt.split("T")[0]
        }
      }
      catch (e) {
        try {
          return this.itemInContentStore.modified_date.split("T")[0]
        } catch (e) {
          return ''
        }
      }
    },
    computedImageUrl() {
      let urlBase = `${this.urlRoot}/t/${this.site}/views`;


      if (this.$props.imgUrl) {
        return this.$props.imgUrl
      } else {

        switch (this.$props.itemObj.type) {
          case 'workbook':
            try {
              let wbInContentStore = this.contentStore.workbookPreviewImages.find(e => e.wbLuid === this.$props.itemObj[this.$props.itemObj.type].id)



              return this.contentStore.workbookPreviewImages.length === 0 ? '' : 'data:image/jpeg;base64,' + wbInContentStore.image
            }
            catch (e) {

              return ''
            }
          case 'datasource':
            return './datasource.png'
          case 'view':
            try {
              let contentUrl = this.$props.itemObj.view.contentUrl.replace("sheets/", "")

              return `${urlBase}/${contentUrl}.png`
            }
            catch (e) {
              return ''
            }

          case 'project':
            return './project_icon.png'
          default:
            return ''
        }
      }
    },

    shadeHeight() {
      return this.$props.imgHeight - 120
    },
    isLikedDisliked() {
      try {
        let itemRatings = this.userStore.userContentRatings.find(e => e.item === this.$props.itemObj[this.$props.itemObj.type].id)

        if (itemRatings) {
          return itemRatings.rating
        } else {
          return -1
        }
      } catch (e) {

        return -1
      }

    },
    isFavorited() {
      try {
        let itemInFavorites = this.contentStore.formattedUserFavorites.find(e => e.luid === this.$props.itemObj[this.$props.itemObj.type].id)

        return itemInFavorites ? true : false
      }
      catch (e) {

        return false
      }
    }
  },
  methods: {
    async openContentInNewTab(itemLuid) {
      this.localOpenLoading = true
      await this.contentStore.vdsGetItemAndOpenInNewWindow(itemLuid)
      this.localOpenLoading = false
    },
    async addRemoveFavorite() {
      this.localFaveLoading = true

      let reqObj = {
        userLuid: this.userStore.selectedUser.userLuid,
        itemLuid: this.$props.itemObj[this.$props.itemObj.type].id,
        itemType: this.$props.itemObj.type,
        label: this.computedItemName
      }

      if (this.isFavorited) {
        await this.contentStore.removeFromUserFavorites(reqObj)
      } else {
        await this.contentStore.addToUserFavorites(reqObj)
      }

      this.localFaveLoading = false
    },
    openContentInTableau() {
      //
    },
    openContentInPreviewModal() {
      this.$emit('openContentPreviewModal', this.$props.itemObj)

    }

  },
  async mounted() {

    try {
      await this.contentStore.getContentDetails(this.$props.itemObj[this.$props.itemObj.type].id)

      if (this.$props.itemObj.type === 'workbook') {
        this.contentStore.getWorkbookPreviewImage(this.$props.itemObj[this.$props.itemObj.type].id)

      }


    } catch (e) {
      //
    }
  },
  watch: {
    itemObj: {
      async handler(newVal, oldVal) {

        await this.contentStore.getContentDetails(this.$props.itemObj[this.$props.itemObj.type].id)

        try {
          if (this.$props.itemObj.type === 'workbook') {
            this.contentStore.getWorkbookPreviewImage(this.$props.itemObj[this.$props.itemObj.type].id)

          }


        } catch (e) {
          //
        }
      },
      deep: true,

    }
  }
}
</script>

<style scope>
.container {
  width: 100%;
  position: relative;
  ;
}

.inner-card-height {
  height: 390px !important;
}

.no-preview-background {
  background-color: rgba(255, 255, 255, .6);
}

.blurred-image {
  filter: blur(1rem);
  overflow: hidden;
}
</style>
