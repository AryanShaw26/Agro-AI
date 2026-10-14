import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'AgroAI — Plant Disease Detection Platform | Model 1: EfficientNet-B0',
  description:
    'Production plant leaf disease classification powered by Model 1 (EfficientNet-B0) across 38 PlantVillage classes with a verified agricultural knowledge base. Strictly no Generative AI.',
  keywords: [
    'AgroAI',
    'plant disease detection',
    'leaf disease scan',
    'EfficientNet-B0',
    'PlantVillage',
    'agricultural AI',
    'crop diagnosis',
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={`${inter.className} min-h-screen flex flex-col bg-[#F7F5EE] text-[#1C231F]`}>
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
