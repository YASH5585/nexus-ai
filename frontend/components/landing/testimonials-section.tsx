"use client";

import { motion } from "framer-motion";
import { GlassCard } from "@/components/ui/glass-card";

const testimonials = [
  {
    quote: "Nexus AI reduced our debugging time by 80%. It&apos;s like having a senior engineer who never sleeps.",
    author: "Sarah Chen",
    role: "CTO at TechCorp",
    avatar: "SC",
  },
  {
    quote: "The self-healing loop is magic. We shipped a critical feature in hours instead of days.",
    author: "Marcus Johnson",
    role: "Lead Developer at StartupXYZ",
    avatar: "MJ",
  },
  {
    quote: "Finally, an AI that actually understands code context and fixes real bugs, not just syntax.",
    author: "Elena Rodriguez",
    role: "Software Architect at EnterpriseCo",
    avatar: "ER",
  },
];

export function TestimonialsSection() {
  return (
    <section className="py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Trusted by engineering teams
          </h2>
          <p className="text-lg text-zinc-400 max-w-2xl mx-auto">
            See how teams are shipping faster with autonomous code healing.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {testimonials.map((testimonial, i) => (
            <motion.div
              key={testimonial.author}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
            >
              <GlassCard className="h-full p-6 flex flex-col">
                <div className="flex-1">
                  <p className="text-zinc-300 leading-relaxed italic">&ldquo;{testimonial.quote}&rdquo;</p>
                </div>
                <div className="mt-6 flex items-center gap-3">
                  <div className="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-semibold text-sm">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-white">{testimonial.author}</p>
                    <p className="text-xs text-zinc-400">{testimonial.role}</p>
                  </div>
                </div>
              </GlassCard>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
