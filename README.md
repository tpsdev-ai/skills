# TPS Skills

Agent skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenClaw](https://openclaw.ai), and other AI agents.

## Install

```bash
# Claude Code
npx skills add tpsdev-ai/skills/ascii-boxes

# OpenClaw
# Copy the skill folder to your OpenClaw skills directory
```

## Skills

### ascii-boxes

Generate and validate ASCII box diagrams with Unicode box-drawing characters.

**Generate** a diagram from a simple text format:
```bash
python3 ascii-boxes/scripts/draw-box.py input.txt
```

**Validate** an existing diagram:
```bash
python3 ascii-boxes/scripts/check-box-align.py README.md
```

LLMs can't reliably count display columns (box-drawing chars are 3 bytes but 1 column). These tools solve that.

## License

Apache 2.0
