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
    <template #selection="data">
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

<script lang="ts">
import categories from "@/assets/categories.yaml";
import { CategoryNode, CategoryTree } from "@/models/category-tree";
import { tagSeparator } from "@/utils/contants";
import { unique } from "@/utils/functions";
import { Component, Prop, Vue, Watch } from "vue-property-decorator";

type Category = ComboboxItem | string;

@Component
export default class TagSelector extends Vue {
  @Prop({ type: Array as () => string[], default: () => [] })
  readonly value!: string[];

  selectedCategories: Category[] = [];
  backendTags: string[] = [];

  created(): void {
    this.onValueChanged();
    this.$tagsApi
      .getTagsTagsGet()
      .then((response) => response.data)
      .then((tags) => {
        this.backendTags = tags;
      });
  }

  get categoryComboboxItems(): ComboboxItem[] {
    const items = this.getComboboxItems(categories as CategoryTree);
    const tags = new Set(
      items
        .map((item) => item.value)
        .flatMap((tags) => tags.split(tagSeparator))
    );
    const freeTags: ComboboxItem[] = this.backendTags
      .filter((tag) => !tags.has(tag))
      .map((tag) => {
        return {
          text: tag,
          value: tag,
        };
      });
    return items.concat(freeTags);
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

  onValueChanged(): void {
    const tags = this.value;
    const inputTags = new Set(tags);
    const comboboxItems = this.categoryComboboxItems.filter((item) =>
      item.value.split(tagSeparator).every((tag) => inputTags.has(tag))
    );
    const itemValues = comboboxItems.map((item) => item.value);
    // keep only children
    this.selectedCategories = comboboxItems.filter(
      (item) =>
        !itemValues
          .filter((value) => value !== item.value)
          .some((value) => value.startsWith(item.value))
    );
    const addedTags = new Set(this.selectedTags);
    this.selectedCategories.push(...tags.filter((tag) => !addedTags.has(tag)));
  }

  onChange(): void {
    this.selectedCategories = this.selectedCategories
      .map((category) => {
        if (typeof category == "string") {
          return category.toLowerCase().replaceAll(",", "").trim();
        } else {
          return category;
        }
      })
      .filter((category) => category);
    const tags = this.selectedTags;
    this.$emit("input", tags);
    this.$emit("change", tags);
  }

  getText(category: Category): string {
    return this.getString(category, (c) => c.text);
  }

  getValue(category: Category): string {
    return this.getString(category, (c) => c.value);
  }

  private getString(
    category: Category,
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

<style scoped>
.overflow {
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
