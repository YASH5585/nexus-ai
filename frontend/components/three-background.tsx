"use client";

import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Float, MeshDistortMaterial } from "@react-three/drei";
import * as THREE from "three";

function mulberry32(seed: number) {
  return function () {
    let t = (seed += 0x6d2b79f5);
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

function createParticles() {
  const count = 1200;
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const random = mulberry32(42);
  for (let i = 0; i < count; i++) {
    const i3 = i * 3;
    positions[i3] = (random() - 0.5) * 20;
    positions[i3 + 1] = (random() - 0.5) * 20;
    positions[i3 + 2] = (random() - 0.5) * 20;
    const color = new THREE.Color();
    color.setHSL(0.6 + random() * 0.2, 0.8, 0.6);
    colors[i3] = color.r;
    colors[i3 + 1] = color.g;
    colors[i3 + 2] = color.b;
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
  return geometry;
}

function Particles() {
  const ref = useRef<THREE.Points>(null);
  const geometry = useMemo(() => createParticles(), []);

  useFrame((state) => {
    if (ref.current) {
      ref.current.rotation.y = state.clock.elapsedTime * 0.05;
      ref.current.rotation.x = state.clock.elapsedTime * 0.02;
    }
  });

  return (
    <points ref={ref} geometry={geometry}>
      <pointsMaterial size={0.02} vertexColors blending={THREE.AdditiveBlending} depthWrite={false} />
    </points>
  );
}

function FloatingOrb({ position, color, speed }: { position: [number, number, number]; color: string; speed: number }) {
  const ref = useRef<THREE.Mesh>(null);
  useFrame((state) => {
    if (ref.current) {
      ref.current.rotation.x = state.clock.elapsedTime * speed;
      ref.current.rotation.y = state.clock.elapsedTime * speed * 0.5;
    }
  });

  return (
    <Float speed={2} rotationIntensity={1} floatIntensity={2}>
      <mesh ref={ref} position={position}>
        <sphereGeometry args={[0.8, 32, 32]} />
        <MeshDistortMaterial color={color} envMapIntensity={0.5} distort={0.3} speed={2} transparent opacity={0.6} />
      </mesh>
    </Float>
  );
}

export default function ThreeBackground() {
  return (
    <div className="fixed inset-0 -z-10">
      <Canvas camera={{ position: [0, 0, 8], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#8b5cf6" />
        <Particles />
        <FloatingOrb position={[-4, 2, -2]} color="#3b82f6" speed={1} />
        <FloatingOrb position={[4, -2, -3]} color="#8b5cf6" speed={0.8} />
        <FloatingOrb position={[0, 4, -4]} color="#6366f1" speed={1.2} />
      </Canvas>
    </div>
  );
}
