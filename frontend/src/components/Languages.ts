export const Languages = {
    ENGLISH: "ENGLISH",
    JAPANESE: "JAPANESE",
    MALAY: "MALAY",
    GERMAN: "GERMAN",
    FRENCH: "FRENCH",
    CHINESE: "CHINESE",
} as const
export type Languages = typeof Languages[keyof typeof Languages];