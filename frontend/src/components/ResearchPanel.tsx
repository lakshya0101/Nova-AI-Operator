"use client";

import React, { useState } from "react";
import {
  Globe,
  Search,
  ExternalLink,
  BookOpen,
  Sparkles,
  ShieldCheck,
} from "lucide-react";
import { ResearchResponse, executeResearch } from "../lib/api";

export default function ResearchPanel() {
  const [query, setQuery] = useState(
    "NVIDIA Nemotron AI agent developments, Nebius Token Factory inference, MCP integration"
  );
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ResearchResponse | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setIsLoading(true);
    try {
      const data = await executeResearch(query);
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white flex items-center space-x-2">
          <Globe className="w-5 h-5 text-cyan-400" />
          <span>Tavily Real-Time Web Intelligence</span>
        </h2>
        <p className="text-xs text-gray-400 mt-1">
          Perform live web research, verify citations, and extract structured evidence for multi-agent workflows.
        </p>
      </div>

      {/* Query Bar */}
      <div className="p-5 rounded-xl bg-surface border border-surface-border">
        <form onSubmit={handleSearch} className="flex gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search topic or research question (e.g. NVIDIA Nemotron AI infrastructure, AI interview preparation)..."
              className="w-full bg-surface-raised border border-surface-border rounded-lg pl-9 pr-4 py-2.5 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500"
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="px-5 py-2.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-black text-xs font-semibold shadow-lg shadow-cyan-500/20 transition-all flex items-center space-x-2"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>{isLoading ? "Researching..." : "Execute Research"}</span>
          </button>
        </form>
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* Executive Answer */}
          <div className="p-6 rounded-xl bg-surface border border-surface-border">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-mono uppercase tracking-wider text-cyan-400 flex items-center space-x-2">
                <BookOpen className="w-4 h-4" />
                <span>Synthesized Web Intelligence</span>
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
                {result.is_live_tavily ? "Live Tavily Web Index" : "Tavily Intelligence Engine"}
              </span>
            </div>
            <p className="text-sm text-gray-200 leading-relaxed font-sans">
              {result.answer || result.summary}
            </p>
          </div>

          {/* Sources Grid */}
          <div>
            <h3 className="text-xs font-mono uppercase tracking-wider text-gray-400 mb-3">
              Verified Source Citations ({result.sources.length})
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {result.sources.map((src, i) => (
                <div
                  key={i}
                  className="p-5 rounded-xl bg-surface border border-surface-border flex flex-col justify-between hover:border-cyan-500/40 transition-all"
                >
                  <div>
                    <div className="flex items-start justify-between mb-2">
                      <span className="text-xs font-bold text-white line-clamp-1">{src.title}</span>
                      {src.score && (
                        <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800">
                          Match: {Math.round(src.score * 100)}%
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-gray-400 leading-relaxed line-clamp-3">
                      {src.content}
                    </p>
                  </div>

                  <a
                    href={src.url}
                    target="_blank"
                    rel="noreferrer"
                    className="mt-4 pt-3 border-t border-surface-border flex items-center justify-between text-xs text-cyan-400 hover:text-cyan-300 font-mono"
                  >
                    <span className="truncate max-w-[280px]">{src.url}</span>
                    <ExternalLink className="w-3.5 h-3.5 flex-shrink-0" />
                  </a>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

