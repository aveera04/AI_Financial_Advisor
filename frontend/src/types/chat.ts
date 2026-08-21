export type Role = "user" | "assistant";

export type AgentRoute =
  | "IPO Advisor Agent"
  | "Stock Advisor Agent"
  | "Web Search Tool (Tavily)"
  | "Orchestrator";

export interface AgentInfo {
  agent_used: string;
  route_info: string;
  processing_time: number;
}

export interface Message {
  id: string;
  role: Role;
  content: string;
  timestamp: Date;
  agentInfo?: AgentInfo;
}
