"use client";

import { motion } from "framer-motion";
import { GlassCard } from "@/components/ui/glass-card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default function SettingsPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-white">Settings</h1>
        <p className="mt-1 text-zinc-400">Configure Nexus AI behavior and preferences</p>
      </motion.div>

      <div className="space-y-6">
        <GlassCard className="p-6">
          <h3 className="text-lg font-semibold text-white mb-4">API Configuration</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1.5">
                OpenAI API Key
              </label>
              <div className="flex gap-3">
                <input
                  type="password"
                  value="sk-...xxxx"
                  readOnly
                  className="flex-1 rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-zinc-300 font-mono"
                />
                <Button variant="secondary">Update</Button>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1.5">
                Model
              </label>
              <select className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white">
                <option>gpt-4o</option>
                <option>gpt-4o-mini</option>
                <option>gpt-4-turbo</option>
                <option>o1-preview</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1.5">
                Max Retries
              </label>
              <input
                type="number"
                defaultValue={5}
                min={1}
                max={10}
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white"
              />
            </div>
          </div>
        </GlassCard>

        <GlassCard className="p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Sandbox Configuration</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-white">Enable Network Access</p>
                <p className="text-xs text-zinc-400">Allow sandbox to make outbound network calls</p>
              </div>
              <Badge variant="neutral">Disabled</Badge>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-white">Memory Limit</p>
                <p className="text-xs text-zinc-400">Maximum memory allocation per execution</p>
              </div>
              <span className="text-sm text-zinc-300 font-mono">512 MB</span>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-white">Execution Timeout</p>
                <p className="text-xs text-zinc-400">Auto-kill after duration</p>
              </div>
              <span className="text-sm text-zinc-300 font-mono">30s</span>
            </div>
          </div>
        </GlassCard>

        <GlassCard className="p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Notifications</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-white">Success Notifications</p>
                <p className="text-xs text-zinc-400">Notify when all tests pass</p>
              </div>
              <Badge variant="success">Enabled</Badge>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-white">Failure Alerts</p>
                <p className="text-xs text-zinc-400">Notify when max retries reached</p>
              </div>
              <Badge variant="success">Enabled</Badge>
            </div>
          </div>
        </GlassCard>

        <div className="flex justify-end gap-3">
          <Button variant="ghost">Reset to Defaults</Button>
          <Button>Save Changes</Button>
        </div>
      </div>
    </div>
  );
}
