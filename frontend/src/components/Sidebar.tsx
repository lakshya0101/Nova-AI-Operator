"use client";

import React from "react";
import {
  Cpu,
  LayoutDashboard,
  Terminal,
  Bot,
  Brain,
  CheckSquare,
  Globe,
  Clock,
  Settings as SettingsIcon,
  Zap,
} from "lucide-react";
import { SystemHealth } from "../lib/api";

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  health: SystemHealth | null;
}

export default function Sidebar({ activeTab, setActiveTab, health }: SidebarProps) {
  const navItems = [
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { id: "workspace", label: "AI Workspace", icon: Terminal, badge: "Primary" },
    { id: "agents", label: "Agent Monitor", icon: Bot },
    { id: "memory", label: "Memory Explorer", icon: Brain },
    { id: "tasks", label: "Task Manager", icon: CheckSquare },
    { id: "research", label: "Web Research", icon: Globe },
    { id: "timeline", label: "Execution Timeline", icon: Clock },
  ];

  return (
    <aside className="w-64 bg-surface border-r border-surface-border flex flex-col h-screen select-none">
      {/* Brand Header */}
      <div className="p-5 border-b border-surface-border flex items-center space-x-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
          <Cpu className="w-6 h-6 text-black stroke-[2.5]" />
        </div>
        <div>
          <div className="flex items-center space-x-1.5">
            <span className="font-extrabold text-lg tracking-wider text-white">NOVA</span>
            <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800">
              v2.0
            </span>
          </div>
          <p className="text-[11px] text-gray-400 font-medium">Personal AI Operating System</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="text-[10px] uppercase font-mono tracking-wider text-gray-500 px-3 pb-2">
          Control Center
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm"
                  : "text-gray-400 hover:text-gray-200 hover:bg-surface-raised"
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon className={`w-4 h-4 ${isActive ? "text-cyan-400" : "text-gray-400"}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-300">
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* System Status Footer */}
      <div className="p-4 border-t border-surface-border bg-surface-raised/40">
        <div className="flex items-center justify-between text-xs mb-2">
          <span className="text-gray-400 flex items-center space-x-1.5">
            <Zap className="w-3.5 h-3.5 text-cyan-400" />
            <span>NVIDIA Nemotron</span>
          </span>
          <span className="flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="text-[11px] text-emerald-400 font-mono">READY</span>
          </span>
        </div>
        <div className="text-[10px] font-mono text-gray-500 truncate">
          Engine: Nebius Token Factory
        </div>
        <div className="text-[10px] font-mono text-gray-500 truncate">
          Tools: MCP Streamable HTTP
        </div>
      </div>
    </aside>
  );
}

