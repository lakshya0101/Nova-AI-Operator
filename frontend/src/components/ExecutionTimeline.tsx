"use client";

import React from "react";
import {
  Clock,
  CheckCircle2,
  AlertCircle,
  PlayCircle,
  ShieldCheck,
  Cpu,
  Inbox,
} from "lucide-react";
import { AgentLogItem } from "../lib/api";

interface ExecutionTimelineProps {
  logs?: AgentLogItem[];
}

export default function ExecutionTimeline({ logs = [] }: ExecutionTimelineProps) {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white flex items-center space-x-2">
          <Clock className="w-5 h-5 text-cyan-400" />
          <span>Execution Timeline &amp; Audit Trail</span>
        </h2>
        <p className="text-xs text-gray-400 mt-1">
          Chronological verified audit trace of agent reasoning, tool invocations, and state mutations.
        </p>
      </div>

      {/* Real Timeline List */}
      {logs.length > 0 ? (
        <div className="relative pl-6 border-l border-surface-border space-y-6 my-6">
          {logs.map((item, idx) => {
            const isSuccess = item.status === "success";
            const isWarning = item.status === "warning" || item.status === "waiting_approval";
            const isFailed = item.status === "failed";

            return (
              <div key={idx} className="relative group">
                {/* Timeline node */}
                <div
                  className={`absolute -left-[31px] top-1 w-4 h-4 rounded-full bg-surface border-2 flex items-center justify-center ${
                    isSuccess
                      ? "border-cyan-400"
                      : isWarning
                      ? "border-amber-400"
                      : "border-rose-400"
                  }`}
                >
                  <div
                    className={`w-1.5 h-1.5 rounded-full ${
                      isSuccess
                        ? "bg-cyan-400"
                        : isWarning
                        ? "bg-amber-400"
                        : "bg-rose-400"
                    }`}
                  ></div>
                </div>

                <div className="p-4 rounded-xl bg-surface border border-surface-border group-hover:border-cyan-500/40 transition-all">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-2">
                    <div className="flex items-center space-x-2">
                      <span className="font-bold text-sm text-white">{item.agent}</span>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-surface-raised text-cyan-400 border border-surface-border">
                        {item.action}
                      </span>
                    </div>
                    <span className="text-[11px] font-mono text-gray-500">
                      {new Date(item.timestamp).toLocaleTimeString()}
                    </span>
                  </div>

                  <p className="text-xs text-gray-300 font-sans leading-relaxed">
                    {item.detail}
                  </p>

                  <div className="mt-3 pt-2 border-t border-surface-border/60 flex items-center justify-between text-[10px] font-mono text-gray-500">
                    <span
                      className={`flex items-center space-x-1 ${
                        isSuccess
                          ? "text-emerald-400"
                          : isWarning
                          ? "text-amber-400"
                          : "text-rose-400"
                      }`}
                    >
                      <CheckCircle2 className="w-3 h-3" />
                      <span>{item.status.toUpperCase()} AUDIT EVENT</span>
                    </span>
                    <span>NOVA OPERATING SYSTEM</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="p-12 rounded-xl bg-surface border border-surface-border text-center space-y-3">
          <Inbox className="w-8 h-8 text-gray-600 mx-auto" />
          <h3 className="text-sm font-semibold text-white">No Execution Events Yet</h3>
          <p className="text-xs text-gray-400 max-w-md mx-auto">
            Execute a workflow in the AI Workspace to generate a live, verifiable multi-agent audit trail.
          </p>
        </div>
      )}
    </div>
  );
}
