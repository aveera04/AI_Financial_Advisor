import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Play, 
  Trash2, 
  MessageSquare, 
  MoreHorizontal,
  Pencil,
  FileDown,
  Search
} from 'lucide-react';
import { useChatStore } from '@/stores/chatStore';
import { formatDistanceToNow } from 'date-fns';
import { ClearChatDialog } from '@/components/dialogs/ClearChatDialog';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

export function Sidebar() {
  const { 
    chats, 
    currentChatId, 
    isInitialized,
    initializeSession, 
    loadChat, 
    deleteChat,
    renameChat 
  } = useChatStore();
  
  const [showClearDialog, setShowClearDialog] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [editingChatId, setEditingChatId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [isInitializing, setIsInitializing] = useState(false);

  const recentChats = chats
    .filter(chat => 
      chat.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      chat.lastMessage.toLowerCase().includes(searchQuery.toLowerCase())
    )
    .slice(0, 10);

  const handleRename = (chatId: string) => {
    if (editTitle.trim()) {
      renameChat(chatId, editTitle.trim());
    }
    setEditingChatId(null);
    setEditTitle('');
  };

  const handleExportChat = (chatId: string) => {
    const chat = chats.find(c => c.id === chatId);
    if (!chat) return;
    
    const content = chat.messages
      .map(m => `[${m.role.toUpperCase()}] ${m.content}`)
      .join('\n\n');
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${chat.title}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleInitialize = async () => {
    setIsInitializing(true);
    try {
      await initializeSession();
    } catch (error) {
      console.error('Failed to initialize:', error);
      // You might want to show a toast notification here
    } finally {
      setIsInitializing(false);
    }
  };

  return (
    <aside 
      className="flex h-full w-64 flex-col border-r border-border bg-sidebar"
      role="complementary"
      aria-label="Chat sidebar"
    >
      {/* Initialize Button */}
      <div className="p-4">
        <Button
          onClick={handleInitialize}
          className="w-full gap-2"
          variant={isInitialized ? "secondary" : "default"}
          aria-label="Initialize new session"
          disabled={isInitializing}
        >
          <Play className="h-4 w-4" />
          {isInitializing ? 'Initializing...' : (isInitialized ? 'New Session' : 'Initialize')}
        </Button>
      </div>

      {/* Search */}
      <div className="px-4 pb-2">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search chats..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9 bg-muted/50"
            aria-label="Search conversations"
          />
        </div>
      </div>

      {/* Recent Chats */}
      <div className="flex-1 overflow-hidden">
        <div className="px-4 py-2">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Recent Chats
          </h3>
        </div>
        <ScrollArea className="h-full px-2">
          <nav aria-label="Recent conversations" className="space-y-1 pb-4">
            {recentChats.length === 0 ? (
              <p className="px-2 py-4 text-center text-sm text-muted-foreground">
                No conversations yet
              </p>
            ) : (
              recentChats.map((chat) => (
                <div
                  key={chat.id}
                  className={cn(
                    "group relative flex items-center gap-2 rounded-lg p-2 transition-colors hover:bg-muted/50",
                    currentChatId === chat.id && "bg-muted"
                  )}
                >
                  <button
                    onClick={() => loadChat(chat.id)}
                    className="flex flex-1 items-start gap-2 text-left"
                    aria-current={currentChatId === chat.id ? 'page' : undefined}
                  >
                    <MessageSquare className="mt-0.5 h-4 w-4 shrink-0 text-muted-foreground" />
                    <div className="min-w-0 flex-1">
                      {editingChatId === chat.id ? (
                        <Input
                          value={editTitle}
                          onChange={(e) => setEditTitle(e.target.value)}
                          onBlur={() => handleRename(chat.id)}
                          onKeyDown={(e) => e.key === 'Enter' && handleRename(chat.id)}
                          className="h-6 text-sm"
                          autoFocus
                          onClick={(e) => e.stopPropagation()}
                        />
                      ) : (
                        <>
                          <p className="truncate text-sm font-medium">
                            {chat.title}
                          </p>
                          <p className="truncate text-xs text-muted-foreground">
                            {chat.lastMessage || 'No messages'}
                          </p>
                          <p className="text-xs text-muted-foreground/70">
                            {formatDistanceToNow(new Date(chat.timestamp), { addSuffix: true })}
                          </p>
                        </>
                      )}
                    </div>
                  </button>
                  
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6 opacity-0 group-hover:opacity-100"
                        aria-label="Chat options"
                      >
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem
                        onClick={() => {
                          setEditingChatId(chat.id);
                          setEditTitle(chat.title);
                        }}
                      >
                        <Pencil className="mr-2 h-4 w-4" />
                        Rename
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => handleExportChat(chat.id)}>
                        <FileDown className="mr-2 h-4 w-4" />
                        Export
                      </DropdownMenuItem>
                      <DropdownMenuItem
                        onClick={() => deleteChat(chat.id)}
                        className="text-destructive focus:text-destructive"
                      >
                        <Trash2 className="mr-2 h-4 w-4" />
                        Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              ))
            )}
          </nav>
        </ScrollArea>
      </div>

      {/* Clear Chat Button */}
      <div className="border-t border-border p-4">
        <Button
          variant="outline"
          className="w-full gap-2 text-destructive hover:bg-destructive/10 hover:text-destructive"
          onClick={() => setShowClearDialog(true)}
          disabled={!currentChatId}
          aria-label="Clear current chat"
        >
          <Trash2 className="h-4 w-4" />
          Clear Chat
        </Button>
      </div>

      <ClearChatDialog 
        open={showClearDialog} 
        onOpenChange={setShowClearDialog} 
      />
    </aside>
  );
}
