const rules: Record<string, (value: string) => boolean | string> = {
  required: (value) => !!value || "Required.",
};

export default rules;
