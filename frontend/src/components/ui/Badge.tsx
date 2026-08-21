import { type HTMLAttributes } from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-muted text-muted-foreground",
        ipo: "bg-accent/15 text-accent",
        stock: "bg-blue-500/15 text-blue-400",
        search: "bg-amber-500/15 text-amber-400",
        orchestrator: "bg-muted text-muted-foreground",
        success: "bg-accent/15 text-accent",
        error: "bg-destructive/15 text-destructive",
      },
    },
    defaultVariants: { variant: "default" },
  }
);

interface BadgeProps
  extends HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <span className={cn(badgeVariants({ variant, className }))} {...props} />
  );
}
