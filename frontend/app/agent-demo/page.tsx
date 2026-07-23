'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { GlassCard } from '@/components/ui/glass-card';
import { Loader2, CheckCircle2, XCircle, Zap, RefreshCw, Brain, Bot, Terminal, Code } from 'lucide-react';

interface Step {
  id: string;
  label: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  completed: boolean;
}

const steps: Step[] = [
  { id: 'entering', label: 'Enter Problem', description: 'User enters: "Reverse a Linked List."', icon: Terminal, completed: false },
  { id: 'generating', label: 'Generating', description: 'AI is creating initial solution...', icon: Brain, completed: false },
  { id: 'testing', label: 'Running Tests', description: 'Executing test suite in sandbox...', icon: Zap, completed: false },
  { id: 'failed', label: 'Tests Failed', description: '3 tests failed - analyzing errors...', icon: XCircle, completed: false },
  { id: 'analyzing', label: 'Analyzing', description: 'Finding root cause of failures...', icon: Brain, completed: false },
  { id: 'repairing', label: 'Repairing', description: 'Applying targeted fixes...', icon: Bot, completed: false },
  { id: 'rerunning', label: 'Running Again', description: 'Re-executing tests with fixes...', icon: RefreshCw, completed: false },
  { id: 'success', label: 'Passed', description: 'All tests passed! Solution is ready.', icon: CheckCircle2, completed: false }
];

export default function AgentDemo() {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [showCode, setShowCode] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);

  const addLog = (message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, `[${timestamp}] ${message}`]);
  };

  const runDemo = async () => {
    setIsRunning(true);
    setCurrentStepIndex(0);
    setShowCode(false);
    setLogs([]);
    addLog('Starting Nexus AI Agent Demo');
    addLog('User input: "Reverse a Linked List."');

    // Step 1: User enters problem (already done)
    await new Promise(resolve => setTimeout(resolve, 1000));
    setCurrentStepIndex(1);
    addLog('Step 1: Problem received');

    // Step 2: Generating
    setCurrentStepIndex(2);
    addLog('Step 2: Generating initial solution with GPT-4o...');
    await new Promise(resolve => setTimeout(resolve, 2000));
    addLog('Generated linked list reversal algorithm');

    // Step 3: Running tests
    setCurrentStepIndex(3);
    addLog('Step 3: Running test suite in isolated sandbox...');
    await new Promise(resolve => setTimeout(resolve, 1500));
    addLog('Executing 5 unit tests...');

    // Step 4: Tests failed
    setCurrentStepIndex(4);
    addLog('Step 4: Test results:');
    addLog('  PASS test_empty_list');
    addLog('  PASS test_single_node');
    addLog('  FAIL test_two_nodes: Expected [2,1], got [1,2]');
    addLog('  FAIL test_three_nodes: Expected [3,2,1], got [1,2,3]');
    addLog('  FAIL test_palindrome: Expected [1,2,1], got [1,2,1] (but tail incorrect)');
    addLog('  PASS test_large_list');
    addLog('Results: 2/5 tests passed');
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Step 5: Analyzing
    setCurrentStepIndex(5);
    addLog('Step 5: Analyzing failures...');
    addLog('Pattern detected: Nodes are not being properly relinked');
    addLog('Root cause: Missing null termination in reversed list');
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Step 6: Repairing
    setCurrentStepIndex(6);
    addLog('Step 6: Applying targeted fix...');
    addLog('Added: current.next = null; after loop');
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Step 7: Running again
    setCurrentStepIndex(7);
    addLog('Step 7: Re-running test suite with fixes...');
    await new Promise(resolve => setTimeout(resolve, 1500));
    addLog('Executing 5 unit tests...');

    // Step 8: Success
    setCurrentStepIndex(8);
    addLog('Step 8: Test results:');
    addLog('  PASS test_empty_list');
    addLog('  PASS test_single_node');
    addLog('  PASS test_two_nodes');
    addLog('  PASS test_three_nodes');
    addLog('  PASS test_palindrome');
    addLog('  PASS test_large_list');
    addLog('Results: 5/5 tests passed');
    await new Promise(resolve => setTimeout(resolve, 2000));

    setShowCode(true);
    addLog('Demo completed successfully!');
  };

  const getStepStatus = (index: number): 'completed' | 'active' | 'pending' => {
    if (index < currentStepIndex) return 'completed';
    if (index === currentStepIndex) return 'active';
    return 'pending';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 to-gray-900 text-white p-6">
      <motion.h1
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="text-4xl font-bold text-center mb-8 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent"
      >
        Nexus AI Hackathon Demo
      </motion.h1>

      <motion.p
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="text-center text-gray-400 mb-12 max-w-2xl mx-auto"
      >
        Watch the autonomous agent solve: &quot;Reverse a Linked List.&quot;
      </motion.p>

      <div className="max-w-4xl mx-auto">
        {/* Progress Steps */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="space-y-4"
        >
          {steps.map((step, index) => {
            const status = getStepStatus(index);
            const isCompleted = status === 'completed';
            const isActive = status === 'active';

            return (
              <motion.div
                key={step.id}
                initial={{ x: isCompleted ? 0 : -20, opacity: isCompleted ? 1 : 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className={`flex items-center gap-4 py-3 px-4 rounded-lg border ${
                  isCompleted ? 'border-green-500/50 bg-green-500/10' : 
                  isActive ? 'border-blue-500/50 bg-blue-500/10' : 
                  'border-gray-700/50'
                }`}
              >
                <div className="flex-shrink-0 flex items-center justify-center w-10 h-10 rounded-full">
                  {isCompleted ? (
                    <CheckCircle2 className="h-5 w-5 text-green-400" />
                  ) : isActive ? (
                    <Loader2 className="h-5 w-5 text-blue-400 animate-spin" />
                  ) : (
                    <span className="text-gray-500">{index + 1}</span>
                  )}
                </div>
                <div className="flex-1 space-y-1">
                  <div className="flex items-center justify-between">
                    <h3 className={`${isActive ? 'font-bold text-white' : 'font-medium text-gray-300'}`}>
                      {step.label}
                    </h3>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${
                      isCompleted ? 'bg-green-500/20 text-green-400' : 
                      isActive ? 'bg-blue-500/20 text-blue-400' : 
                      'bg-gray-700/20 text-gray-400'
                    }`}>
                      {isCompleted ? 'Done' : isActive ? 'In Progress' : 'Pending'}
                    </span>
                  </div>
                  <p className="text-sm text-gray-400">{step.description}</p>
                </div>
              </motion.div>
            );
          })}
        </motion.div>

        {/* Code Preview */}
        {showCode && (
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="mt-8"
          >
            <GlassCard className="p-6">
              <h2 className="flex items-center gap-3 mb-4">
                <Code className="h-5 w-5 text-green-400" /> Final Solution
              </h2>
              <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                <pre className="text-sm font-mono text-green-400">
{`function reverseLinkedList(head) {
  let prev = null;
  let current = head;
  
  while (current !== null) {
    const nextTemp = current.next;
    current.next = prev;
    prev = current;
    current = nextTemp;
  }
  
  return prev;
}`}
                </pre>
              </div>
            </GlassCard>
          </motion.div>
        )}

        {/* Logs Panel */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="mt-8"
        >
          <GlassCard className="p-6">
            <h2 className="flex items-center gap-3 mb-4">
              <Terminal className="h-5 w-5 text-gray-400" /> Execution Log
            </h2>
            <div className="bg-gray-900 rounded-lg p-4 h-96 overflow-y-auto font-mono text-xs">
              <div className="space-y-1">
                {logs.map((log, index) => (
                  <div key={index} className="flex items-start gap-2">
                    <span className="text-gray-500 w-20">{log.split(']')[0] + ']'}</span>
                    <span className="text-gray-300 break-words">{log.split(']')[1]?.trim()}</span>
                  </div>
                ))}
              </div>
            </div>
          </GlassCard>
        </motion.div>
      </div>
    </div>
  );
}