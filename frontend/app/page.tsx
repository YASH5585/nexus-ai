"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import ThreeBackground from "@/components/three-background";
import { FeaturesSection } from "@/components/landing/features-section";
import { HowItWorksSection } from "@/components/landing/how-it-works-section";
import { ArchitectureSection } from "@/components/landing/architecture-section";
import { DemoSection } from "@/components/landing/demo-section";
import { TestimonialsSection } from "@/components/landing/testimonials-section";
import { FAQSection } from "@/components/landing/faq-section";
import { Footer } from "@/components/landing/footer";

export default function Home() {
  return (
    <div className="relative min-h-screen">
      <ThreeBackground />

      <section className="relative min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-5xl text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
            className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-sm text-zinc-300 backdrop-blur-sm mb-8"
          >
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            OpenAI Build Week Hackathon
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-5xl sm:text-6xl lg:text-8xl font-bold tracking-tight mb-6"
          >
            <span className="block bg-gradient-to-r from-white via-blue-100 to-zinc-400 bg-clip-text text-transparent">
              The Self-Healing
            </span>
            <span className="block bg-gradient-to-r from-blue-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent mt-2">
              Software Engineer
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="text-xl sm:text-2xl text-zinc-400 font-medium mb-4 tracking-wide"
          >
            Build. Test. Fix. Repeat.
          </motion.p>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="text-base text-zinc-500 max-w-2xl mx-auto mb-10 leading-relaxed"
          >
            Nexus AI is an autonomous agent that writes code, runs it in secure sandboxes,
            and iteratively patches failures until every test passes.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <Link href="/dashboard">
              <Button size="lg" className="group">
                Launch Dashboard
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
            <Link href="#how-it-works">
              <Button variant="secondary" size="lg">
                See How it Works
              </Button>
            </Link>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.5, duration: 1 }}
            className="mt-20"
          >
            <Link href="#features" className="inline-flex flex-col items-center text-zinc-500 hover:text-white transition-colors">
              <span className="text-xs uppercase tracking-widest mb-2">Scroll</span>
              <motion.div animate={{ y: [0, 8, 0] }} transition={{ duration: 1.5, repeat: Infinity }}>
                <ChevronDown className="h-5 w-5" />
              </motion.div>
            </Link>
          </motion.div>
        </div>
      </section>

      <div id="features">
        <FeaturesSection />
      </div>

      <div id="architecture">
        <ArchitectureSection />
      </div>

      <DemoSection />

      <div id="how-it-works">
        <HowItWorksSection />
      </div>

      <TestimonialsSection />
      <FAQSection />
      <Footer />
    </div>
  );
}
