import {
  CompositionsApi,
  GeoApi,
  HashApi,
  ImagesApi,
  TagsApi,
} from "./backend";

declare module "vue/types/vue" {
  interface Vue {
    $compositionsApi: CompositionsApi;
    $geoApi: GeoApi;
    $hashApi: HashApi;
    $imagesApi: ImagesApi;
    $tagsApi: TagsApi;
  }
}
