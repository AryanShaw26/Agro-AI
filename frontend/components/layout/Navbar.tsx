'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Leaf, Scan, BookOpen, History, Info, Menu, X, ArrowRight } from 'lucide-react';

export default function Navbar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { href: '/', label: 'Home' },
    { href: '/scan', label: 'AI Scan' },
    { href: '/diseases', label: 'Diseases (38)' },
    { href: '/history', label: 'Scan History' },
    { href: '/about', label: 'Model Transparency' },
  ];

  return (
    <header className="sticky top-0 z-50 w-full bg-[#F7F5EE]/90 backdrop-blur-md border-b border-[rgba(28,35,31,0.08)] transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        {/* Brand Logo */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-11 h-11 rounded-2xl bg-[#1F694B] flex items-center justify-center text-white shadow-sm transition-transform duration-200 group-hover:scale-105">
            <div className="relative">
              <Leaf className="w-6 h-6 text-[#F7F5EE]" />
              <Scan className="w-3.5 h-3.5 text-[#D6A434] absolute -bottom-1 -right-1" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-xl tracking-tight text-[#1C231F]">AgroAI</span>
              <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-[#E7F0EA] text-[#1F694B] border border-[#2E8B67]/20">
                EfficientNetV2-S
              </span>
            </div>
            <p className="text-[11px] text-[#6B756F] hidden sm:block tracking-wide">Scan. Understand. Protect.</p>
          </div>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-1 bg-white/70 px-4 py-1.5 rounded-full border border-[rgba(28,35,31,0.06)] shadow-sm">
          {navLinks.map((link) => {
            const isActive = pathname === link.href || (link.href !== '/' && pathname.startsWith(link.href));
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-[#1F694B] text-white shadow-sm'
                    : 'text-[#1C231F] hover:text-[#1F694B] hover:bg-[#E7F0EA]/60'
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        {/* Primary CTA */}
        <div className="hidden sm:flex items-center gap-3">
          <Link
            href="/scan"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#1F694B] text-white text-sm font-semibold shadow-sm hover:bg-[#18533b] hover:shadow-md transition-all active:scale-[0.98]"
          >
            <Scan className="w-4 h-4 text-[#D6A434]" />
            <span>Scan a Leaf</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {/* Mobile menu button */}
        <div className="flex sm:hidden">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-xl bg-white border border-[rgba(28,35,31,0.08)] text-[#1C231F]"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="sm:hidden bg-[#F7F5EE] border-b border-[rgba(28,35,31,0.08)] px-4 pt-3 pb-6 space-y-2">
          {navLinks.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className={`block px-4 py-2.5 rounded-xl text-sm font-medium ${
                  isActive ? 'bg-[#1F694B] text-white' : 'text-[#1C231F] bg-white border border-[rgba(28,35,31,0.04)]'
                }`}
              >
                {link.label}
              </Link>
            );
          })}
          <div className="pt-2">
            <Link
              href="/scan"
              onClick={() => setMobileMenuOpen(false)}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-[#1F694B] text-white text-sm font-semibold"
            >
              <Scan className="w-4 h-4 text-[#D6A434]" />
              <span>Scan a Leaf Now</span>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}

