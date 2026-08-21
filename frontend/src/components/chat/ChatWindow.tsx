import { useEffect, useRef } from "react";
import { useChatStore } from "@/stores/chatStore";
import { MessageBubble } from "@/components/chat/MessageBubble";
import { TypingIndicator } from "@/components/chat/TypingIndicator";
import { Pulse, Sparkle, ChartBar, TrendUp, MagnifyingGlass } from "@phosphor-icons/react";

const STARTER_PROMPTS = [
  {
    icon: ChartBar,
    title: "IPO Analysis & GMP",
    query: "What are the current IPO opportunities in India and their GMP?",
  },
  {
    icon: TrendUp,
    title: "Stock Research",
    query: "Analyze RELIANCE stock for investment with fundamentals and technicals",
  },
  {
    icon: MagnifyingGlass,
    title: "Market Trends",
    query: "What are today's top Indian stock market trends and sector performance?",
  },
];

export function ChatWindow() {
  const messages = useChatStore((s) => s.messages);
  const isLoading = useChatStore((s) => s.isLoading);
  const setPendingQuery = useChatStore((s) => s.setPendingQuery);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center p-6 text-center">
        <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-secondary border border-border shadow-lg mb-4">
          <Pulse size={32} weight="bold" className="text-accent" />
        </div>
        <h2 className="text-xl md:text-2xl font-bold tracking-tight text-foreground">
          AI Financial Advisor
        </h2>
        <p className="mt-2 max-w-md text-sm text-muted-foreground leading-relaxed">
          Intelligent real-time insights for Indian capital markets (NSE/BSE). Powered by specialized IPO and Stock analysis multi-agent routing.
        </p>

        <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-3 w-full max-w-2xl text-left">
          {STARTER_PROMPTS.map((prompt, idx) => (
            <button
              key={idx}
              onClick={() => setPendingQuery(prompt.query)}
              className="flex flex-col justify-between p-4 rounded-xl border border-border bg-card hover:border-accent/40 hover:bg-secondary/60 transition-all duration-200 group cursor-pointer"
            >
              <div className="flex items-center gap-2 text-xs font-semibold text-accent mb-2">
                <prompt.icon size={16} weight="bold" />
                {prompt.title}
              </div>
              <p className="text-xs text-muted-foreground group-hover:text-foreground line-clamp-2">
                {prompt.query}
              </p>
              <div className="flex items-center gap-1 text-[11px] text-muted-foreground group-hover:text-accent mt-3">
                <Sparkle size={12} />
                Try this query
              </div>
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 min-h-0 overflow-y-auto px-2 md:px-4">
      <div className="mx-auto max-w-3xl py-4 space-y-1">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        {isLoading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
