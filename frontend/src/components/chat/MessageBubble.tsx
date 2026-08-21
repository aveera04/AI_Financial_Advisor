import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { AgentBadge } from "@/components/chat/AgentBadge";
import { User, Robot, Clock } from "@phosphor-icons/react";
import { cn } from "@/lib/utils";
import type { Message } from "@/types/chat";

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const timeStr = new Date(message.timestamp).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div className={cn("flex gap-3 px-3 md:px-4 py-3.5", isUser && "flex-row-reverse")}>
      <div
        className={cn(
          "flex h-8 w-8 shrink-0 items-center justify-center rounded-full border shadow-sm",
          isUser
            ? "bg-accent/20 border-accent/40 text-accent"
            : "bg-secondary border-border text-accent"
        )}
      >
        {isUser ? <User size={18} weight="bold" /> : <Robot size={18} weight="bold" />}
      </div>

      <div className={cn("max-w-[88%] md:max-w-[82%] space-y-1.5", isUser ? "items-end text-right" : "items-start")}>
        <div className={cn("flex items-center gap-2 text-[11px] text-muted-foreground px-1", isUser && "justify-end")}>
          <span className="font-semibold text-foreground/80">{isUser ? "You" : "AI Advisor"}</span>
          <span>•</span>
          <span>{timeStr}</span>
        </div>

        <div
          className={cn(
            "rounded-xl px-4 py-3 text-sm leading-relaxed text-left shadow-sm",
            isUser
              ? "bg-secondary/90 border border-accent/30 text-foreground inline-block shadow-md"
              : "bg-card border border-border text-card-foreground"
          )}
        >
          {isUser ? (
            <p className="whitespace-pre-wrap break-words font-normal text-foreground">{message.content}</p>
          ) : (
            <div className="prose prose-invert prose-sm max-w-none break-words overflow-x-auto">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>

        {!isUser && message.agentInfo && (
          <div className="flex items-center gap-2 px-1 pt-1">
            <AgentBadge agentUsed={message.agentInfo.agent_used} />
            <span className="flex items-center gap-1 text-[11px] text-muted-foreground">
              <Clock size={12} />
              {message.agentInfo.processing_time}s
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
