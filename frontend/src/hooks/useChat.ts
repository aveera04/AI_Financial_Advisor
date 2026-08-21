import { useCallback } from "react";
import { api } from "@/services/api";
import { useChatStore } from "@/stores/chatStore";
import { RateLimitError, ApiServiceError } from "@/services/api";
import type { Message } from "@/types/chat";

export function useChat() {
  const addMessage = useChatStore((s) => s.addMessage);
  const setLoading = useChatStore((s) => s.setLoading);
  const isLoading = useChatStore((s) => s.isLoading);

  const sendMessage = useCallback(
    async (query: string) => {
      if (!query.trim() || isLoading) return;

      const userMessage: Message = {
        id: crypto.randomUUID(),
        role: "user",
        content: query.trim(),
        timestamp: new Date(),
      };
      addMessage(userMessage);
      setLoading(true);

      try {
        const result = await api.chat(query.trim());
        const assistantMessage: Message = {
          id: crypto.randomUUID(),
          role: "assistant",
          content: result.response,
          timestamp: new Date(),
          agentInfo: {
            agent_used: result.agent_used,
            route_info: result.route_info,
            processing_time: result.processing_time,
          },
        };
        addMessage(assistantMessage);
      } catch (error) {
        let errorContent: string;
        if (error instanceof RateLimitError) {
          errorContent = `**Rate Limit Reached**\n\nThe AI service is temporarily unavailable. Please wait ${error.retryAfter} and try again.`;
        } else if (error instanceof ApiServiceError) {
          errorContent = `**Error**\n\n${error.message}`;
        } else {
          errorContent = "**Unexpected Error**\n\nSomething went wrong. Please try again.";
        }
        addMessage({
          id: crypto.randomUUID(),
          role: "assistant",
          content: errorContent,
          timestamp: new Date(),
        });
      } finally {
        setLoading(false);
      }
    },
    [addMessage, setLoading, isLoading]
  );

  return { sendMessage };
}
