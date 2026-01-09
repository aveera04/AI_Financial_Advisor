import { useState } from 'react';
import { Sidebar } from '@/components/layout/Sidebar';
import { ChatHeader } from '@/components/chat/ChatHeader';
import { ChatArea } from '@/components/chat/ChatArea';
import { ChatInput } from '@/components/chat/ChatInput';
import { SessionFooter } from '@/components/chat/SessionFooter';
import { RegulatoryWarningDialog } from '@/components/dialogs/RegulatoryWarningDialog';
import { useChatStore } from '@/stores/chatStore';
import type { Source } from '@/types/chat';

// Mock response generator for demo
const generateMockResponse = (userMessage: string, tone: 'concise' | 'detailed') => {
  const regulatoryKeywords = ['tax', 'trading', 'legal', 'compliance', 'irs', 'sec'];
  const isRegulatory = regulatoryKeywords.some((k) =>
    userMessage.toLowerCase().includes(k)
  );

  const mockSources: Source[] = [
    {
      id: '1',
      title: 'Understanding ETF Expense Ratios',
      url: 'https://www.investopedia.com/terms/e/expenseratio.asp',
      hostname: 'investopedia.com',
      reason: 'Used to define ETF expense ratios and their impact on returns.',
      quality: 'high',
    },
    {
      id: '2',
      title: 'SEC Investor Bulletin',
      url: 'https://www.sec.gov/investor/alerts',
      hostname: 'sec.gov',
      reason: 'Recent regulation summary and investor protection guidelines.',
      quality: 'high',
    },
    {
      id: '3',
      title: 'Market Analysis Report',
      url: 'https://www.morningstar.com/articles',
      hostname: 'morningstar.com',
      reason: 'Current market trends and fund performance data.',
      quality: 'medium',
    },
  ];

  const shortAnswer = tone === 'concise' 
    ? 'Based on your question, here\'s a brief overview of the key points you should consider.'
    : 'Thank you for your question. Let me provide you with a comprehensive analysis.';

  const detailedContent = tone === 'detailed'
    ? `\n\n**Key Considerations:**\n\n1. **Expense Ratios**: When evaluating investments, always consider the expense ratio, which directly impacts your returns over time.\n\n2. **Diversification**: Spreading investments across different asset classes can help manage risk effectively.\n\n3. **Time Horizon**: Your investment timeline significantly influences the appropriate strategy and risk level.\n\n4. **Tax Implications**: Consider the tax efficiency of your investments, especially in taxable accounts.`
    : '';

  return {
    content: shortAnswer + detailedContent,
    sources: mockSources,
    model: 'GPT-5 Thinking mini',
    isRegulatory,
  };
};

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

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500));

    const response = generateMockResponse(message, sessionSettings.tone);

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
      isRegulatory: response.isRegulatory,
      requiresConfirmation: response.isRegulatory,
    });

    // Add audit log entry
    addAuditEntry({
      messageId: getCurrentChat()?.messages.length?.toString() || '0',
      sourcesFetched: allSources.map((s) => s.url),
      modelUsed: response.model,
    });

    setIsLoading(false);
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
