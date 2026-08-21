import { create } from "zustand";
import type { Message } from "@/types/chat";

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  systemReady: boolean;
  isInitializing: boolean;
  initError: string | null;
  sampleQueries: string[];
  pendingQuery: string;

  // Actions
  addMessage: (message: Message) => void;
  clearMessages: () => void;
  setLoading: (loading: boolean) => void;
  setSystemReady: (ready: boolean) => void;
  setIsInitializing: (isInitializing: boolean) => void;
  setInitError: (error: string | null) => void;
  setSampleQueries: (queries: string[]) => void;
  setPendingQuery: (query: string) => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isLoading: false,
  systemReady: false,
  isInitializing: true,
  initError: null,
  sampleQueries: [],
  pendingQuery: "",

  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),

  clearMessages: () => set({ messages: [] }),

  setLoading: (loading) => set({ isLoading: loading }),

  setSystemReady: (ready) => set({ systemReady: ready }),

  setIsInitializing: (isInitializing) => set({ isInitializing }),

  setInitError: (error) => set({ initError: error }),

  setSampleQueries: (queries) => set({ sampleQueries: queries }),

  setPendingQuery: (query) => set({ pendingQuery: query }),
}));
