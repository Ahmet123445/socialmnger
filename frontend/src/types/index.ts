export interface User {
  id: string;
  email: string;
  username: string;
  full_name?: string;
  avatar_url?: string;
  is_active: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface ContentItem {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  media_asset_id?: string;
  platforms?: string[];
  status: string;
  scheduled_at?: string;
  published_at?: string;
  general_caption?: string;
  general_hashtags?: string;
  platform_captions?: Record<string, string>;
  platform_hashtags?: Record<string, string>;
  ai_generated?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface PlatformPost {
  id: string;
  content_item_id: string;
  platform: string;
  platform_post_id?: string;
  caption?: string;
  hashtags?: string;
  status: string;
  error_message?: string;
  post_url?: string;
  published_at?: string;
  created_at: string;
}

export interface PublishJob {
  id: string;
  content_item_id: string;
  platform: string;
  status: string;
  attempts: number;
  error_message?: string;
  result?: Record<string, any>;
  started_at?: string;
  completed_at?: string;
  created_at: string;
}

export interface MediaAsset {
  id: string;
  filename: string;
  original_filename?: string;
  file_size?: number;
  mime_type?: string;
  duration_seconds?: number;
  thumbnail_path?: string;
  storage_type: string;
  created_at: string;
}

export interface AnalyticsSnapshot {
  id: string;
  platform_post_id: string;
  platform: string;
  views: number;
  likes: number;
  comments: number;
  shares: number;
  saves: number;
  follower_count?: number;
  engagement_rate?: number;
  performance_score?: number;
  snapshot_date: string;
}

export interface AnalyticsSummary {
  total_views: number;
  total_likes: number;
  total_comments: number;
  total_shares: number;
  avg_engagement_rate: number;
  content_count: number;
  platform_breakdown: Record<string, { views: number; likes: number }>;
}

export interface AISetting {
  id: string;
  provider: string;
  base_url: string;
  model_name: string;
  temperature: number;
  max_tokens: number;
  is_active: string;
}

export interface AIGenerateResponse {
  platform: string;
  caption?: string;
  hashtags?: string;
  suggestions?: string[];
}

export interface AIRecommendation {
  id: string;
  recommendation_type: string;
  platform?: string;
  title?: string;
  recommendation: string;
  confidence_score?: number;
  is_applied: string;
  created_at: string;
}

export interface DashboardSummary {
  today_content_count: number;
  week_content_count: number;
  scheduled_count: number;
  published_count: number;
  failed_count: number;
  total_views: number;
  total_likes: number;
  total_engagement_rate: number;
  platform_stats: Record<string, any>;
  recent_content: Array<{
    id: string;
    title: string;
    status: string;
    platforms: string[];
    created_at: string;
  }>;
  top_performing?: Record<string, any>;
  alerts: Array<{
    type: string;
    message: string;
  }>;
}

export interface PlatformAccount {
  id: string;
  platform: string;
  platform_username?: string;
  platform_user_id?: string;
  status: string;
  created_at: string;
}

export interface SystemSetting {
  id: string;
  key: string;
  value?: string;
  description?: string;
  updated_at: string;
}
