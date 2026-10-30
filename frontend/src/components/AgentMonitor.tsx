"use client";

import React from "react";
import {
  Brain,
  Globe,
  Compass,
  ShieldAlert,
  PlayCircle,
  Sparkles,
  CheckCircle2,
  Cpu,
  Activity,
  Clock,
  AlertTriangle,
} from "lucide-react";
import { AgentLogItem } from "../lib/api";

interface AgentMonitorProps {
  logs?: AgentLogItem[];
}

export default function AgentMonitor({ logs = [] }: AgentMonitorProps) {
  // Determine dynamic real-time status of each agent from live logs
  const getAgentStatus = (agentName: string) => {
    const agentLogs = logs.filter((l) => l.agent.toLowerCase().includes(agentName.toLowerCase()));
    if (agentLogs.length === 0) {
      return { label: "Idle / Ready", color: "bg-gray-800 text-gray-400 border-gray-700" };
    }
    const last = agentLogs[agentLogs.length - 1];
    if (last.status === "failed") {
      return { label: "Failed", color: "bg-rose-950/60 text-rose-400 border-rose-800" };
    }
    if (last.status === "waiting_approval") {
      return { label: "Waiting Approval", color: "bg-amber-950/60 text-amber-400 border-amber-800" };
    }
    return { label: "Completed", color: "bg-emerald-950/60 text-emerald-400 border-emerald-800" };
  };

  const agents = [
    {
      id: "planner",
      name: "Planner Agent",
      role: "Goal Decomposition & Strategic Sequencing",
      model: "NVIDIA Nemotron Super",
      icon: Compass,
      color: "text-blue-400 border-blue-500/30 bg-blue-500/10",
      description: "Decomposes complex objectives, analyzes task dependencies, and sets approval boundaries.",
    },
    {
      id: "research",
      name: "Research Agent",
      role: "Web Intelligence & Evidence Extraction",
      model: "Tavily Web Search + Nemotron",
      icon: Globe,
      color: "text-cyan-400 border-cyan-500/30 bg-cyan-500/10",
      description: "Executes targeted web search queries, validates source credibility, and preserves citation links.",
    },
    {
      id: "memory",
      name: "Memory Agent",
      role: "Personal Context & Semantic Retrieval",
      model: "pgvector / Cosine Semantic Store",
      icon: Brain,
      color: "text-purple-400 border-purple-500/30 bg-purple-500/10",
      description: "Extracts relevant personal preferences, decisions, and active goals before workflow execution.",
    },
    {
      id: "execution",
      name: "Execution Agent",
      role: "Action Execution via MCP Protocol",
      model: "MCP Streamable HTTP Tools",
      icon: PlayCircle,
      color: "text-emerald-400 border-emerald-500/30 bg-emerald-500/10",
      description: "Invokes backend MCP tools (get_tasks, create_task, update_task_status) safely.",
    },
    {
      id: "critic",
      name: "Critic Agent",
      role: "Safety Gating & Coherence Verification",
      model: "NVIDIA Nemotron Lightning",
      icon: ShieldAlert,
      color: "text-amber-400 border-amber-500/30 bg-amber-500/10",
      description: "Verifies human approval constraints on mutations and checks plan feasibility before execution.",
    },
    {
      id: "reflection",
      name: "Reflection Agent",
      role: "Post-Execution Analysis & Continuous Learning",
      model: "NVIDIA Nemotron Lightning",
      icon: Sparkles,
      color: "text-rose-400 border-rose-500/30 bg-rose-500/10",
      description: "Analyzes workflow efficiency and persists verified execution memories for continuous improvement.",
    },
  ];

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <Activity className="w-5 h-5 text-cyan-400" />
            <span>Specialized Multi-Agent Swarm</span>
          </h2>
          <p className="text-xs text-gray-400 mt-1">
            Real-time status of NOVA&apos;s modular agents coordinated via Nebius Token Factory.
          </p>
        </div>
        <div className="flex items-center space-x-2 text-xs font-mono text-cyan-400 bg-cyan-950/40 border border-cyan-800 px-3 py-1.5 rounded-lg">
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
          <span>6 Agents Initialized</span>
        </div>
      </div>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent) => {
          const Icon = agent.icon;
          const status = getAgentStatus(agent.id);
          return (
            <div
              key={agent.id}
              className="p-5 rounded-xl bg-surface border border-surface-border flex flex-col justify-between hover:border-surface-border/80 transition-all group"
            >
              <div>
                <div className="flex items-start justify-between mb-3">
                  <div className={`p-2.5 rounded-lg border ${agent.color}`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <span
                    className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${status.color}`}
                  >
                    {status.label}
                  </span>
                </div>
                <h3 className="font-bold text-white text-base group-hover:text-cyan-400 transition-colors">
                  {agent.name}
                </h3>
                <p className="text-xs font-medium text-cyan-400/90 mt-0.5">{agent.role}</p>
                <p className="text-xs text-gray-400 mt-2.5 leading-relaxed">{agent.description}</p>
              </div>

              <div className="mt-5 pt-3 border-t border-surface-border flex items-center justify-between text-[11px] font-mono text-gray-500">
                <span>Model:</span>
                <span className="text-gray-300">{agent.model}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Live Agent Event Logs */}
      <div className="rounded-xl bg-surface border border-surface-border p-6">
        <h3 className="text-sm font-mono uppercase tracking-wider text-white mb-4 flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-cyan-400" />
          <span>Real-Time Multi-Agent Trace</span>
        </h3>

        {logs.length > 0 ? (
          <div className="space-y-2">
            {logs.map((log, idx) => (
              <div
                key={idx}
                className="flex items-start space-x-3 p-3 rounded-lg bg-surface-raised border border-surface-border text-xs font-mono"
              >
                <CheckCircle2 className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-cyan-400 font-bold">[{log.agent}]</span>
                    <span className="text-gray-400">&bull; {log.action}</span>
                    <span className="text-[10px] text-gray-500">
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-gray-300 mt-1 font-sans text-xs">{log.detail}</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-xs text-gray-500 font-mono py-4 text-center">
            No active agent traces. Run a workflow in the AI Workspace to inspect real-time inter-agent messaging.
          </div>
        )}
      </div>
    </div>
  );
}
