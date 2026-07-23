import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: false,
  output: "export",
  trailingSlash: true,
  basePath: "/nexus-ai",
  images: {
    unoptimized: true,
    remotePatterns: [
      {
        protocol: "https",
        hostname: "nexus-ai.vercel.app",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "nexus-ai-backend.onrender.com",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "**",
      },
    ],
  },
  env: {
    NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL || "https://nexus-ai-backend.onrender.com",
    NEXT_PUBLIC_FRONTEND_URL: process.env.NEXT_PUBLIC_FRONTEND_URL || "https://nexus-ai.vercel.app",
  },
};

export default nextConfig;