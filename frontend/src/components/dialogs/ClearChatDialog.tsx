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
import { useChatStore } from '@/stores/chatStore';

interface ClearChatDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function ClearChatDialog({ open, onOpenChange }: ClearChatDialogProps) {
  const clearCurrentChat = useChatStore((state) => state.clearCurrentChat);

  const handleConfirm = () => {
    clearCurrentChat();
    onOpenChange(false);
  };

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Clear this chat?</AlertDialogTitle>
          <AlertDialogDescription>
            This action cannot be undone. All messages in this conversation will
            be permanently deleted.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={handleConfirm}
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
          >
            Confirm
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
