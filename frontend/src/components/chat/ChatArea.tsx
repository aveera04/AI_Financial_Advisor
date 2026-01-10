import { useRef, useEffect } from 'react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { MessageCard } from '@/components/chat/MessageCard';
import { useChatStore } from '@/stores/chatStore';
import { Bot, Sparkles } from 'lucide-react';

interface ChatAreaProps {
  onFollowUp: (content: string) => void;
  isLoading?: boolean;
}

export function ChatArea({ onFollowUp, isLoading }: ChatAreaProps) {
  const { isInitialized, chats, currentChatId } = useChatStore();
  const currentChat = chats.find(chat => chat.id === currentChatId);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  
  // Debug logging
  console.log('🔍 ChatArea render - isInitialized:', isInitialized, 'currentChatId:', currentChatId);
  console.log('🔍 Current chat:', currentChat);
  console.log('🔍 Messages count:', currentChat?.messages?.length || 0);
  console.log('🔍 isLoading:', isLoading);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
    }
  }, [currentChat?.messages, isLoading]);

  if (!isInitialized) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <div className="text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10">
            <Sparkles className="h-8 w-8 text-primary" />
          </div>
          <h2 className="text-xl font-semibold">Welcome to AI Financial Advisor</h2>
          <p className="mt-2 text-muted-foreground">
            Click <strong>Initialize</strong> in the sidebar to start your session
          </p>
        </div>
      </div>
    );
  }

  // Show welcome message only when there are no messages and not loading
  if (!currentChat?.messages.length && !isLoading) {
    return (
      <div className="flex flex-1 items-center justify-center p-8">
        <div className="max-w-md text-center">
          <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-primary/20 to-primary/5">
            <Bot className="h-10 w-10 text-primary" />
          </div>
          <h2 className="text-2xl font-bold">Hello! I'm your AI Financial Advisor</h2>
          <p className="mt-3 text-muted-foreground">
            I can help you with investment strategies, portfolio analysis, 
            budgeting, and financial planning. All advice is sourced and cited.
          </p>
          <div className="mt-6 grid gap-2 text-left">
            <div className="rounded-lg bg-muted/50 p-3">
              <p className="text-sm font-medium">💡 Quick-start tips:</p>
              <ul className="mt-2 space-y-1 text-sm text-muted-foreground">
                <li>• Ask about ETF expense ratios</li>
                <li>• Request a portfolio review</li>
                <li>• Explore tax-advantaged accounts</li>
                <li>• Upload documents for analysis</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <ScrollArea className="flex-1 p-6">
      <div ref={scrollContainerRef} className="mx-auto max-w-7xl space-y-6">
        {currentChat?.messages.map((message) => (
          <MessageCard
            key={message.id}
            message={message}
            onFollowUp={onFollowUp}
          />
        ))}
        
        {/* Loading indicator */}
        {isLoading && (
          <div className="flex gap-3">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary/10">
              <Bot className="h-4 w-4 text-primary" />
            </div>
            <div className="flex-1 rounded-lg bg-muted/50 p-4">
              <div className="flex items-center gap-2">
                <div className="h-2 w-2 animate-bounce rounded-full bg-primary [animation-delay:-0.3s]"></div>
                <div className="h-2 w-2 animate-bounce rounded-full bg-primary [animation-delay:-0.15s]"></div>
                <div className="h-2 w-2 animate-bounce rounded-full bg-primary"></div>
                <span className="ml-2 text-sm text-muted-foreground">Thinking...</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </ScrollArea>
  );
}
