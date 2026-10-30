"use client";

import React, { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import DashboardOverview from "../components/DashboardOverview";
import Workspace from "../components/Workspace";
import AgentMonitor from "../components/AgentMonitor";
import MemoryExplorer from "../components/MemoryExplorer";
import TaskManager from "../components/TaskManager";
import ResearchPanel from "../components/ResearchPanel";
import ExecutionTimeline from "../components/ExecutionTimeline";
import { AlertCircle } from "lucide-react";
import {
  fetchHealth,
  fetchTasks,
  fetchMemories,
  SystemHealth,
  Task,
  MemoryItem,
  AgentLogItem,
} from "../lib/api";

export default function Home() {
  const [activeTab, setActiveTab] = useState<string>("dashboard");
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [workspaceInitialPrompt, setWorkspaceInitialPrompt] = useState<string>("");
  const [recentLogs, setRecentLogs] = useState<AgentLogItem[]>([]);
  const [backendError, setBackendError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      const h = await fetchHealth();
      setHealth(h);
      setBackendError(null);
    } catch {
      setHealth(null);
      setBackendError("NOVA backend service is offline at http://127.0.0.1:8000. Launch uvicorn to activate live integrations.");
      return;
    }

    try {
      const t = await fetchTasks();
      setTasks(t.tasks);
    } catch (e: any) {
      console.error("Failed to load tasks:", e);
    }

    try {
      const m = await fetchMemories();
      setMemories(m);
    } catch (e: any) {
      console.error("Failed to load memories:", e);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleRunQuickDemo = (prompt: string) => {
    setWorkspaceInitialPrompt(prompt);
    setActiveTab("workspace");
  };

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      {/* Sidebar */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} health={health} />

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col h-screen overflow-y-auto">
        {/* Top Operational Bar */}
        <header className="h-14 border-b border-surface-border bg-surface/50 backdrop-blur-md px-8 flex items-center justify-between sticky top-0 z-30">
          <div className="flex items-center space-x-3">
            <span className="text-xs font-mono text-gray-400 uppercase tracking-wider">
              Mode: Autonomous Personal Operator
            </span>
            <span className="text-gray-600">&bull;</span>
            <span className="text-xs font-mono text-cyan-400">
              Active Context: Nebius x NVIDIA 2026
            </span>
          </div>

          <div className="flex items-center space-x-4 text-xs font-mono">
            <div className="flex items-center space-x-2">
              <span
                className={`w-2 h-2 rounded-full ${
                  health ? "bg-emerald-400" : "bg-rose-400 animate-ping"
                }`}
              ></span>
              <span className="text-gray-300">
                {health ? "Backend Connected (Port 8000)" : "Backend Disconnected"}
              </span>
            </div>
            {health && (
              <div className="flex items-center space-x-2">
                <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
                <span className="text-gray-300">
                  {health.nebius_configured ? "Nebius Live" : "Nemotron Simulated"}
                </span>
              </div>
            )}
          </div>
        </header>

        {/* Backend Warning Banner if unreachable */}
        {backendError && (
          <div className="bg-rose-950/80 border-b border-rose-800 text-rose-200 px-8 py-2.5 text-xs flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-400" />
            <span>{backendError}</span>
          </div>
        )}

        {/* View Switcher Container */}
        <div className="p-8 flex-1">
          {activeTab === "dashboard" && (
            <DashboardOverview
              health={health}
              tasks={tasks}
              memories={memories}
              onNavigate={setActiveTab}
              onRunQuickDemo={handleRunQuickDemo}
            />
          )}

          {activeTab === "workspace" && (
            <Workspace
              initialPrompt={workspaceInitialPrompt}
              onRefreshData={loadData}
              onLogsUpdate={(logs) => setRecentLogs(logs)}
            />
          )}

          {activeTab === "agents" && <AgentMonitor logs={recentLogs} />}

          {activeTab === "memory" && (
            <MemoryExplorer memories={memories} onRefresh={loadData} />
          )}

          {activeTab === "tasks" && <TaskManager tasks={tasks} onRefresh={loadData} />}

          {activeTab === "research" && <ResearchPanel />}

          {activeTab === "timeline" && <ExecutionTimeline logs={recentLogs} />}
        </div>
      </main>
    </div>
  );
}
