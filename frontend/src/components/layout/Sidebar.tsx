import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { useChatStore } from "@/stores/chatStore";
import { Trash, Lightbulb, Info, ChartBar, TrendUp, MagnifyingGlass, RocketLaunch, ArrowClockwise } from "@phosphor-icons/react";

interface SidebarProps {
  onInitialize?: () => void;
}

export function Sidebar({ onInitialize }: SidebarProps) {
  const clearMessages = useChatStore((s) => s.clearMessages);
  const sampleQueries = useChatStore((s) => s.sampleQueries);
  const setPendingQuery = useChatStore((s) => s.setPendingQuery);
  const systemReady = useChatStore((s) => s.systemReady);
  const isInitializing = useChatStore((s) => s.isInitializing);

  return (
    <aside className="flex w-72 shrink-0 flex-col border-r border-border bg-primary">
      <div className="border-b border-border p-4">
        <div className="flex items-center gap-2 text-sm font-medium text-foreground">
          <Info size={18} weight="bold" /> System Information
        </div>
        <div className="mt-3 space-y-2 text-xs text-muted-foreground">
          <div className="flex items-center gap-2">
            <span className={`h-2 w-2 rounded-full ${systemReady ? "bg-accent" : "bg-destructive"}`} />
            {systemReady ? "System Active" : isInitializing ? "Initializing..." : "Not Initialized"}
          </div>
          <div className="flex items-center gap-2"><ChartBar size={14} /> IPO Advisor Agent</div>
          <div className="flex items-center gap-2"><TrendUp size={14} /> Stock Advisor Agent</div>
          <div className="flex items-center gap-2"><MagnifyingGlass size={14} /> Tavily Web Search</div>
        </div>
        {onInitialize && (
          <div className="mt-3 pt-3 border-t border-border/50">
            <Button
              variant={systemReady ? "secondary" : "primary"}
              size="sm"
              onClick={onInitialize}
              disabled={isInitializing}
              className="w-full text-xs flex items-center justify-center gap-1.5 h-8 font-medium cursor-pointer"
            >
              {isInitializing ? (
                <>
                  <Spinner size="sm" /> Initializing...
                </>
              ) : systemReady ? (
                <>
                  <ArrowClockwise size={14} weight="bold" /> Re-initialize System
                </>
              ) : (
                <>
                  <RocketLaunch size={14} weight="bold" /> Initialize System
                </>
              )}
            </Button>
          </div>
        )}
      </div>
      <div className="flex-1 overflow-y-auto p-4">
        <div className="flex items-center gap-2 text-sm font-medium text-foreground">
          <Lightbulb size={18} weight="bold" /> Sample Queries
        </div>
        <div className="mt-3 space-y-2">
          {sampleQueries.map((q, i) => (
            <button key={i} onClick={() => setPendingQuery(q)} disabled={!systemReady}
              className="w-full cursor-pointer rounded-lg border border-border bg-card px-3 py-2 text-left text-xs text-muted-foreground transition-colors duration-200 hover:border-accent/40 hover:text-foreground disabled:cursor-not-allowed disabled:opacity-50">
              {q}
            </button>
          ))}
        </div>
      </div>
      <div className="border-t border-border p-4">
        <Button variant="ghost" size="sm" onClick={clearMessages} className="w-full">
          <Trash size={16} /> Clear Chat
        </Button>
      </div>
    </aside>
  );
}
