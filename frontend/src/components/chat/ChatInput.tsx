import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/Button";
import { PaperPlaneRight, ArrowClockwise } from "@phosphor-icons/react";
import { useChatStore } from "@/stores/chatStore";
import { useChat } from "@/hooks/useChat";

interface ChatInputProps {
  onRetry?: () => void;
}

export function ChatInput({ onRetry }: ChatInputProps) {
  const [value, setValue] = useState<string>("");
  const inputRef = useRef<HTMLInputElement>(null);
  const isLoading = useChatStore((s) => s.isLoading);
  const systemReady = useChatStore((s) => s.systemReady);
  const isInitializing = useChatStore((s) => s.isInitializing);
  const initError = useChatStore((s) => s.initError);
  const pendingQuery = useChatStore((s) => s.pendingQuery);
  const setPendingQuery = useChatStore((s) => s.setPendingQuery);
  const { sendMessage } = useChat();

  useEffect(() => {
    if (pendingQuery) {
      setValue(pendingQuery);
      setPendingQuery("");
      inputRef.current?.focus();
    }
  }, [pendingQuery, setPendingQuery]);

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!value.trim() || isLoading) return;

    if (!systemReady) {
      if (onRetry) {
        onRetry();
      }
      return;
    }

    sendMessage(value);
    setValue("");
  }

  const placeholderText = isLoading
    ? "AI is analyzing your query…"
    : isInitializing
    ? "Connecting to backend server…"
    : initError
    ? "Backend offline — start FastAPI backend and click retry"
    : "Ask about IPOs (e.g. GMP, allotment), stock analysis (e.g. RELIANCE, TATA), or market trends…";

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-3 border-t border-border bg-primary px-4 py-3">
      <input
        ref={inputRef}
        id="chat-input"
        type="text"
        value={value}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setValue(e.target.value)}
        placeholder={placeholderText}
        disabled={isLoading || isInitializing}
        className="flex-1 rounded-lg border border-border bg-card px-4 py-2.5 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
        autoComplete="off"
      />
      {!systemReady && initError && onRetry ? (
        <Button
          type="button"
          variant="secondary"
          size="icon"
          onClick={onRetry}
          title="Retry connecting to backend"
          aria-label="Retry connection"
        >
          <ArrowClockwise size={20} weight="bold" />
        </Button>
      ) : (
        <Button
          type="submit"
          size="icon"
          disabled={!value.trim() || isLoading || !systemReady}
          aria-label="Send message"
        >
          <PaperPlaneRight size={20} weight="bold" />
        </Button>
      )}
    </form>
  );
}
