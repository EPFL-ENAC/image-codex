import piexif from "piexifjs";

export default class Image {
  static readonly attributes: string[][] = [
    ["0th", piexif.ImageIFD.ImageDescription],
    ["Exif", piexif.ExifIFD.UserComment],
  ];

  public name: string | undefined;
  public type: string | undefined;
  private exif: Record<string, Record<string, string>>;
  private oldTags: Set<string>;
  private newTags: Set<string>;

  constructor(file?: File, public content?: string) {
    this.name = file?.name;
    this.type = file?.type;
    this.exif = content ? piexif.load(content) : {};
    this.oldTags = Image.getTags(this.exif);
    this.newTags = new Set(this.oldTags);
  }

  static getTags(exif: Record<string, Record<string, string>>): Set<string> {
    return new Set(
      Image.attributes
        .flatMap((attribute) => {
          const group = exif[attribute[0]];
          return group ? [group[attribute[1]]] : [];
        })
        .filter((tags) => tags !== undefined)
        .map((tags) => tags.replace(/ASCII|[^\x20-\x7E]/g, ""))
        .flatMap((tags) => tags.split(","))
        .map((tag) => tag.trim())
        .filter((tag) => tag.length > 0)
        .map((tag) => tag.toLowerCase())
    );
  }

  get removedTags(): string[] {
    return Array.from(
      new Set([...this.oldTags].filter((t) => !this.newTags.has(t)))
    ).sort();
  }

  get unmodifiedTags(): string[] {
    return Array.from(
      new Set([...this.oldTags].filter((t) => this.newTags.has(t)))
    ).sort();
  }

  get addedTags(): string[] {
    return Array.from(
      new Set([...this.newTags].filter((t) => !this.oldTags.has(t)))
    ).sort();
  }

  public addTag(tag: string): void {
    this.newTags.add(tag);
  }

  public addTags(tags: string[]): void {
    tags.forEach((tag) => this.addTag(tag));
  }

  public removeTag(tag: string): void {
    this.newTags.delete(tag);
  }

  public tag(separator: string): string {
    const tags: string = Array.from(this.newTags).sort().join(separator);
    Image.attributes.forEach((attribute) => {
      this.exif[attribute[0]][attribute[1]] = tags;
    });
    const bytes = piexif.dump(this.exif);
    return piexif.insert(bytes, this.content);
  }

  private getExifObject(): Record<string, Record<string, unknown>> {
    const result: Record<string, Record<string, unknown>> = {};
    for (const ifd in this.exif) {
      if (ifd !== "thumbnail") {
        const tags: Record<string, unknown> = {};
        for (const tag in this.exif[ifd]) {
          tags[piexif.TAGS[ifd][tag]["name"]] = this.exif[ifd][tag];
        }
        result[ifd] = tags;
      }
    }
    return result;
  }
}
