"use client";

import { motion } from "framer-motion";
import { GlassCard } from "@/components/ui/glass-card";
import { ChevronDown } from "lucide-react";
import { useState } from "react";

const faqs = [
  {
    question: "What is Nexus AI?",
    answer: "Nexus AI is an autonomous software engineering agent that generates code, executes it in secure sandboxes, and self-heals failures through an intelligent iterative loop until all tests pass.",
  },
  {
    question: "How does the self-healing loop work?",
    answer: "After generating code, Nexus AI runs unit tests, collects compiler errors, runtime errors, and failed tests. It then analyzes the failures and patches the code automatically, repeating until success or the retry limit is reached.",
  },
  {
    question: "Is my code secure?",
    answer: "Yes. All code execution happens in isolated sandbox environments with strict timeouts and resource limits. No persistent storage or network access is granted by default.",
  },
  {
    question: "What programming languages are supported?",
    answer: "Currently Python is fully supported with pytest integration. JavaScript/TypeScript support is coming soon with Jest and Vitest.",
  },
  {
    question: "Can I integrate this into my CI/CD pipeline?",
    answer: "Absolutely. Nexus AI exposes a REST API that can be integrated into any CI/CD workflow. We also provide SDKs for Python and TypeScript.",
  },
  {
    question: "What happens if the AI can&apos;t fix the code?",
    answer: "After reaching the maximum retry limit (default: 5), the system returns the last attempted code along with a detailed error report and reasoning trace for manual intervention.",
  },
];

export function FAQSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section className="py-24">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Frequently asked questions
          </h2>
          <p className="text-lg text-zinc-400">
            Everything you need to know about Nexus AI.
          </p>
        </motion.div>

        <div className="space-y-4">
          {faqs.map((faq, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
            >
              <GlassCard className="overflow-hidden">
                <button
                  onClick={() => setOpenIndex(openIndex === i ? null : i)}
                  className="w-full flex items-center justify-between p-5 text-left"
                >
                  <span className="text-sm font-medium text-white">{faq.question}</span>
                  <motion.div
                    animate={{ rotate: openIndex === i ? 180 : 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <ChevronDown className="h-4 w-4 text-zinc-400" />
                  </motion.div>
                </button>
                <motion.div
                  initial={false}
                  animate={{ height: openIndex === i ? "auto" : 0, opacity: openIndex === i ? 1 : 0 }}
                  transition={{ duration: 0.3 }}
                  className="overflow-hidden"
                >
                  <p className="px-5 pb-5 text-sm text-zinc-400 leading-relaxed">{faq.answer}</p>
                </motion.div>
              </GlassCard>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
