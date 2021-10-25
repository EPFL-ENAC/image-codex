<template>
  <l-map :center="[46.8, 8.1]" :zoom="8">
    <l-tile-layer
      url="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}"
      attribution="Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ"
    ></l-tile-layer>
    <l-marker
      v-for="image in images"
      :key="image.id"
      :lat-lng="[image.latitude, image.longitude]"
    >
      <l-tooltip>
        <v-img :src="image.url" max-height="128" max-width="128"></v-img>
      </l-tooltip>
    </l-marker>
  </l-map>
</template>

<style scoped>
.leaflet-container {
  height: 1024px;
  z-index: 0;
}
</style>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import { LMap, LTileLayer, LMarker, LTooltip } from "vue2-leaflet";
import { GeoImage } from "@/backend";

@Component({
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LTooltip,
  },
})
export default class ImagesMap extends Vue {
  images: GeoImage[] = [];

  created(): void {
    this.$http
      .get<GeoImage[]>("/geo/images")
      .then((response) => response.data)
      .then((images) => {
        this.images = images;
      });
  }
}
</script>
