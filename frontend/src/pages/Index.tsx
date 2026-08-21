import { Header } from "@/components/layout/Header";
import { Sidebar } from "@/components/layout/Sidebar";
import { ChatWindow } from "@/components/chat/ChatWindow";
import { ChatInput } from "@/components/chat/ChatInput";
import { DisclaimerModal } from "@/components/dialogs/DisclaimerModal";
import { useSystemInit } from "@/hooks/useSystemInit";
import { useChatStore } from "@/stores/chatStore";
import { ShieldCheck, WarningCircle, ArrowClockwise } from "@phosphor-icons/react";

export default function IndexPage() {
  const { retry } = useSystemInit();
  const initError = useChatStore((s) => s.initError);

  return (
    <>
      <DisclaimerModal />
      <div className="flex h-full w-full flex-col bg-background text-foreground overflow-hidden">
        <Header onRetry={retry} />

        {initError && (
          <div className="bg-destructive/15 border-b border-destructive/30 px-4 py-2 text-xs flex items-center justify-between text-destructive shrink-0">
            <div className="flex items-center gap-2">
              <WarningCircle size={16} weight="bold" />
              <span>
                <strong>Backend disconnected:</strong> Could not connect to FastAPI server at http://localhost:8000. Run{" "}
                <code className="bg-destructive/20 px-1 py-0.5 rounded text-[11px]">
                  uvicorn api.main:app --reload --port 8000
                </code>
              </span>
            </div>
            <button
              onClick={retry}
              className="flex items-center gap-1 font-medium underline underline-offset-2 hover:opacity-80 cursor-pointer ml-4"
            >
              <ArrowClockwise size={14} /> Retry
            </button>
          </div>
        )}

        <div className="flex flex-1 min-h-0 overflow-hidden">
          <div className="hidden md:flex h-full">
            <Sidebar onInitialize={retry} />
          </div>
          <main className="flex flex-1 min-h-0 flex-col overflow-hidden bg-background">
            <ChatWindow />
            <ChatInput onRetry={retry} />
            <footer className="border-t border-border bg-primary px-4 py-2 text-center shrink-0">
              <p className="flex items-center justify-center gap-1.5 text-[11px] text-muted-foreground">
                <ShieldCheck size={14} weight="duotone" />
                Not SEBI registered. Informational purposes only. Consult a qualified financial advisor before investing.
              </p>
            </footer>
          </main>
        </div>
      </div>
    </>
  );
}
