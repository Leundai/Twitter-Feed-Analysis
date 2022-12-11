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

// TODO: Change author_ids to camelCase
export interface EmotionContributor {
  author_ids: Array<number>;
  occurance: number;
}

export interface EmotionContributors {
  anger: EmotionContributor;
  disgust: EmotionContributor;
  fear: EmotionContributor;
  joy: EmotionContributor;
  neutral: EmotionContributor;
  sadness: EmotionContributor;
  surprise: EmotionContributor;
}
