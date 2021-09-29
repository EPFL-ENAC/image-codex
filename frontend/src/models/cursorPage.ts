export default interface CursorPage<T> {
  items: T[];
  total: number;
  next: string;
  size: number;
}
