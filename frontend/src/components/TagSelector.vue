<template>
  <v-combobox
    v-model="selectedCategories"
    :items="categoryComboboxItems"
    label="Categories"
    :messages="messages"
    chips
    deletable-chips
    multiple
    @change="onChange"
  ></v-combobox>
</template>

<script lang="ts">
import { Vue, Component, Watch } from "vue-property-decorator";
import categories from "@/assets/categories.yaml";
import { CategoryNode, CategoryTree } from "@/models/category-tree";
import { tagSeparator } from "@/utils/contants";
import { unique } from "@/utils/functions";

@Component
export default class TagSelector extends Vue {
  value: string[] = [];
  selectedCategories: (ComboboxItem | string)[] = [];

  get categoryComboboxItems(): ComboboxItem[] {
    return this.getComboboxItems(categories as CategoryTree);
  }

  get selectedTags(): string[] {
    return this.selectedCategories
      .map((category) => {
        if (typeof category === "string") {
          return category;
        } else {
          return category.value;
        }
      })
      .flatMap((categories) => categories.split(tagSeparator))
      .filter(unique)
      .sort();
  }

  get messages(): string {
    return (
      `Actual tags (${this.selectedTags.length}): ` +
      this.selectedTags.join(", ")
    );
  }

  @Watch("$i18n.locale")
  onLocaleChanged(): void {
    this.selectedCategories = this.selectedCategories.map((category) => {
      if (typeof category === "string") {
        return category;
      } else {
        return (
          this.categoryComboboxItems.find(
            (item) => item.value === category.value
          ) ?? category
        );
      }
    });
  }

  onChange(): void {
    this.$emit("input", this.selectedTags);
    this.$emit("change");
  }

  private getTreeItems(
    tree: CategoryTree,
    parents: string[] = []
  ): TreeviewItem[] {
    const locale = this.$i18n.locale as keyof CategoryNode;
    return Object.entries(tree).map(([key, value]) => {
      const id = [...parents, key];
      return {
        id: id.join(tagSeparator),
        name: (value[locale] as string) ?? key,
        children: value.children ? this.getTreeItems(value.children, id) : [],
      };
    });
  }

  private getComboboxItems(
    tree: CategoryTree,
    parents: [string, string][] = []
  ): ComboboxItem[] {
    const locale = this.$i18n.locale as keyof CategoryNode;
    return Object.entries(tree).flatMap(([key, value]) => {
      const text = (value[locale] as string) ?? key;
      const current: [string, string][] = [...parents, [key, text]];
      return [
        {
          value: current.map((item) => item[0]).join(tagSeparator),
          text: current.map((item) => item[1]).join(" / "),
        },
      ].concat(
        value.children ? this.getComboboxItems(value.children, current) : []
      );
    });
  }
}

interface TreeviewItem {
  id: string;
  name: string;
  children?: TreeviewItem[];
}

interface ComboboxItem {
  text: string;
  value: string;
}
</script>
