// Mirrors backend SUPPORTED_LANGUAGES (app/services/language_detection/
// language_mapper.py). Grouped for the <optgroup> dropdowns. Keep in sync.

export const LANGUAGE_GROUPS = [
  {
    label: "Indian languages",
    languages: [
      "hindi",
      "bengali",
      "tamil",
      "telugu",
      "marathi",
      "gujarati",
      "punjabi",
      "kannada",
      "malayalam",
      "urdu",
      "odia",
      "assamese",
      "nepali",
      "sanskrit",
      "konkani",
      "sindhi",
      "kashmiri",
      "manipuri",
      "santali",
    ],
  },
  {
    label: "Regional dialects (low-resource)",
    languages: [
      "bhojpuri",
      "awadhi",
      "maithili",
      "magahi",
      "chhattisgarhi",
    ],
  },
  {
    label: "Global languages",
    languages: [
      "english",
      "french",
      "spanish",
      "german",
      "arabic",
      "chinese",
      "russian",
    ],
  },
];

export function titleCase(value) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}
