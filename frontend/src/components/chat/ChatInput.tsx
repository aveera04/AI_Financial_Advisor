import { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import {
  Send,
  Paperclip,
  X,
  TrendingUp,
  PiggyBank,
  Shield,
  Calculator,
  Loader2,
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface ChatInputProps {
  onSend: (message: string, files?: File[]) => void;
  isLoading: boolean;
}

const quickPrompts = [
  { label: 'Investment basics', icon: TrendingUp, prompt: 'What are the best investment strategies for beginners?' },
  { label: 'Savings tips', icon: PiggyBank, prompt: 'How can I save more money each month?' },
  { label: 'Risk assessment', icon: Shield, prompt: 'How do I assess my risk tolerance for investing?' },
  { label: 'Tax planning', icon: Calculator, prompt: 'What are common tax deductions I might be missing?' },
];

export function ChatInput({ onSend, isLoading }: ChatInputProps) {
  const [input, setInput] = useState('');
  const [attachedFiles, setAttachedFiles] = useState<File[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = () => {
    if (!input.trim() && attachedFiles.length === 0) return;
    onSend(input, attachedFiles);
    setInput('');
    setAttachedFiles([]);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setAttachedFiles((prev) => [...prev, ...Array.from(e.target.files!)]);
    }
  };

  const removeFile = (index: number) => {
    setAttachedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleQuickPrompt = (prompt: string) => {
    setInput(prompt);
  };

  return (
    <div className="border-t border-border bg-card/50 p-4 backdrop-blur-sm">
      <div className="mx-auto max-w-3xl space-y-3">
        {/* Quick Prompts */}
        <div className="flex flex-wrap gap-2">
          {quickPrompts.map((qp) => (
            <Button
              key={qp.label}
              variant="outline"
              size="sm"
              onClick={() => handleQuickPrompt(qp.prompt)}
              className="gap-2 text-xs"
              disabled={isLoading}
            >
              <qp.icon className="h-3 w-3" />
              {qp.label}
            </Button>
          ))}
        </div>

        {/* Attached Files */}
        {attachedFiles.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {attachedFiles.map((file, index) => (
              <Badge
                key={index}
                variant="secondary"
                className="flex items-center gap-1"
              >
                <Paperclip className="h-3 w-3" />
                {file.name}
                <button
                  onClick={() => removeFile(index)}
                  className="ml-1 rounded-full p-0.5 hover:bg-muted"
                  aria-label={`Remove ${file.name}`}
                >
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            ))}
          </div>
        )}

        {/* Input Area */}
        <div className="flex items-end gap-2">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            multiple
            className="hidden"
            aria-label="Attach files"
          />
          
          <Button
            variant="ghost"
            size="icon"
            onClick={() => fileInputRef.current?.click()}
            disabled={isLoading}
            aria-label="Attach file"
          >
            <Paperclip className="h-5 w-5" />
          </Button>

          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about investments, savings, or financial planning..."
            className="min-h-[44px] max-h-[200px] flex-1 resize-none bg-muted/50"
            disabled={isLoading}
            rows={1}
            aria-label="Type your message"
          />

          <Button
            onClick={handleSubmit}
            disabled={isLoading || (!input.trim() && attachedFiles.length === 0)}
            size="icon"
            className={cn(
              'transition-all',
              input.trim() || attachedFiles.length > 0
                ? 'bg-primary text-primary-foreground'
                : ''
            )}
            aria-label="Send message"
          >
            {isLoading ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <Send className="h-5 w-5" />
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}
