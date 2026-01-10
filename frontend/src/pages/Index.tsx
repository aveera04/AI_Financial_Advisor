import { useState, useEffect } from 'react';
import { Sidebar } from '@/components/layout/Sidebar';
import { ChatHeader } from '@/components/chat/ChatHeader';
import { ChatArea } from '@/components/chat/ChatArea';
import { ChatInput } from '@/components/chat/ChatInput';
import { SessionFooter } from '@/components/chat/SessionFooter';
import { RegulatoryWarningDialog } from '@/components/dialogs/RegulatoryWarningDialog';
import { useChatStore } from '@/stores/chatStore';
import type { Source } from '@/types/chat';
import { apiService } from '@/services/api';
import { useToast } from '@/hooks/use-toast';

const Index = () => {
  const { addMessage, sessionSettings, isInitialized, addAuditEntry, getCurrentChat } = useChatStore();
  const [isLoading, setIsLoading] = useState(false);
  const [isApiAvailable, setIsApiAvailable] = useState<boolean | null>(null);
  const { toast } = useToast();
  const [pendingRegulatory, setPendingRegulatory] = useState<{
    message: string;
    files?: File[];
    actionType: string;
  } | null>(null);

  // Check API availability on mount
  useEffect(() => {
    const checkApi = async () => {
      const available = await apiService.isAvailable();
      setIsApiAvailable(available);
      if (!available) {
        toast({
          title: "Backend Unavailable",
          description: "The AI backend is not responding. Please ensure the API server is running on port 8000.",
          variant: "destructive",
        });
      }
    };
    checkApi();
  }, [toast]);

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
    console.log('🚀 Processing message:', message);
    console.log('📊 Current chat before adding user message:', getCurrentChat());
    
    // Add user message
    addMessage({
      role: 'user',
      content: message + (files?.length ? `\n\n[Attached ${files.length} file(s)]` : ''),
    });
    
    console.log('✅ User message added, current chat:', getCurrentChat());

    setIsLoading(true);

    try {
      // Call the real API
      const response = await apiService.sendMessage({
        message: message,
        tone: sessionSettings.tone,
      });

      // Convert API sources to the expected format
      const allSources: Source[] = response.sources.map((s) => ({
        id: s.id,
        title: s.title,
        url: s.url,
        hostname: s.hostname,
        reason: s.reason,
        quality: s.quality as 'high' | 'medium' | 'low',
      }));

      // Add file sources if files were attached
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
      
      console.log('✅ Assistant message added, current chat:', getCurrentChat());

      // Add audit log entry
      addAuditEntry({
        messageId: getCurrentChat()?.messages.length?.toString() || '0',
        sourcesFetched: allSources.map((s) => s.url),
        modelUsed: response.model,
      });

    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message as assistant response
      addMessage({
        role: 'assistant',
        content: `Sorry, I encountered an error while processing your request. ${error instanceof Error ? error.message : 'Please try again later.'}`,
        model: 'Error',
        isRegulatory: false,
      });

      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to get response from AI",
        variant: "destructive",
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
        
        <ChatArea onFollowUp={handleFollowUp} isLoading={isLoading} />
        
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
