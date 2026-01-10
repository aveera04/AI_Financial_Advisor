import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { AlertTriangle } from 'lucide-react';

interface RegulatoryWarningDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  actionType: string;
  onConfirm: () => void;
}

export function RegulatoryWarningDialog({
  open,
  onOpenChange,
  actionType,
  onConfirm,
}: RegulatoryWarningDialogProps) {
  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent className="border-warning/50">
        <AlertDialogHeader>
          <AlertDialogTitle className="flex items-center gap-2 text-warning">
            <AlertTriangle className="h-5 w-5" />
            Regulatory Warning
          </AlertDialogTitle>
          <AlertDialogDescription className="space-y-2">
            <p>
              You are about to request advice related to{' '}
              <strong>{actionType}</strong>.
            </p>
            <p>
              This type of advice may have legal and financial implications.
              Please note:
            </p>
            <ul className="ml-4 mt-2 list-disc space-y-1 text-sm">
              <li>AI-generated content is for informational purposes only</li>
              <li>
                This does not constitute professional financial, legal, or tax
                advice
              </li>
              <li>
                Consult with qualified professionals before making decisions
              </li>
              <li>
                You are responsible for verifying information and compliance
              </li>
            </ul>
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={onConfirm}
            className="bg-warning text-warning-foreground hover:bg-warning/90"
          >
            I Understand, Proceed
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
