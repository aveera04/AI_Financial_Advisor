export interface Source {
  id: string;
  title: string;
  url: string;
  hostname: string;
  reason: string;
  quality: 'high' | 'medium' | 'low';
  isUserUpload?: boolean;
  filename?: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: Source[];
  model?: string;
  isRegulatory?: boolean;
  requiresConfirmation?: boolean;
  confirmed?: boolean;
}

export interface Chat {
  id: string;
  title: string;
  lastMessage: string;
  timestamp: Date;
  messages: ChatMessage[];
}

export interface SessionSettings {
  tone: 'concise' | 'detailed';
  currency: string;
  riskProfile: 'conservative' | 'moderate' | 'aggressive';
  storageMode: 'local' | 'cloud';
  privacyOptIn: boolean;
  highContrastMode: boolean;
}

export interface AuditLogEntry {
  id: string;
  timestamp: Date;
  messageId: string;
  sourcesFetched: string[];
  modelUsed: string;
}
