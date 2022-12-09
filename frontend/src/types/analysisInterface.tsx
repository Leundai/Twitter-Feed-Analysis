export interface EmotionCount {
  fear: number;
  joy: number;
  surprise: number;
  anger: number;
  disgust: number;
  sadness: number;
  neutral: number;
}

export type EmotionKey = keyof EmotionCount;
