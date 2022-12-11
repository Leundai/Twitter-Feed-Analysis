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
export interface EmotionContributors {
  [authorId: string]: number;
}

export interface EmotionsContributors {
  anger: EmotionContributors;
  disgust: EmotionContributors;
  fear: EmotionContributors;
  joy: EmotionContributors;
  neutral: EmotionContributors;
  sadness: EmotionContributors;
  surprise: EmotionContributors;
}

export interface ClassifiedTweet {
  anger: number;
  author_id: string;
  content: string;
  created_at: string;
  disgust: number;
  fear: number;
  joy: number;
  max_emotion: string;
  neutral: number;
  sadness: number;
  surprise: number;
  tweet_id: string;
}

export type ClassifiedTweets = Array<ClassifiedTweet>;

export interface AuthorsInfo {
  [authorId: string]: {
    name: string;
    username: string;
  };
}
