import { useState } from 'react';
import { Sidebar } from '@/components/layout/Sidebar';
import { ChatHeader } from '@/components/chat/ChatHeader';
import { ChatArea } from '@/components/chat/ChatArea';
import { ChatInput } from '@/components/chat/ChatInput';
import { SessionFooter } from '@/components/chat/SessionFooter';
import { RegulatoryWarningDialog } from '@/components/dialogs/RegulatoryWarningDialog';
import { useChatStore } from '@/stores/chatStore';
import { apiService } from '@/services/api';
import type { Source } from '@/types/chat';

const Index = () => {
  const { addMessage, sessionSettings, isInitialized, addAuditEntry, getCurrentChat } = useChatStore();
  const [isLoading, setIsLoading] = useState(false);
  const [pendingRegulatory, setPendingRegulatory] = useState<{
    message: string;
    files?: File[];
    actionType: string;
  } | null>(null);

  const checkRegulatoryContent = (message: string): string | null => {
    const regulatoryPatterns = [
      { pattern: /tax/i, type: 'tax advice' },
      { pattern: /trad(e|ing)/i, type: 'trading orders' },
      { pattern: /legal/i, type: 'legal advice' },
      { pattern: /compliance/i, type: 'regulatory compliance' },
    ];

    for (const { pattern, type } of regulatoryPatterns) {
      if (pattern.test(message)) {
        return type;
      }
    }
    return null;
  };

  const handleSendMessage = async (message: string, files?: File[]) => {
    const regulatoryType = checkRegulatoryContent(message);
    
    if (regulatoryType) {
      setPendingRegulatory({ message, files, actionType: regulatoryType });
      return;
    }

    await processMessage(message, files);
  };

  const processMessage = async (message: string, files?: File[]) => {
    // Add user message
    addMessage({
      role: 'user',
      content: message + (files?.length ? `\n\n[Attached ${files.length} file(s)]` : ''),
    });

    setIsLoading(true);

    try {
      // Call the real API
      const response = await apiService.sendMessage({
        content: message,
        files: files?.map(f => f.name),
      });

      // Add file sources if files were attached
      const allSources = [...response.sources];
      if (files?.length) {
        files.forEach((file, index) => {
          allSources.push({
            id: `upload-${index}`,
            title: `User Upload: ${file.name}`,
            url: '#',
            hostname: 'Local file',
            reason: 'Document provided by user for analysis.',
            quality: 'medium',
            isUserUpload: true,
            filename: file.name,
          });
        });
      }

      // Add assistant message
      addMessage({
        role: 'assistant',
        content: response.content,
        sources: allSources,
        model: response.model,
        isRegulatory: response.is_regulatory,
        requiresConfirmation: response.is_regulatory,
      });

      // Add audit log entry
      addAuditEntry({
        messageId: getCurrentChat()?.messages.length?.toString() || '0',
        sourcesFetched: allSources.map((s) => s.url),
        modelUsed: response.model,
      });
    } catch (error) {
      // Handle error
      addMessage({
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Failed to process message'}`,
        sources: [],
        model: 'error',
        isRegulatory: false,
        requiresConfirmation: false,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegulatoryConfirm = () => {
    if (pendingRegulatory) {
      processMessage(pendingRegulatory.message, pendingRegulatory.files);
      setPendingRegulatory(null);
    }
  };

  const handleFollowUp = (previousContent: string) => {
    // Pre-fill with a follow-up template
  };

  return (
    <div className="flex h-screen bg-background dark">
      <Sidebar />
      
      <main className="flex flex-1 flex-col overflow-hidden">
        <ChatHeader />
        
        <ChatArea onFollowUp={handleFollowUp} />
        
        {isInitialized && (
          <>
            <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
            <SessionFooter />
          </>
        )}
      </main>

      <RegulatoryWarningDialog
        open={!!pendingRegulatory}
        onOpenChange={(open) => !open && setPendingRegulatory(null)}
        actionType={pendingRegulatory?.actionType || ''}
        onConfirm={handleRegulatoryConfirm}
      />
    </div>
  );
};

export default Index;
