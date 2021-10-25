import piexif from "piexifjs";
import { tagSeparator } from "@/utils/contants";

export default class UploadImage {
  static readonly tagsAttributes: string[][] = [
    ["0th", piexif.ImageIFD.ImageDescription],
    ["Exif", piexif.ExifIFD.UserComment],
  ];
  static readonly authorAttribute: string[] = ["0th", piexif.ImageIFD.Artist];
  static readonly copyrightAttribute: string[] = [
    "0th",
    piexif.ImageIFD.Copyright,
  ];

  public oldAuthor: string | undefined;
  public newAuthor: string | undefined;
  public oldCopyright: string | undefined;
  public newCopyright: string | undefined;

  private exif: Record<string, Record<string, string | undefined>>;
  private oldTags: Set<string>;
  private newTags: Set<string>;

  constructor(
    public name: string,
    public type: string,
    public content: string
  ) {
    this.exif = content ? piexif.load(content) : {};
    this.oldTags = this.getTags();
    this.newTags = new Set(this.oldTags);
    this.oldAuthor = this.getAttributeValue(UploadImage.authorAttribute);
    this.newAuthor = this.oldAuthor;
    this.oldCopyright = this.getAttributeValue(UploadImage.copyrightAttribute);
    this.newCopyright = this.oldCopyright;
  }

  private getAttributeValue(key: string[]): string | undefined {
    const group = this.exif[key[0]];
    return group ? group[key[1]] : undefined;
  }

  private setAttributeValue(key: string[], value: string | undefined): void {
    this.exif[key[0]][key[1]] = value;
  }

  private getTags(): Set<string> {
    return new Set(
      UploadImage.tagsAttributes
        .map((attribute) => this.getAttributeValue(attribute))
        .filter((tags): tags is string => tags !== undefined)
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

  get authorChanged(): boolean {
    return this.oldAuthor !== this.newAuthor;
  }

  get copyrightChanged(): boolean {
    return this.oldCopyright !== this.newCopyright;
  }

  get isValid(): boolean {
    return this.newTags.size > 0 && !!this.newAuthor && !!this.newCopyright;
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

  public write(): string {
    this.setAttributeValue(UploadImage.authorAttribute, this.newAuthor);
    this.setAttributeValue(UploadImage.copyrightAttribute, this.newCopyright);
    const tags: string = Array.from(this.newTags).sort().join(tagSeparator);
    UploadImage.tagsAttributes.forEach((attribute) => {
      this.setAttributeValue(attribute, tags);
    });
    const bytes = piexif.dump(this.exif);
    return piexif.insert(bytes, this.content);
  }

  get metadata(): Record<string, Record<string, unknown>> {
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
