import qs from "qs";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types, @typescript-eslint/no-explicit-any
export function paramsSerializer(params: any): string {
  return qs.stringify(params, { arrayFormat: "repeat" });
}

export function unique<T>(value: T, index: number, array: T[]): boolean {
  return array.indexOf(value) === index;
}
