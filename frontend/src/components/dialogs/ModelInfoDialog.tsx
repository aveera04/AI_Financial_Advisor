import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Brain, Shield, Zap } from 'lucide-react';

interface ModelInfoDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function ModelInfoDialog({ open, onOpenChange }: ModelInfoDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Brain className="h-5 w-5 text-primary" />
            AI Model Information
          </DialogTitle>
          <DialogDescription>
            Learn about the AI powering your financial advisor
          </DialogDescription>
        </DialogHeader>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between rounded-lg bg-muted p-4">
            <div>
              <p className="font-semibold">GPT-5 Thinking mini</p>
              <p className="text-sm text-muted-foreground">
                Advanced reasoning model
              </p>
            </div>
            <Badge variant="secondary">Active</Badge>
          </div>

          <div className="space-y-3">
            <div className="flex items-start gap-3">
              <Zap className="mt-0.5 h-4 w-4 text-primary" />
              <div>
                <p className="text-sm font-medium">Enhanced Reasoning</p>
                <p className="text-xs text-muted-foreground">
                  Advanced chain-of-thought for complex financial analysis
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <Shield className="mt-0.5 h-4 w-4 text-primary" />
              <div>
                <p className="text-sm font-medium">Safety Features</p>
                <p className="text-xs text-muted-foreground">
                  Built-in safeguards for financial advice compliance
                </p>
              </div>
            </div>
          </div>

          <p className="text-xs text-muted-foreground">
            This AI provides informational guidance only and does not constitute
            professional financial, legal, or tax advice. Always consult with
            qualified professionals for specific decisions.
          </p>
        </div>
      </DialogContent>
    </Dialog>
  );
}
