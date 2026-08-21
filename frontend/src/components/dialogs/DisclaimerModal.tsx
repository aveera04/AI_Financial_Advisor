import { useEffect, useState } from "react";
import { Button } from "@/components/ui/Button";
import { ShieldCheck } from "@phosphor-icons/react";

const STORAGE_KEY = "sebi_disclaimer_accepted";

export function DisclaimerModal() {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  useEffect(() => {
    const accepted = localStorage.getItem(STORAGE_KEY);
    if (!accepted) setIsOpen(true);
  }, []);

  function handleAccept() {
    localStorage.setItem(STORAGE_KEY, "true");
    setIsOpen(false);
  }

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="disclaimer-title"
    >
      <div className="w-full max-w-lg rounded-2xl border border-border bg-card p-6 shadow-2xl animate-in fade-in zoom-in-95 duration-200">
        <div className="mb-4 flex items-center gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-accent/15 text-accent border border-accent/20">
            <ShieldCheck size={26} weight="duotone" />
          </div>
          <div>
            <h2 id="disclaimer-title" className="text-lg font-semibold text-foreground">
              Important Disclaimer
            </h2>
            <p className="text-xs text-muted-foreground">SEBI Regulatory Notice</p>
          </div>
        </div>

        <div className="space-y-3 text-sm leading-relaxed text-muted-foreground border-y border-border/50 py-4 my-2">
          <p>
            This AI Financial Advisor is for <strong className="text-foreground">informational purposes only</strong> and does not constitute investment advice, financial advice, trading advice, or any other form of advice.
          </p>
          <p>
            This tool is not registered with the <strong className="text-foreground">Securities and Exchange Board of India (SEBI)</strong> as an investment advisor. All information provided should be independently verified.
          </p>
          <p>
            Always consult a qualified, SEBI-registered financial advisor before making any investment decisions. Past performance does not guarantee future results.
          </p>
        </div>

        <div className="mt-6 flex justify-end">
          <Button onClick={handleAccept} className="px-6">
            I Understand & Accept
          </Button>
        </div>
      </div>
    </div>
  );
}
