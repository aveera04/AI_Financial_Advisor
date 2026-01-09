import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { useChatStore } from '@/stores/chatStore';
import { formatDistanceToNow } from 'date-fns';
import { Cloud, HardDrive, Lock } from 'lucide-react';

export function SessionFooter() {
  const { sessionStartTime, sessionSettings, updateSettings } = useChatStore();

  return (
    <footer 
      className="border-t border-border bg-card/30 px-4 py-2"
      role="contentinfo"
    >
      <div className="mx-auto flex max-w-3xl items-center justify-between text-xs text-muted-foreground">
        <div className="flex items-center gap-4">
          {sessionStartTime && (
            <span>
              Session started{' '}
              {formatDistanceToNow(new Date(sessionStartTime), { addSuffix: true })}
            </span>
          )}
          
          <div className="flex items-center gap-2">
            {sessionSettings.storageMode === 'cloud' ? (
              <Cloud className="h-3 w-3" />
            ) : (
              <HardDrive className="h-3 w-3" />
            )}
            <Badge variant="outline" className="h-5 text-[10px]">
              {sessionSettings.storageMode === 'cloud' ? 'Cloud' : 'Local'}
            </Badge>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Lock className="h-3 w-3" />
            <Label htmlFor="privacy-toggle" className="text-xs cursor-pointer">
              Save chats
            </Label>
            <Switch
              id="privacy-toggle"
              checked={sessionSettings.privacyOptIn}
              onCheckedChange={(checked) =>
                updateSettings({ privacyOptIn: checked })
              }
              aria-label="Toggle chat saving"
            />
          </div>
        </div>
      </div>
    </footer>
  );
}
