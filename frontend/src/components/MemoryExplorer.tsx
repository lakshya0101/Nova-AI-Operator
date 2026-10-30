"use client";

import React, { useState } from "react";
import {
  Brain,
  Search,
  Plus,
  Trash2,
  Tag,
  Clock,
  Sparkles,
  Filter,
} from "lucide-react";
import {
  MemoryItem,
  createMemory,
  deleteMemory,
  searchMemories,
} from "../lib/api";

interface MemoryExplorerProps {
  memories: MemoryItem[];
  onRefresh: () => void;
}

export default function MemoryExplorer({ memories, onRefresh }: MemoryExplorerProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState<MemoryItem[] | null>(null);
  const [showAddModal, setShowAddModal] = useState(false);

  // New memory form state
  const [newTitle, setNewTitle] = useState("");
  const [newContent, setNewContent] = useState("");
  const [newCategory, setNewCategory] = useState("profile");
  const [newTags, setNewTags] = useState("");
  const [newImportance, setNewImportance] = useState(1.5);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const categories = [
    { id: "all", label: "All Contexts" },
    { id: "profile", label: "Profile" },
    { id: "decision", label: "Decisions" },
    { id: "project", label: "Projects" },
    { id: "learned", label: "Learned Patterns" },
    { id: "workflow", label: "Workflows" },
  ];

  const handleSemanticSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      setSearchResults(null);
      return;
    }
    setIsSearching(true);
    try {
      const results = await searchMemories(searchQuery);
      setSearchResults(results);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSearching(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newContent.trim()) return;
    setIsSubmitting(true);
    try {
      await createMemory({
        title: newTitle,
        content: newContent,
        category: newCategory,
        tags: newTags,
        importance: Number(newImportance),
      });
      setShowAddModal(false);
      setNewTitle("");
      setNewContent("");
      setNewTags("");
      onRefresh();
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteMemory(id);
      onRefresh();
      if (searchResults) {
        setSearchResults((prev) => (prev ? prev.filter((m) => m.id !== id) : null));
      }
    } catch (err) {
      console.error(err);
    }
  };

  const displayMemories =
    searchResults !== null
      ? searchResults
      : selectedCategory === "all"
      ? memories
      : memories.filter((m) => m.category === selectedCategory);

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header & Search */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <Brain className="w-5 h-5 text-purple-400" />
            <span>Persistent Semantic Memory Engine</span>
          </h2>
          <p className="text-xs text-gray-400 mt-1">
            Embeddings-indexed personal knowledge store powering context-aware reasoning.
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="inline-flex items-center space-x-2 px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold shadow-lg shadow-purple-600/20 transition-all self-start md:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>Record New Memory</span>
        </button>
      </div>

      {/* Search Bar & Category Filter */}
      <div className="p-4 rounded-xl bg-surface border border-surface-border space-y-4">
        <form onSubmit={handleSemanticSearch} className="flex gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Semantic search (e.g. 'interview guidelines', 'evening preferences', 'hackathon project')..."
              className="w-full bg-surface-raised border border-surface-border rounded-lg pl-9 pr-4 py-2 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-purple-500"
            />
          </div>
          <button
            type="submit"
            disabled={isSearching}
            className="px-4 py-2 rounded-lg bg-surface-raised hover:bg-surface-border text-xs font-mono text-purple-300 border border-purple-500/30 transition-all flex items-center space-x-1.5"
          >
            <Sparkles className="w-3.5 h-3.5 text-purple-400" />
            <span>{isSearching ? "Searching..." : "Cosine Match"}</span>
          </button>
          {searchResults !== null && (
            <button
              type="button"
              onClick={() => {
                setSearchResults(null);
                setSearchQuery("");
              }}
              className="px-3 py-2 rounded-lg bg-surface-raised text-xs text-gray-400 hover:text-white"
            >
              Clear
            </button>
          )}
        </form>

        {/* Categories */}
        <div className="flex flex-wrap gap-2 pt-2 border-t border-surface-border">
          {categories.map((c) => (
            <button
              key={c.id}
              onClick={() => {
                setSelectedCategory(c.id);
                setSearchResults(null);
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                selectedCategory === c.id && searchResults === null
                  ? "bg-purple-500/20 text-purple-300 border border-purple-500/40"
                  : "text-gray-400 hover:text-gray-200 bg-surface-raised"
              }`}
            >
              {c.label}
            </button>
          ))}
        </div>
      </div>

      {/* Memory Items Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {displayMemories.map((mem) => (
          <div
            key={mem.id}
            className="p-5 rounded-xl bg-surface border border-surface-border flex flex-col justify-between hover:border-purple-500/40 transition-all group"
          >
            <div>
              <div className="flex items-start justify-between mb-2">
                <span className="text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 rounded bg-purple-950/60 text-purple-300 border border-purple-800">
                  {mem.category}
                </span>
                <div className="flex items-center space-x-2">
                  {mem.similarity_score !== undefined && mem.similarity_score !== null && (
                    <span className="text-[10px] font-mono text-cyan-400">
                      Score: {mem.similarity_score}
                    </span>
                  )}
                  <button
                    onClick={() => handleDelete(mem.id)}
                    className="opacity-0 group-hover:opacity-100 p-1 text-gray-500 hover:text-rose-400 transition-opacity"
                    title="Delete Memory"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>

              <h3 className="font-bold text-white text-sm mb-1.5">{mem.title}</h3>
              <p className="text-xs text-gray-300 leading-relaxed">{mem.content}</p>

              {mem.tags && (
                <div className="flex flex-wrap gap-1 mt-3">
                  {mem.tags.split(",").map((tag, idx) => (
                    <span
                      key={idx}
                      className="text-[10px] text-gray-400 bg-surface-raised px-2 py-0.5 rounded border border-surface-border"
                    >
                      #{tag.trim()}
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div className="mt-4 pt-3 border-t border-surface-border flex items-center justify-between text-[11px] text-gray-500 font-mono">
              <span>Source: {mem.source}</span>
              <span>Weight: {mem.importance}x</span>
            </div>
          </div>
        ))}
      </div>

      {displayMemories.length === 0 && (
        <div className="text-center py-12 text-gray-500 text-xs font-mono">
          No memory records match the selected query.
        </div>
      )}

      {/* Add Memory Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-surface border border-surface-border rounded-2xl p-6 max-w-lg w-full shadow-2xl">
            <h3 className="text-base font-bold text-white mb-4 flex items-center space-x-2">
              <Brain className="w-5 h-5 text-purple-400" />
              <span>Record Contextual Memory</span>
            </h3>

            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-xs font-mono text-gray-400 mb-1">Title</label>
                <input
                  type="text"
                  required
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  placeholder="e.g. Evening routine preference"
                  className="w-full bg-surface-raised border border-surface-border rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500"
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-gray-400 mb-1">Category</label>
                <select
                  value={newCategory}
                  onChange={(e) => setNewCategory(e.target.value)}
                  className="w-full bg-surface-raised border border-surface-border rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500"
                >
                  <option value="profile">Profile</option>
                  <option value="decision">Decision</option>
                  <option value="project">Project</option>
                  <option value="learned">Learned Context</option>
                  <option value="workflow">Workflow</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-mono text-gray-400 mb-1">Content Context</label>
                <textarea
                  required
                  rows={3}
                  value={newContent}
                  onChange={(e) => setNewContent(e.target.value)}
                  placeholder="Describe personal knowledge, rule, or preference..."
                  className="w-full bg-surface-raised border border-surface-border rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500"
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-gray-400 mb-1">Tags (comma separated)</label>
                <input
                  type="text"
                  value={newTags}
                  onChange={(e) => setNewTags(e.target.value)}
                  placeholder="evening,interview,routine"
                  className="w-full bg-surface-raised border border-surface-border rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500"
                />
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
                  className="px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold"
                >
                  {isSubmitting ? "Encoding..." : "Save Memory"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

