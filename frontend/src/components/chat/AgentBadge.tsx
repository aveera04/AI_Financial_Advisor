import { Badge } from "@/components/ui/Badge";
import {
  ChartBar, TrendUp, MagnifyingGlass, Robot,
} from "@phosphor-icons/react";

interface AgentBadgeProps {
  agentUsed: string;
}

export function AgentBadge({ agentUsed }: AgentBadgeProps) {
  const config = getAgentConfig(agentUsed);
  return (
    <Badge variant={config.variant}>
      <config.icon size={14} weight="bold" />
      {config.label}
    </Badge>
  );
}

function getAgentConfig(agentUsed: string) {
  if (agentUsed.includes("IPO"))
    return { label: "IPO Advisor", variant: "ipo" as const, icon: ChartBar };
  if (agentUsed.includes("Stock"))
    return { label: "Stock Advisor", variant: "stock" as const, icon: TrendUp };
  if (agentUsed.includes("Search") || agentUsed.includes("Tavily"))
    return { label: "Web Search", variant: "search" as const, icon: MagnifyingGlass };
  return { label: "Orchestrator", variant: "orchestrator" as const, icon: Robot };
}
