import { Badge } from "@/components/ui/Badge";
import { Spinner } from "@/components/ui/Spinner";
import { Button } from "@/components/ui/Button";
import { useChatStore } from "@/stores/chatStore";
import { Pulse, ArrowClockwise, WarningCircle } from "@phosphor-icons/react";

interface HeaderProps {
  onRetry?: () => void;
}

export function Header({ onRetry }: HeaderProps) {
  const systemReady = useChatStore((s) => s.systemReady);
  const isInitializing = useChatStore((s) => s.isInitializing);
  const initError = useChatStore((s) => s.initError);

  return (
    <header className="flex items-center justify-between border-b border-border bg-primary px-4 md:px-6 py-3">
      <div className="flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-secondary border border-border">
          <Pulse size={22} weight="bold" className="text-accent" />
        </div>
        <div>
          <h1 className="text-base md:text-lg font-semibold tracking-tight text-foreground">
            AI Financial Advisor
          </h1>
          <p className="text-[11px] text-muted-foreground hidden sm:block">
            Indian Market Intelligence • IPO & Stock Analysis
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {systemReady ? (
          <Badge variant="success">System Active</Badge>
        ) : isInitializing ? (
          <div className="flex items-center gap-2">
            <Spinner size="sm" />
            <span className="text-xs text-muted-foreground">Connecting…</span>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <Badge variant="error" className="cursor-help" title={initError ?? undefined}>
              <WarningCircle size={14} weight="bold" />
              Backend Offline
            </Badge>
            {onRetry && (
              <Button variant="secondary" size="sm" onClick={onRetry} className="h-7 text-xs px-2.5">
                <ArrowClockwise size={14} /> Retry
              </Button>
            )}
          </div>
        )}
      </div>
    </header>
  );
}
