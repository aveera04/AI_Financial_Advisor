import { useEffect, useCallback } from "react";
import { api } from "@/services/api";
import { useChatStore } from "@/stores/chatStore";

export function useSystemInit() {
  const setSystemReady = useChatStore((s) => s.setSystemReady);
  const setIsInitializing = useChatStore((s) => s.setIsInitializing);
  const setInitError = useChatStore((s) => s.setInitError);
  const setSampleQueries = useChatStore((s) => s.setSampleQueries);

  const initSystem = useCallback(async () => {
    setIsInitializing(true);
    setInitError(null);

    try {
      const health = await api.health();
      if (health.status === "ok") {
        setSystemReady(true);
        setInitError(null);
      } else {
        await api.initialize();
        setSystemReady(true);
        setInitError(null);
      }
    } catch (err: unknown) {
      try {
        await api.initialize();
        setSystemReady(true);
        setInitError(null);
      } catch (innerErr: unknown) {
        setSystemReady(false);
        const msg =
          innerErr instanceof Error
            ? innerErr.message
            : "Cannot reach FastAPI backend server at http://localhost:8000";
        setInitError(msg);
      }
    } finally {
      setIsInitializing(false);
    }

    try {
      const data = await api.sampleQueries();
      if (data?.queries?.length) {
        setSampleQueries(data.queries);
      }
    } catch {
      setSampleQueries([
        "What are the current IPO opportunities in India?",
        "Analyze RELIANCE stock for investment",
        "What are today's stock market trends?",
        "Compare IPO vs mutual fund returns",
        "Tell me about Hyundai Motor India IPO",
        "What is the GMP for recent IPOs?",
      ]);
    }
  }, [setSystemReady, setIsInitializing, setInitError, setSampleQueries]);

  useEffect(() => {
    initSystem();
  }, [initSystem]);

  return { retry: initSystem };
}
