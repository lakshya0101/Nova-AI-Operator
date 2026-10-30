"use client";

import React, { useState } from "react";
import {
  CheckSquare,
  Plus,
  Trash2,
  Clock,
  AlertCircle,
  CheckCircle2,
  Calendar,
  Filter,
} from "lucide-react";
import { Task, createTask, updateTaskStatus, deleteTask } from "../lib/api";

interface TaskManagerProps {
  tasks: Task[];
  onRefresh: () => void;
}

export default function TaskManager({ tasks, onRefresh }: TaskManagerProps) {
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [priorityFilter, setPriorityFilter] = useState<string>("all");
  const [showAddModal, setShowAddModal] = useState(false);

  // New task form state
  const [newTitle, setNewTitle] = useState("");
  const [newDesc, setNewDesc] = useState("");
  const [newPriority, setNewPriority] = useState("medium");
  const [newDueDate, setNewDueDate] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    setIsSubmitting(true);
    try {
      await createTask({
        title: newTitle,
        description: newDesc,
        priority: newPriority,
        due_date: newDueDate ? new Date(newDueDate).toISOString() : undefined,
      });
      setShowAddModal(false);
      setNewTitle("");
      setNewDesc("");
      onRefresh();
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleToggleStatus = async (task: Task) => {
    const nextStatus =
      task.status === "completed"
        ? "pending"
        : task.status === "pending"
        ? "in_progress"
        : "completed";
    try {
      await updateTaskStatus(task.id, nextStatus);
      onRefresh();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteTask(id);
      onRefresh();
    } catch (err) {
      console.error(err);
    }
  };

  const filteredTasks = tasks.filter((t) => {
    if (statusFilter !== "all" && t.status !== statusFilter) return false;
    if (priorityFilter !== "all" && t.priority !== priorityFilter) return false;
    return true;
  });

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case "urgent":
        return "bg-rose-950/60 text-rose-400 border-rose-800";
      case "high":
        return "bg-amber-950/60 text-amber-400 border-amber-800";
      case "medium":
        return "bg-blue-950/60 text-blue-400 border-blue-800";
      default:
        return "bg-gray-800 text-gray-400 border-gray-700";
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <CheckSquare className="w-5 h-5 text-blue-400" />
            <span>Persistent Action Tasks</span>
          </h2>
          <p className="text-xs text-gray-400 mt-1">
            Track, prioritize, and manage actions managed by NOVA operator and MCP tools.
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="inline-flex items-center space-x-2 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-lg shadow-blue-600/20 transition-all self-start md:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>New Action Task</span>
        </button>
      </div>

      {/* Filter Toolbar */}
      <div className="p-4 rounded-xl bg-surface border border-surface-border flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-gray-500 font-mono">Status:</span>
          {["all", "pending", "in_progress", "completed"].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-3 py-1 rounded-md transition-all ${
                statusFilter === st
                  ? "bg-blue-500/20 text-blue-300 border border-blue-500/40"
                  : "text-gray-400 hover:text-white bg-surface-raised"
              }`}
            >
              {st.replace("_", " ")}
            </button>
          ))}
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <span className="text-gray-500 font-mono">Priority:</span>
          {["all", "urgent", "high", "medium", "low"].map((pr) => (
            <button
              key={pr}
              onClick={() => setPriorityFilter(pr)}
              className={`px-2.5 py-1 rounded-md transition-all ${
                priorityFilter === pr
                  ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40"
                  : "text-gray-400 hover:text-white bg-surface-raised"
              }`}
            >
              {pr}
            </button>
          ))}
        </div>
      </div>

      {/* Tasks List */}
      <div className="space-y-3">
        {filteredTasks.map((task) => (
          <div
            key={task.id}
            className="p-4 rounded-xl bg-surface border border-surface-border hover:border-surface-border/80 flex items-start justify-between gap-4 transition-all group"
          >
            <div className="flex items-start space-x-3.5">
              <button
                onClick={() => handleToggleStatus(task)}
                className={`mt-0.5 w-5 h-5 rounded border flex items-center justify-center transition-colors ${
                  task.status === "completed"
                    ? "bg-emerald-500 border-emerald-500 text-black"
                    : task.status === "in_progress"
                    ? "bg-blue-500/20 border-blue-400 text-blue-400"
                    : "border-gray-600 hover:border-cyan-400"
                }`}
                title="Toggle Task Status"
              >
                {task.status === "completed" && <CheckCircle2 className="w-4 h-4" />}
                {task.status === "in_progress" && <Clock className="w-3.5 h-3.5" />}
              </button>

              <div>
                <div className="flex items-center space-x-2">
                  <span
                    className={`font-semibold text-sm ${
                      task.status === "completed" ? "line-through text-gray-500" : "text-white"
                    }`}
                  >
                    {task.title}
                  </span>
                  <span
                    className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded border ${getPriorityBadge(
                      task.priority
                    )}`}
                  >
                    {task.priority}
                  </span>
                </div>
                {task.description && (
                  <p className="text-xs text-gray-400 mt-1 leading-relaxed">
                    {task.description}
                  </p>
                )}
                {task.due_date && (
                  <div className="flex items-center space-x-1.5 mt-2 text-[11px] font-mono text-gray-500">
                    <Calendar className="w-3.5 h-3.5 text-cyan-400" />
                    <span>Due: {new Date(task.due_date).toLocaleDateString()}</span>
                  </div>
                )}
              </div>
            </div>

            <button
              onClick={() => handleDelete(task.id)}
              className="opacity-0 group-hover:opacity-100 p-1.5 text-gray-500 hover:text-rose-400 transition-opacity"
              title="Delete Task"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        ))}

        {filteredTasks.length === 0 && (
          <div className="text-center py-12 text-gray-500 text-xs font-mono">
            No action tasks match the current filter criteria.
          </div>
        )}
      </div>

      {/* Add Task Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-surface border border-surface-border rounded-2xl p-6 max-w-lg w-full shadow-2xl">
            <h3 className="text-base font-bold text-white mb-4 flex items-center space-x-2">
              <CheckSquare className="w-5 h-5 text-blue-400" />
              <span>Create Action Task</span>
            </h3>

            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-xs font-mono text-gray-400 mb-1">Title</label>
                <input
                  type="text"
                  required
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  placeholder="e.g. Technical interview preparation"
                  className="w-full bg-surface-raised border border-surface-border rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-gray-400 mb-1">Description</label>
                <textarea
                  rows={2}
                  value={newDesc}
                  onChange={(e) => setNewDesc(e.target.value)}
                  placeholder="Task details and milestones..."
                  className="w-full bg-surface-raised border border-surface-border rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-mono text-gray-400 mb-1">Priority</label>
                  <select
                    value={newPriority}
                    onChange={(e) => setNewPriority(e.target.value)}
                    className="w-full bg-surface-raised border border-surface-border rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-mono text-gray-400 mb-1">Due Date</label>
                  <input
                    type="date"
                    value={newDueDate}
                    onChange={(e) => setNewDueDate(e.target.value)}
                    className="w-full bg-surface-raised border border-surface-border rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500"
                  >
                  </input>
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-3 border-t border-surface-border">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-lg bg-surface-raised text-xs text-gray-300 hover:bg-surface-border"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold"
                >
                  {isSubmitting ? "Saving..." : "Create Task"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

