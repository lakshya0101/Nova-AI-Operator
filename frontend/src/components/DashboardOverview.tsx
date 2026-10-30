"use client";

import React from "react";
import {
  Cpu,
  Brain,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  Sparkles,
  ShieldCheck,
  Globe,
  Activity,
  Layers,
} from "lucide-react";
import { SystemHealth, Task, MemoryItem } from "../lib/api";

interface DashboardOverviewProps {
  health: SystemHealth | null;
  tasks: Task[];
  memories: MemoryItem[];
  onNavigate: (tab: string) => void;
  onRunQuickDemo: (instruction: string) => void;
}

export default function DashboardOverview({
  health,
  tasks,
  memories,
  onNavigate,
  onRunQuickDemo,
}: DashboardOverviewProps) {
  const pendingTasks = tasks.filter((t) => t.status === "pending" || t.status === "in_progress");
  const completedTasks = tasks.filter((t) => t.status === "completed");

  const quickPrompts = [
    {
      title: "Organize Evening Workflow",
      prompt: "Organize my evening. Prioritize my unfinished tasks and leave time for interview preparation.",
      desc: "Deconstructs schedule, evaluates task priorities, and schedules dedicated prep block.",
    },
    {
      title: "NVIDIA Nemotron Architecture Research",
      prompt: "Research NVIDIA Nemotron AI infrastructure and prepare a comparison with modern agent systems.",
      desc: "Queries Tavily web index, extracts citations, and synthesizes architectural evidence.",
    },
    {
      title: "Contextual Memory Synthesis",
      prompt: "Review my persistent goals and summarize active focus areas for the hackathon.",
      desc: "Retrieves memory embeddings from pgvector/local store and formulates next milestones.",
    },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Hero Welcome Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-surface to-surface-raised border border-surface-border p-8 shadow-xl">
        <div className="absolute top-0 right-0 -mr-16 -mt-16 w-80 h-80 rounded-full bg-cyan-500/10 blur-3xl pointer-events-none"></div>
        <div className="relative z-10 max-w-3xl">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-mono mb-4">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Nebius Token Factory &times; NVIDIA Nemotron Active</span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-2">
            Welcome back, Operator. NOVA is online.
          </h1>
          <p className="text-gray-400 text-base leading-relaxed mb-6">
            Autonomous Personal AI Operating System. Think. Remember. Orchestrate. Execute. Ready to plan multi-step workflows, retrieve contextual memory, and execute verified actions.
          </p>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => onNavigate("workspace")}
              className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-black font-semibold text-sm transition-all shadow-lg shadow-cyan-500/20"
            >
              <span>Launch AI Workspace</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => onNavigate("agents")}
              className="inline-flex items-center space-x-2 px-4 py-2.5 rounded-lg bg-surface-raised hover:bg-surface-border text-gray-200 text-sm font-medium border border-surface-border transition-all"
            >
              <Activity className="w-4 h-4 text-cyan-400" />
              <span>Inspect 6 Specialized Agents</span>
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Model Engine */}
        <div className="p-5 rounded-xl bg-surface border border-surface-border flex flex-col justify-between">
          <div className="flex items-center justify-between text-gray-400 mb-3">
            <span className="text-xs font-mono uppercase tracking-wider">AI Inference</span>
            <Cpu className="w-4 h-4 text-cyan-400" />
          </div>
          <div>
            <div className="text-xl font-bold text-white tracking-wide">Nemotron Super</div>
            <div className="text-xs text-gray-400 mt-1">Dual-tier routing via Nebius</div>
          </div>
          <div className="mt-4 pt-3 border-t border-surface-border flex items-center justify-between text-[11px] font-mono">
            <span className="text-gray-500">Latency: ~12ms</span>
            <span className="text-emerald-400">Online</span>
          </div>
        </div>

        {/* Pending Actions */}
        <div className="p-5 rounded-xl bg-surface border border-surface-border flex flex-col justify-between">
          <div className="flex items-center justify-between text-gray-400 mb-3">
            <span className="text-xs font-mono uppercase tracking-wider">Active Tasks</span>
            <CheckCircle2 className="w-4 h-4 text-blue-400" />
          </div>
          <div>
            <div className="text-2xl font-bold text-white tracking-wide">{pendingTasks.length}</div>
            <div className="text-xs text-gray-400 mt-1">{completedTasks.length} completed milestones</div>
          </div>
          <div className="mt-4 pt-3 border-t border-surface-border flex items-center justify-between text-[11px]">
            <button onClick={() => onNavigate("tasks")} className="text-cyan-400 hover:underline">
              View Task List &rarr;
            </button>
          </div>
        </div>

        {/* Semantic Memory */}
        <div className="p-5 rounded-xl bg-surface border border-surface-border flex flex-col justify-between">
          <div className="flex items-center justify-between text-gray-400 mb-3">
            <span className="text-xs font-mono uppercase tracking-wider">Persistent Memory</span>
            <Brain className="w-4 h-4 text-purple-400" />
          </div>
          <div>
            <div className="text-2xl font-bold text-white tracking-wide">{memories.length}</div>
            <div className="text-xs text-gray-400 mt-1">Contextual memory records</div>
          </div>
          <div className="mt-4 pt-3 border-t border-surface-border flex items-center justify-between text-[11px]">
            <button onClick={() => onNavigate("memory")} className="text-cyan-400 hover:underline">
              Explore Memories &rarr;
            </button>
          </div>
        </div>

        {/* Safety & Protocol */}
        <div className="p-5 rounded-xl bg-surface border border-surface-border flex flex-col justify-between">
          <div className="flex items-center justify-between text-gray-400 mb-3">
            <span className="text-xs font-mono uppercase tracking-wider">Protocol Security</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div>
            <div className="text-xl font-bold text-white tracking-wide">MCP HTTP</div>
            <div className="text-xs text-gray-400 mt-1">Human-in-the-Loop Gated</div>
          </div>
          <div className="mt-4 pt-3 border-t border-surface-border flex items-center justify-between text-[11px] font-mono">
            <span className="text-gray-500">Port 8000/mcp</span>
            <span className="text-cyan-400">Secured</span>
          </div>
        </div>
      </div>

      {/* Featured Hackathon Demonstrations */}
      <div className="rounded-xl bg-surface border border-surface-border p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center space-x-2">
              <Layers className="w-5 h-5 text-cyan-400" />
              <span>Core Demonstration Workflows</span>
            </h2>
            <p className="text-xs text-gray-400 mt-0.5">
              Select any benchmark scenario to observe real multi-agent planning and execution.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {quickPrompts.map((q, idx) => (
            <div
              key={idx}
              className="p-4 rounded-lg bg-surface-raised border border-surface-border hover:border-cyan-500/50 transition-all flex flex-col justify-between group"
            >
              <div>
                <h3 className="font-semibold text-white text-sm group-hover:text-cyan-400 transition-colors">
                  {q.title}
                </h3>
                <p className="text-xs text-gray-400 mt-1 leading-relaxed">{q.desc}</p>
                <div className="mt-3 p-2 rounded bg-black/40 border border-surface-border text-[11px] font-mono text-gray-300">
                  &ldquo;{q.prompt}&rdquo;
                </div>
              </div>
              <button
                onClick={() => onRunQuickDemo(q.prompt)}
                className="mt-4 w-full py-2 px-3 rounded bg-cyan-500/10 hover:bg-cyan-500 text-cyan-400 hover:text-black font-medium text-xs transition-all flex items-center justify-center space-x-1.5"
              >
                <span>Execute Scenario</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

