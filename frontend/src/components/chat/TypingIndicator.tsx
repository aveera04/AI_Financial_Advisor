import { useState, useEffect } from "react";

const STAGES = [
  "Analyzing your query...",
  "Routing to specialized financial agent...",
  "Searching market & IPO data...",
  "Synthesizing financial insights...",
];

export function TypingIndicator() {
  const [stageIndex, setStageIndex] = useState(0);
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const stageTimer = setInterval(() => {
      setStageIndex((prev) => (prev + 1) % STAGES.length);
    }, 4500);

    const countTimer = setInterval(() => {
      setSeconds((prev) => prev + 1);
    }, 1000);

    return () => {
      clearInterval(stageTimer);
      clearInterval(countTimer);
    };
  }, []);

  return (
    <div className="flex items-center gap-3 px-4 py-3" role="status" aria-label="AI is thinking">
      <div className="flex items-center gap-1">
        <span className="h-2 w-2 rounded-full bg-accent animate-bounce [animation-delay:0ms]" />
        <span className="h-2 w-2 rounded-full bg-accent animate-bounce [animation-delay:150ms]" />
        <span className="h-2 w-2 rounded-full bg-accent animate-bounce [animation-delay:300ms]" />
      </div>
      <div className="flex items-center gap-2">
        <span className="text-sm text-muted-foreground transition-all duration-300">
          {STAGES[stageIndex]}
        </span>
        <span className="text-xs text-muted-foreground/60 font-mono">({seconds}s)</span>
      </div>
    </div>
  );
}
