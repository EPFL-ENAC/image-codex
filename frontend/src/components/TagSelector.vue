<template>
  <v-combobox
    v-model="selectedCategories"
    :items="categoryComboboxItems"
    label="Categories"
    :messages="messages"
    clearable
    multiple
    @change="onChange"
  >
    <template v-slot:selection="data">
      <v-chip
        :key="getValue(data.item)"
        v-bind="data.attrs"
        :input-value="data.selected"
        :disabled="data.disabled"
        close
        @click:close="data.parent.selectItem(data.item)"
      >
        <span class="overflow" :title="getText(data.item)">
          {{ getText(data.item) }}
        </span>
      </v-chip>
    </template>
  </v-combobox>
</template>

<style scoped>
.overflow {
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>

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
      .map(this.getValue)
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

  getText(category: ComboboxItem | string): string {
    return this.getString(category, (c) => c.text);
  }

  getValue(category: ComboboxItem | string): string {
    return this.getString(category, (c) => c.value);
  }

  private getString(
    category: ComboboxItem | string,
    getter: (item: ComboboxItem) => string
  ): string {
    if (typeof category === "string") {
      return category;
    } else {
      return getter(category);
    }
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
