import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import {
  Copy,
  FileDown,
  MessageSquarePlus,
  BookmarkPlus,
  ChevronDown,
  ExternalLink,
  Bot,
  User,
  AlertTriangle,
  Check,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import type { ChatMessage, Source } from '@/types/chat';
import { useChatStore } from '@/stores/chatStore';
import { toast } from 'sonner';

interface MessageCardProps {
  message: ChatMessage;
  onFollowUp?: (content: string) => void;
}

function QualityBadge({ quality }: { quality: Source['quality'] }) {
  const variants = {
    high: 'bg-success/20 text-success border-success/30',
    medium: 'bg-warning/20 text-warning border-warning/30',
    low: 'bg-destructive/20 text-destructive border-destructive/30',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center rounded border px-1.5 py-0.5 text-[10px] font-medium uppercase',
        variants[quality]
      )}
    >
      {quality}
    </span>
  );
}

export function MessageCard({ message, onFollowUp }: MessageCardProps) {
  const [sourcesOpen, setSourcesOpen] = useState(false);
  const { confirmRegulatoryAction } = useChatStore();
  const isAssistant = message.role === 'assistant';

  const handleCopy = async () => {
    await navigator.clipboard.writeText(message.content);
    toast.success('Copied to clipboard');
  };

  const handleExportMessage = () => {
    let content = `${message.content}\n\nTimestamp: ${message.timestamp}`;
    
    if (message.sources?.length) {
      content += '\n\nSources:\n';
      message.sources.forEach((s) => {
        content += `- ${s.title} (${s.url}) [${s.quality.toUpperCase()}]\n  Reason: ${s.reason}\n`;
      });
    }
    
    if (message.model) {
      content += `\nModel: ${message.model}`;
    }

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `message-${message.id}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    toast.success('Message exported');
  };

  const handleSaveAsNote = () => {
    toast.success('Saved as note');
  };

  return (
    <div
      className={cn(
        'flex gap-3',
        isAssistant ? 'justify-start' : 'justify-end'
      )}
      role="article"
      aria-label={`${message.role} message`}
    >
      {isAssistant && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary/10">
          <Bot className="h-4 w-4 text-primary" />
        </div>
      )}

      <Card
        className={cn(
          'max-w-[75%] p-4',
          isAssistant
            ? 'bg-card'
            : 'bg-primary text-primary-foreground'
        )}
      >
        {/* Regulatory Warning Banner */}
        {message.isRegulatory && !message.confirmed && (
          <div className="mb-3 flex items-center gap-2 rounded-lg bg-warning/10 p-3 text-warning">
            <AlertTriangle className="h-4 w-4" />
            <span className="text-sm">
              This response contains regulated financial advice.
            </span>
            <Button
              size="sm"
              variant="outline"
              onClick={() => confirmRegulatoryAction(message.id)}
              className="ml-auto border-warning text-warning hover:bg-warning/20"
            >
              <Check className="mr-1 h-3 w-3" />
              Acknowledge
            </Button>
          </div>
        )}

        {/* Message Content */}
        <div className="prose prose-sm dark:prose-invert max-w-none">
          <p className="whitespace-pre-wrap">{message.content}</p>
        </div>

        {/* Sources Section */}
        {isAssistant && message.sources && message.sources.length > 0 && (
          <Collapsible
            open={sourcesOpen}
            onOpenChange={setSourcesOpen}
            className="mt-4"
          >
            <CollapsibleTrigger asChild>
              <Button
                variant="ghost"
                size="sm"
                className="w-full justify-between text-muted-foreground hover:text-foreground"
              >
                <span className="flex items-center gap-2">
                  <ExternalLink className="h-4 w-4" />
                  Sources ({message.sources.length})
                </span>
                <ChevronDown
                  className={cn(
                    'h-4 w-4 transition-transform',
                    sourcesOpen && 'rotate-180'
                  )}
                />
              </Button>
            </CollapsibleTrigger>
            <CollapsibleContent className="mt-2 space-y-2">
              {message.sources.map((source) => (
                <div
                  key={source.id}
                  className="flex items-start gap-2 rounded-lg bg-muted/50 p-2 text-sm"
                >
                  <ExternalLink className="mt-0.5 h-3 w-3 shrink-0 text-primary" />
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2">
                      <a
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="truncate font-medium text-primary hover:underline"
                      >
                        {source.title}
                      </a>
                      <QualityBadge quality={source.quality} />
                    </div>
                    <p className="text-xs text-muted-foreground">
                      {source.hostname}
                    </p>
                    <p className="mt-1 text-xs italic text-muted-foreground">
                      {source.reason}
                    </p>
                    {source.isUserUpload && (
                      <Badge variant="outline" className="mt-1">
                        User upload: {source.filename}
                      </Badge>
                    )}
                  </div>
                </div>
              ))}
            </CollapsibleContent>
          </Collapsible>
        )}

        {/* Model Badge */}
        {isAssistant && message.model && (
          <div className="mt-3 flex items-center gap-2">
            <Badge variant="secondary" className="text-xs">
              Model: {message.model}
            </Badge>
          </div>
        )}

        {/* Action Buttons */}
        {isAssistant && (
          <div className="mt-3 flex flex-wrap items-center gap-2 border-t border-border pt-3">
            <Button
              variant="ghost"
              size="sm"
              onClick={handleSaveAsNote}
              className="h-7 text-xs"
            >
              <BookmarkPlus className="mr-1 h-3 w-3" />
              Save as note
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleCopy}
              className="h-7 text-xs"
            >
              <Copy className="mr-1 h-3 w-3" />
              Copy text
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onFollowUp?.(message.content)}
              className="h-7 text-xs"
            >
              <MessageSquarePlus className="mr-1 h-3 w-3" />
              Ask follow-up
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleExportMessage}
              className="h-7 text-xs"
            >
              <FileDown className="mr-1 h-3 w-3" />
              Export to PDF
            </Button>
          </div>
        )}

        {/* Hidden machine-readable metadata */}
        <div className="sr-only" aria-hidden="true" data-message-id={message.id}>
          {JSON.stringify({
            id: message.id,
            timestamp: message.timestamp,
            model: message.model,
            sources: message.sources,
          })}
        </div>
      </Card>

      {!isAssistant && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-secondary">
          <User className="h-4 w-4 text-secondary-foreground" />
        </div>
      )}
    </div>
  );
}
