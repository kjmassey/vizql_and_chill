<template>


  <div class="container" @mouseenter="showFooter = true" @mouseleave="showFooter = false" style="aspect-ratio: 1;">
    <div class="inner">
      <v-img :height="$props.imgHeight" :src="$props.imgUrl" lazy-src="../../public/chart-lazy-load.png"
        :class="$props.userHasAccess ? 'preview-image' : 'blurred preview-image'" rounded="lg" cover />

    </div>
    <div class="overlay" v-if="!$props.userHasAccess">
      <div v-show="!showFooter">

        <v-btn color="red" block size="x-large" elevation="4">
          <template v-slot:default>
            <div class="lock-button-container">

              <v-icon size="x-large">mdi-lock</v-icon>

            </div>
          </template>
        </v-btn>

      </div>

    </div>
    <div class="content-type-pill-container ml-6">
      <div class="text-subtitle-2 content-type-pill">
        <div :class="pillClass">{{ $props.contentType.toUpperCase() }}</div>
      </div>
    </div>

    <div class="footer-slide-in w-100 h-100" v-show="showFooter">

      <v-scale-transition>
        <v-tooltip text="Click to Request Access" location="top">
          <template v-slot:activator="{ props }">
            <div class="overlay-lock-icon" v-if="!$props.userHasAccess" v-bind="props">
              <v-btn color="red" block size="small" elevation="4">
                <template v-slot:default>
                  <div class="lock-button-container">

                    <v-icon size="x-large">mdi-lock</v-icon>

                  </div>
                </template>
              </v-btn>
            </div>
          </template>
        </v-tooltip>
      </v-scale-transition>

      <v-scale-transition>



        <v-card-text v-show="showFooter">
          <div class="footer-icons">
            <div class="text-h4 w-100 pb-6">{{ $props.contentName }}</div>

            <div class="d-flex start align-center w-100">
              <v-icon size="x-large">mdi-account-circle</v-icon>
              <div class="pl-2">{{ $props.ownerName }}</div>
            </div>

            <v-tooltip :text="$props.contentUrl" location="top">
              <template v-slot:activator="{ props }">
                <div class="d-flex align-center w-100" v-bind="props" style="cursor: pointer;"
                  @click="openContentInNewTab($props.contentUrl)">
                  <v-icon v-bind="props" link size="x-large">mdi-open-in-new</v-icon>
                  <div class="pl-2" v-bind="props">

                    {{ `...${$props.contentUrl.slice(-25)}` }}

                  </div>

                </div>
              </template>
            </v-tooltip>

            <div class="d-flex start align-center w-100">
              <v-icon size="x-large">mdi-eye</v-icon>
              <div class="pl-2">{{ $props.viewCount }}</div>
            </div>



            <div class="d-flex start align-center w-100" style="cursor: pointer;"
              @click="$emit('openEmbeddedContentViewer', this.$props.contentUrl)"
              v-if="$props.contentType == 'view' && this.$props.userHasAccess">
              <v-icon size="x-large">mdi-open-in-app</v-icon>
              <div class="pl-2">Open Here</div>
            </div>

          </div>
        </v-card-text>
      </v-scale-transition>
    </div>
  </div>


</template>

<script>
export default {
  name: 'ContentPreview',
  data: () => ({
    showLockText: false,
    showFooter: false,
    showTooltip: false
  }),
  props: {
    userHasAccess: { type: Boolean, default: false },
    contentUrl: { type: String, default: '' },
    contentType: { type: String, default: 'workbook' },
    imgUrl: { type: String, default: '' },
    ownerName: { type: String, default: 'Owner' },
    viewCount: { type: String, default: '12345' },
    imgHeight: { type: String, default: '800' },
    contentName: { type: String, default: 'This is some content...' },

  },
  components: {

  },
  computed: {
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
    }
  },
  methods: {
    openContentInNewTab(url) {
      window.open(url, '_blank')
    },

  },
  mounted() {

  },
}
</script>

<style scoped>
.container {
  width: 100%;
  position: relative;
}

.inner {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden
}

.overlay {
  position: absolute;
  z-index: 50;
  top: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.blurred {
  filter: blur(8px);
  overflow: hidden;
  z-index: 10;
}

.lock-button-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.footer-slide-in {
  display: flex;
  justify-content: center;
  position: absolute;
  top: 0;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 99;

}

.footer-icons {
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  width: 100%;
  z-index: 52;
  height: 100%;
}

.content-type-pill-container {
  position: absolute;
  top: 8px;
  right: 4px;
  z-index: 53;
}

.content-type-pill {
  padding: 4px;
  border-radius: 8px;
}

.workbook-pill {
  padding: 4px 8px;
  background-color: rgb(var(--v-theme-success));
  border-radius: 5px;

}

.datasource-pill {
  padding: 4px 8px;
  background-color: rgb(var(--v-theme-error));
  border-radius: 5px;

}

.view-pill {
  padding: 4px 8px;
  background-color: rgb(var(--v-theme-warning));
  border-radius: 5px;

}

.overlay-lock-icon {
  margin-right: 12px;
  margin-bottom: 24px;
  position: absolute;
  bottom: 0;
  right: 0;
  z-index: 51;
}
</style>
