export type CategoryTree = Record<string, CategoryNode>;

export interface CategoryNode {
  en?: string;
  de?: string;
  children?: CategoryTree;
}
