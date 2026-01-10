import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  ToggleGroup,
  ToggleGroupItem,
} from '@/components/ui/toggle-group';
import { 
  FileDown, 
  TrendingUp, 
  HelpCircle,
  Sparkles
} from 'lucide-react';
import { useChatStore } from '@/stores/chatStore';
import { ModelInfoDialog } from '@/components/dialogs/ModelInfoDialog';

const currencies = [
  { value: 'USD', label: '$ USD' },
  { value: 'EUR', label: '€ EUR' },
  { value: 'GBP', label: '£ GBP' },
  { value: 'JPY', label: '¥ JPY' },
  { value: 'CAD', label: '$ CAD' },
];

const riskProfiles = [
  { value: 'conservative', label: 'Conservative', color: 'bg-green-500' },
  { value: 'moderate', label: 'Moderate', color: 'bg-yellow-500' },
  { value: 'aggressive', label: 'Aggressive', color: 'bg-red-500' },
];

export function ChatHeader() {
  const { sessionSettings, updateSettings, getCurrentChat } = useChatStore();
  const [showModelInfo, setShowModelInfo] = useState(false);
  const currentChat = getCurrentChat();

  const handleExportConversation = () => {
    if (!currentChat) return;

    const content = currentChat.messages
      .map((msg) => {
        let text = `[${msg.role.toUpperCase()}] ${msg.timestamp}\n${msg.content}`;
        if (msg.sources?.length) {
          text += '\n\nSources:\n';
          msg.sources.forEach((s) => {
            text += `- ${s.title} (${s.hostname}) - ${s.reason}\n`;
          });
        }
        if (msg.model) {
          text += `\nModel: ${msg.model}`;
        }
        return text;
      })
      .join('\n\n---\n\n');

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentChat.title}-export.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <header className="border-b border-border bg-card/50 backdrop-blur-sm">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
            <Sparkles className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">
              AI Financial Advisor
            </h1>
            <p className="text-xs text-muted-foreground">
              Powered by GPT-5 Thinking mini
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          {/* Tone Selector */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-muted-foreground">Tone:</span>
            <ToggleGroup
              type="single"
              value={sessionSettings.tone}
              onValueChange={(value) =>
                value && updateSettings({ tone: value as 'concise' | 'detailed' })
              }
              aria-label="Response tone"
            >
              <ToggleGroupItem value="concise" size="sm" aria-label="Concise responses">
                Concise
              </ToggleGroupItem>
              <ToggleGroupItem value="detailed" size="sm" aria-label="Detailed responses">
                Detailed
              </ToggleGroupItem>
            </ToggleGroup>
          </div>

          {/* Currency Selector */}
          <Select
            value={sessionSettings.currency}
            onValueChange={(value) => updateSettings({ currency: value })}
          >
            <SelectTrigger className="w-24" aria-label="Select currency">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {currencies.map((curr) => (
                <SelectItem key={curr.value} value={curr.value}>
                  {curr.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* Risk Profile */}
          <div className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
            <Select
              value={sessionSettings.riskProfile}
              onValueChange={(value) =>
                updateSettings({
                  riskProfile: value as 'conservative' | 'moderate' | 'aggressive',
                })
              }
            >
              <SelectTrigger className="w-32" aria-label="Select risk profile">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {riskProfiles.map((profile) => (
                  <SelectItem key={profile.value} value={profile.value}>
                    <div className="flex items-center gap-2">
                      <span
                        className={`h-2 w-2 rounded-full ${profile.color}`}
                      />
                      {profile.label}
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Export Button */}
          <Button
            variant="outline"
            size="sm"
            onClick={handleExportConversation}
            disabled={!currentChat?.messages.length}
            aria-label="Export conversation to PDF"
          >
            <FileDown className="mr-2 h-4 w-4" />
            Export
          </Button>

          {/* Model Info */}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setShowModelInfo(true)}
            aria-label="Model information"
          >
            <HelpCircle className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <ModelInfoDialog open={showModelInfo} onOpenChange={setShowModelInfo} />
    </header>
  );
}
