import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Chat, ChatMessage, SessionSettings, AuditLogEntry } from '@/types/chat';

interface ChatState {
  chats: Chat[];
  currentChatId: string | null;
  sessionSettings: SessionSettings;
  sessionStartTime: Date | null;
  auditLog: AuditLogEntry[];
  isInitialized: boolean;
  
  // Actions
  initializeSession: () => void;
  createNewChat: () => string;
  loadChat: (chatId: string) => void;
  clearCurrentChat: () => void;
  deleteChat: (chatId: string) => void;
  renameChat: (chatId: string, newTitle: string) => void;
  addMessage: (message: Omit<ChatMessage, 'id' | 'timestamp'>) => void;
  updateSettings: (settings: Partial<SessionSettings>) => void;
  confirmRegulatoryAction: (messageId: string) => void;
  addAuditEntry: (entry: Omit<AuditLogEntry, 'id' | 'timestamp'>) => void;
  getCurrentChat: () => Chat | undefined;
}

const generateId = () => Math.random().toString(36).substring(2, 15);

const defaultSettings: SessionSettings = {
  tone: 'concise',
  currency: 'USD',
  riskProfile: 'moderate',
  storageMode: 'local',
  privacyOptIn: false,
  highContrastMode: false,
};

export const useChatStore = create<ChatState>()(
  persist(
    (set, get) => ({
      chats: [],
      currentChatId: null,
      sessionSettings: defaultSettings,
      sessionStartTime: null,
      auditLog: [],
      isInitialized: false,

      initializeSession: () => {
        const chatId = get().createNewChat();
        set({
          isInitialized: true,
          sessionStartTime: new Date(),
          currentChatId: chatId,
        });
      },

      createNewChat: () => {
        const newChat: Chat = {
          id: generateId(),
          title: 'New Conversation',
          lastMessage: '',
          timestamp: new Date(),
          messages: [],
        };
        set((state) => ({
          chats: [newChat, ...state.chats],
          currentChatId: newChat.id,
        }));
        return newChat.id;
      },

      loadChat: (chatId) => {
        set({ currentChatId: chatId });
      },

      clearCurrentChat: () => {
        const { currentChatId } = get();
        if (!currentChatId) return;
        
        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === currentChatId
              ? { ...chat, messages: [], lastMessage: '', title: 'New Conversation' }
              : chat
          ),
        }));
      },

      deleteChat: (chatId) => {
        set((state) => {
          const newChats = state.chats.filter((chat) => chat.id !== chatId);
          const newCurrentChatId =
            state.currentChatId === chatId
              ? newChats[0]?.id || null
              : state.currentChatId;
          return { chats: newChats, currentChatId: newCurrentChatId };
        });
      },

      renameChat: (chatId, newTitle) => {
        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === chatId ? { ...chat, title: newTitle } : chat
          ),
        }));
      },

      addMessage: (message) => {
        const { currentChatId } = get();
        if (!currentChatId) return;

        const newMessage: ChatMessage = {
          ...message,
          id: generateId(),
          timestamp: new Date(),
        };

        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === currentChatId
              ? {
                  ...chat,
                  messages: [...chat.messages, newMessage],
                  lastMessage: message.content.substring(0, 50),
                  timestamp: new Date(),
                  title: chat.messages.length === 0 ? message.content.substring(0, 30) : chat.title,
                }
              : chat
          ),
        }));
      },

      updateSettings: (settings) => {
        set((state) => ({
          sessionSettings: { ...state.sessionSettings, ...settings },
        }));
      },

      confirmRegulatoryAction: (messageId) => {
        const { currentChatId } = get();
        if (!currentChatId) return;

        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === currentChatId
              ? {
                  ...chat,
                  messages: chat.messages.map((msg) =>
                    msg.id === messageId ? { ...msg, confirmed: true } : msg
                  ),
                }
              : chat
          ),
        }));
      },

      addAuditEntry: (entry) => {
        const newEntry: AuditLogEntry = {
          ...entry,
          id: generateId(),
          timestamp: new Date(),
        };
        set((state) => ({
          auditLog: [...state.auditLog, newEntry],
        }));
      },

      getCurrentChat: () => {
        const { chats, currentChatId } = get();
        return chats.find((chat) => chat.id === currentChatId);
      },
    }),
    {
      name: 'financial-advisor-storage',
      partialize: (state) =>
        state.sessionSettings.privacyOptIn
          ? state
          : { ...state, chats: [], auditLog: [] },
    }
  )
);
