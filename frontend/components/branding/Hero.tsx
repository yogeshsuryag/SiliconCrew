"use client";

import { Github, CircleDot } from "lucide-react";
import { Logo } from "./Logo";
import { REPO_URL, ISSUES_URL } from "./links";

const CAPABILITIES = [
  "Starts from a structured specification and generates synthesizable Verilog.",
  "Creates self-checking testbenches and can inspect waveforms when simulation fails.",
  "Runs RTL lint and simulation with local tools.",
  "Presents source files, tool activity, and results in one workbench.",
];

const TOOLS = ["Verilog", "Icarus Verilog", "MCP"];

/** Compact project intro shown on the landing page. */
export function Hero() {
  return (
    <section data-testid="landing-hero" className="mb-9">
      <div className="rounded-xl border border-border bg-surface-1/60 p-6 md:p-7">
        <div className="flex items-start gap-3.5">
          <div className="w-10 h-10 rounded-lg bg-primary/15 grid place-items-center shrink-0 text-primary">
            <Logo className="h-6 w-6" />
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <h1 className="text-[19px] font-semibold tracking-tight">SiliconCrew</h1>
              <span className="text-[10.5px] font-medium uppercase tracking-wide text-muted-foreground/80 border border-border rounded px-1.5 py-0.5">
                Open source · MIT
              </span>
            </div>
            <p className="mt-1 text-[13.5px] text-foreground/85 leading-snug">
              An LLM-assisted demo for RTL design and verification.
            </p>
            <p className="mt-1 text-[12px] text-muted-foreground">
              spec → RTL → lint → simulate, with local EDA tools.
            </p>
          </div>
        </div>

        <ul className="mt-5 grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-2">
          {CAPABILITIES.map((c) => (
            <li key={c} className="flex items-start gap-2 text-[12.5px] text-foreground/80">
              <span className="mt-1.5 h-1 w-1 rounded-full bg-primary/70 shrink-0" />
              <span className="min-w-0">{c}</span>
            </li>
          ))}
        </ul>

        <div className="mt-5 flex items-center gap-2 flex-wrap">
          {TOOLS.map((t) => (
            <span
              key={t}
              className="text-[11px] font-medium text-muted-foreground bg-surface-2 border border-border rounded-md px-2 py-1"
            >
              {t}
            </span>
          ))}
        </div>

        <div className="mt-5 flex items-center gap-3 flex-wrap">
          <a
            href={REPO_URL}
            target="_blank"
            rel="noreferrer noopener"
            className="inline-flex items-center gap-1.5 h-9 px-3.5 rounded-lg bg-primary text-primary-foreground text-[12.5px] font-medium hover:opacity-90"
          >
            <Github className="h-4 w-4" /> View on GitHub
          </a>
          <a
            href={ISSUES_URL}
            target="_blank"
            rel="noreferrer noopener"
            className="inline-flex items-center gap-1.5 h-9 px-3 rounded-lg border border-border text-[12.5px] font-medium text-foreground hover:bg-surface-2"
          >
            <CircleDot className="h-4 w-4" /> Issues
          </a>
        </div>
      </div>
    </section>
  );
}
