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
      @click="onClickTooltip(image)"
    >
      <l-icon
        :class-name="getClassName(image)"
        :icon-url="image.url"
        :iconSize="[64, 64]"
      ></l-icon>
    </l-marker>
    <v-dialog v-model="imageDialog" max-width="512">
      <v-card v-if="selectedImage">
        <v-card-title>{{ selectedImage.id }}</v-card-title>
        <v-card-text>
          <v-img :src="selectedImage.url"></v-img>
          <v-chip-group column>
            <v-chip v-for="tag in selectedImage.tags" :key="tag">
              {{ tag }}
            </v-chip>
          </v-chip-group>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" text @click="imageDialog = false"
            >Dismiss</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </l-map>
</template>

<style scoped>
.leaflet-container {
  height: 1024px;
  z-index: 0;
}
</style>
<style>
.my-image {
  border-style: solid;
  border-color: var(--v-primary-base);
}
</style>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import { LMap, LTileLayer, LMarker, LIcon } from "vue2-leaflet";
import { GeoImage } from "@/backend";

@Component({
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LIcon,
  },
})
export default class TerritoryMap extends Vue {
  images: GeoImage[] = [];
  imageDialog = false;
  selectedImage: GeoImage | null = null;

  created(): void {
    this.$http
      .get<GeoImage[]>("/geo/images")
      .then((response) => response.data)
      .then((images) => {
        this.images = images;
      });
  }

  getClassName(image: GeoImage): string {
    if (image.author === this.$store.state.username) {
      return "my-image";
    } else {
      return "";
    }
  }

  onClickTooltip(image: GeoImage): void {
    this.selectedImage = image;
    this.imageDialog = true;
  }
}
</script>
