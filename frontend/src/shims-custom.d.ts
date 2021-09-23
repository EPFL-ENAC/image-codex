import { AxiosInstance } from "axios";

declare module "*.yaml" {
  const content: unknown;
  export default content;
}

declare module "piexifjs";

declare module "vue/types/vue" {
  interface Vue {
    $http: AxiosInstance;
  }
}
