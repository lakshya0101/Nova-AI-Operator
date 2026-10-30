"use client";

import React, { useState } from "react";
import {
  Send,
  Play,
  Eye,
  CheckCircle2,
  AlertCircle,
  Clock,
  ShieldCheck,
  Brain,
  Globe,
  Bot,
  ExternalLink,
  ChevronDown,
  ChevronUp,
  RotateCcw,
  Sparkles,
} from "lucide-react";
import {
  PlanResponse,
  runOrchestration,
  PlanStep,
  ExecutionResult,
} from "../lib/api";

interface WorkspaceProps {
  initialPrompt?: string;
  onRefreshData: () => void;
  onLogsUpdate?: (logs: any[]) => void;
}

export default function Workspace({
  initialPrompt = "",
  onRefreshData,
  onLogsUpdate,
}: WorkspaceProps) {
  const [instruction, setInstruction] = useState(
    initialPrompt ||
      "Organize my evening. Prioritize my unfinished tasks and leave time for interview preparation."
  );
  const [isLoading, setIsLoading] = useState(false);
  const [planResult, setPlanResult] = useState<PlanResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expandedSteps, setExpandedSteps] = useState<Record<number, boolean>>({});

  const handleRun = async (dryRun: boolean, approve: boolean) => {
    if (!instruction.trim()) return;
    setIsLoading(true);
    setError(null);
    try {
      const data = await runOrchestration(instruction, dryRun, approve);
      setPlanResult(data);
      if (data.agent_logs && onLogsUpdate) {
        onLogsUpdate(data.agent_logs);
      }
      onRefreshData();
    } catch (err: any) {
      setError(err.message || "Execution request failed");
    } finally {
      setIsLoading(false);
    }
  };

  const toggleStep = (idx: number) => {
    setExpandedSteps((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  // Determine if there are steps awaiting approval
  const hasPendingApproval =
    planResult &&
    Object.values(planResult.step_results).some(
      (r) => r.status === "skipped" && r.detail?.includes("requires explicit approval")
    );

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Goal Entry Card */}
      <div className="rounded-2xl bg-surface border border-surface-border p-6 shadow-xl relative overflow-hidden">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
            <h2 className="text-sm font-mono uppercase tracking-wider text-white">
              AI Command Terminal
            </h2>
          </div>
          <div className="text-xs text-gray-400 font-mono flex items-center space-x-2">
            <span>Powered by</span>
            <span className="text-cyan-400 font-semibold">NVIDIA Nemotron Super</span>
          </div>
        </div>

        <div className="relative">
          <textarea
            value={instruction}
            onChange={(e) => setInstruction(e.target.value)}
            rows={3}
            placeholder="State your goal in natural language (e.g. Organize my evening, research NVIDIA AI developments, prepare schedule)..."
            className="w-full bg-surface-raised border border-surface-border rounded-xl p-4 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-cyan-500 transition-colors font-sans"
          />
        </div>

        {/* Action Controls */}
        <div className="mt-4 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center space-x-2 text-xs text-gray-400">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Human-in-the-Loop Safe Mode Active</span>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={() => handleRun(true, false)}
              disabled={isLoading || !instruction.trim()}
              className="inline-flex items-center space-x-2 px-4 py-2 rounded-lg bg-surface-raised hover:bg-surface-border text-gray-200 border border-surface-border text-xs font-medium transition-all disabled:opacity-50"
            >
              <Eye className="w-3.5 h-3.5 text-cyan-400" />
              <span>Preview Plan (Dry Run)</span>
            </button>
            <button
              onClick={() => handleRun(false, true)}
              disabled={isLoading || !instruction.trim()}
              className="inline-flex items-center space-x-2 px-5 py-2 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-black text-xs font-semibold shadow-lg shadow-cyan-500/20 transition-all disabled:opacity-50"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>Execute Workflow (Approved)</span>
            </button>
          </div>
        </div>
      </div>

      {/* Loading Indicator */}
      {isLoading && (
        <div className="p-8 rounded-xl bg-surface border border-surface-border flex flex-col items-center justify-center space-y-3">
          <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
          <div className="text-sm font-mono text-cyan-400 animate-pulse">
            NOVA Multi-Agent Swarm Orchestrating...
          </div>
          <div className="text-xs text-gray-500">
            Consulting Memory &bull; Tavily Web Research &bull; Nemotron Strategic Planning
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-800 text-rose-300 text-sm flex items-center space-x-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Orchestration Results Display */}
      {planResult && !isLoading && (
        <div className="space-y-6">
          {/* Summary Header */}
          <div className="p-5 rounded-xl bg-surface border border-surface-border flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="text-xs font-mono text-cyan-400 uppercase tracking-wider mb-1">
                Interpreted Goal &bull; {planResult.request_id.slice(0, 8)}
              </div>
              <h3 className="text-base font-semibold text-white">
                &ldquo;{planResult.interpreted_intent}&rdquo;
              </h3>
              <p className="text-xs text-gray-400 mt-1">{planResult.final_summary}</p>
            </div>

            <div className="flex items-center space-x-4 text-xs font-mono text-gray-400 bg-surface-raised px-4 py-2.5 rounded-lg border border-surface-border">
              <div>
                <span className="text-gray-500">Model:</span>{" "}
                <span className="text-cyan-400 font-medium">
                  {planResult.model_used || "Nemotron Super"}
                </span>
              </div>
              {planResult.total_latency_ms && (
                <div>
                  <span className="text-gray-500">Latency:</span>{" "}
                  <span className="text-white">{planResult.total_latency_ms}ms</span>
                </div>
              )}
            </div>
          </div>

          {/* Pending Approval Callout Banner */}
          {hasPendingApproval && (
            <div className="p-5 rounded-xl bg-amber-950/30 border border-amber-600/50 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-lg shadow-amber-950/20">
              <div className="flex items-start space-x-3">
                <AlertCircle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-semibold text-amber-300">
                    Human-in-the-Loop Approval Required
                  </h4>
                  <p className="text-xs text-amber-200/80 mt-0.5">
                    State mutation steps are held. Review proposed changes below and confirm execution.
                  </p>
                </div>
              </div>
              <button
                onClick={() => handleRun(false, true)}
                className="px-4 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-black font-semibold text-xs transition-colors shadow"
              >
                Approve &amp; Execute Mutations
              </button>
            </div>
          )}

          {/* Memory & Research Context Panels */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Contextual Memory Retrieved */}
            <div className="p-4 rounded-xl bg-surface border border-surface-border">
              <div className="flex items-center space-x-2 text-xs font-mono text-purple-400 mb-3">
                <Brain className="w-4 h-4" />
                <span className="uppercase tracking-wider">Contextual Memory Engine</span>
              </div>
              {planResult.memory_context && planResult.memory_context.length > 0 ? (
                <div className="space-y-2">
                  {planResult.memory_context.map((m, i) => (
                    <div key={i} className="p-2.5 rounded bg-surface-raised border border-surface-border text-xs">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-white">{m.title}</span>
                        <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800">
                          {m.category}
                        </span>
                      </div>
                      <p className="text-gray-400 mt-1 text-[11px] leading-relaxed">{m.content}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-gray-500">No prior context records required for this task.</p>
              )}
            </div>

            {/* Tavily Web Research Evidence */}
            <div className="p-4 rounded-xl bg-surface border border-surface-border">
              <div className="flex items-center space-x-2 text-xs font-mono text-cyan-400 mb-3">
                <Globe className="w-4 h-4" />
                <span className="uppercase tracking-wider">Tavily Web Research Evidence</span>
              </div>
              {planResult.research_evidence ? (
                <div className="space-y-2">
                  <div className="p-2.5 rounded bg-surface-raised border border-surface-border text-xs">
                    <p className="text-gray-300 font-medium mb-2">
                      {planResult.research_evidence.answer || planResult.research_evidence.summary}
                    </p>
                    <div className="space-y-1.5 pt-2 border-t border-surface-border">
                      {planResult.research_evidence.sources.slice(0, 2).map((s, idx) => (
                        <a
                          key={idx}
                          href={s.url}
                          target="_blank"
                          rel="noreferrer"
                          className="flex items-center justify-between p-1.5 rounded hover:bg-black/30 text-[11px] text-cyan-400 hover:text-cyan-300"
                        >
                          <span className="truncate max-w-[280px]">{s.title}</span>
                          <ExternalLink className="w-3 h-3 flex-shrink-0" />
                        </a>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-xs text-gray-500">Local orchestration; no web search requested.</p>
              )}
            </div>
          </div>

          {/* Generated Execution Plan Steps */}
          <div className="p-6 rounded-xl bg-surface border border-surface-border">
            <h3 className="text-sm font-mono uppercase tracking-wider text-white mb-4 flex items-center space-x-2">
              <Bot className="w-4 h-4 text-cyan-400" />
              <span>Multi-Step Execution Plan ({planResult.plan.length} Steps)</span>
            </h3>

            <div className="space-y-3">
              {planResult.plan.map((step, idx) => {
                const result = planResult.step_results[String(idx)] || planResult.step_results[idx];
                const isExpanded = !!expandedSteps[idx];
                const isSkipped = result?.status === "skipped";
                const isSuccess = result?.status === "success";
                const isFailed = result?.status === "failed";

                return (
                  <div
                    key={idx}
                    className="p-4 rounded-xl bg-surface-raised border border-surface-border hover:border-surface-border/80 transition-all"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-3">
                        <div className="flex items-center justify-center w-6 h-6 rounded-full bg-black/40 text-xs font-mono text-cyan-400 border border-surface-border mt-0.5">
                          {idx + 1}
                        </div>
                        <div>
                          <div className="flex items-center space-x-2">
                            <span className="font-semibold text-sm text-white">{step.name}</span>
                            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-black/50 text-gray-400 border border-surface-border">
                              tool: {step.tool}
                            </span>
                            {step.requires_approval && (
                              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-amber-950 text-amber-400 border border-amber-800">
                                Requires Approval
                              </span>
                            )}
                          </div>
                          <p className="text-xs text-gray-400 mt-1">
                            Expected: {step.expected_result}
                          </p>
                        </div>
                      </div>

                      {/* Status Badge */}
                      <div className="flex items-center space-x-2">
                        {isSuccess && (
                          <span className="inline-flex items-center space-x-1 px-2.5 py-1 rounded-full text-xs font-mono bg-emerald-950/60 text-emerald-400 border border-emerald-800">
                            <CheckCircle2 className="w-3.5 h-3.5" />
                            <span>SUCCESS</span>
                          </span>
                        )}
                        {isSkipped && (
                          <span className="inline-flex items-center space-x-1 px-2.5 py-1 rounded-full text-xs font-mono bg-amber-950/60 text-amber-400 border border-amber-800">
                            <Clock className="w-3.5 h-3.5" />
                            <span>SKIPPED</span>
                          </span>
                        )}
                        {isFailed && (
                          <span className="inline-flex items-center space-x-1 px-2.5 py-1 rounded-full text-xs font-mono bg-rose-950/60 text-rose-400 border border-rose-800">
                            <AlertCircle className="w-3.5 h-3.5" />
                            <span>FAILED</span>
                          </span>
                        )}
                        <button
                          onClick={() => toggleStep(idx)}
                          className="p-1 rounded text-gray-400 hover:text-white"
                        >
                          {isExpanded ? (
                            <ChevronUp className="w-4 h-4" />
                          ) : (
                            <ChevronDown className="w-4 h-4" />
                          )}
                        </button>
                      </div>
                    </div>

                    {/* Collapsible Step Detail / Output */}
                    {isExpanded && (
                      <div className="mt-3 pt-3 border-t border-surface-border text-xs space-y-2">
                        {result?.detail && (
                          <div className="text-gray-300">
                            <span className="text-gray-500 font-mono">Detail:</span>{" "}
                            {result.detail}
                          </div>
                        )}
                        {step.arguments && Object.keys(step.arguments).length > 0 && (
                          <div>
                            <span className="text-gray-500 font-mono">Arguments:</span>
                            <pre className="mt-1 p-2 rounded bg-black/60 text-[11px] font-mono text-cyan-300 overflow-x-auto">
                              {JSON.stringify(step.arguments, null, 2)}
                            </pre>
                          </div>
                        )}
                        {result?.output && (
                          <div>
                            <span className="text-gray-500 font-mono">Execution Output:</span>
                            <pre className="mt-1 p-2 rounded bg-black/60 text-[11px] font-mono text-emerald-300 overflow-x-auto">
                              {JSON.stringify(result.output, null, 2)}
                            </pre>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

