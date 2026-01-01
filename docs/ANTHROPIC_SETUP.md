# Anthropic Claude Setup Guide

Use Anthropic's Claude instead of OpenAI for AI job analysis - often **cheaper and faster**!

## Why Choose Anthropic Claude?

### 💰 Cost Comparison

| Model | Cost per Job | Speed | Quality |
|-------|--------------|-------|---------|
| **Claude 3 Haiku** | ~$0.0005 | ⚡⚡⚡ Fastest | Good |
| **Claude 3.5 Sonnet** | ~$0.003 | ⚡⚡ Fast | Excellent |
| **Claude 3 Opus** | ~$0.015 | ⚡ Moderate | Best |
| GPT-3.5-turbo | ~$0.01 | ⚡⚡ Fast | Good |
| GPT-4 | ~$0.05 | ⚡ Slow | Excellent |

**Winner: Claude 3.5 Sonnet** - Best balance of cost, speed, and quality!

### ✅ Advantages

- **Cheaper**: 3-10x cheaper than OpenAI for similar quality
- **Faster**: Often faster response times
- **Longer context**: Can handle longer job descriptions
- **Better JSON**: More reliable JSON output
- **Choice**: Freedom to switch between providers

---

## Quick Setup (3 Steps)

### Step 1: Get Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up for an account
3. Click "API Keys" in the left menu
4. Click "Create Key"
5. Copy your API key (starts with `sk-ant-...`)
6. **Save it now** - you can't see it again!

### Step 2: Add to Environment

Edit your `.env` file:

```env
# Option 1: Use Anthropic instead of OpenAI
ANTHROPIC_API_KEY=sk-ant-your_key_here

# You can comment out or remove OpenAI
# OPENAI_API_KEY=
```

### Step 3: Update Configuration

Edit `config/config.yaml`:

```yaml
ai:
  provider: "anthropic"  # Change from "openai"
  model: "claude-3-5-sonnet-20241022"  # Recommended!
  temperature: 0.7
  max_tokens: 1000
```

**Done!** The system will now use Claude instead of OpenAI.

---

## Claude Model Guide

### Claude 3 Haiku - Fastest & Cheapest
```yaml
model: "claude-3-haiku-20240307"
```
- **Cost**: ~$0.0005 per job (20x cheaper than GPT-3.5-turbo!)
- **Speed**: Lightning fast
- **Use for**: High-volume searches, simple extraction
- **Perfect for**: Analyzing 1000+ jobs/month

### Claude 3.5 Sonnet - Best Value (Recommended)
```yaml
model: "claude-3-5-sonnet-20241022"
```
- **Cost**: ~$0.003 per job (3x cheaper than GPT-3.5-turbo)
- **Speed**: Very fast
- **Use for**: Most use cases, excellent balance
- **Perfect for**: Regular job searches

### Claude 3 Opus - Highest Quality
```yaml
model: "claude-3-opus-20240229"
```
- **Cost**: ~$0.015 per job (3x cheaper than GPT-4)
- **Speed**: Moderate
- **Use for**: Critical job analysis, complex requirements
- **Perfect for**: Senior roles, detailed analysis

---

## Usage Examples

### Using Claude via CLI

```bash
# Search with Claude analysis (Sonnet)
python -m src.main --search "Python Developer"

# The system automatically uses Claude if configured!
```

### Using Claude via API

```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Software Engineer",
    "analyze": true
  }'
```

### Using Claude via n8n

```json
{
  "keywords": "Data Scientist",
  "options": {
    "analyze": true
  }
}
```

Claude is used automatically based on your config!

---

## Switching Between Providers

### Option 1: Configuration File

Edit `config/config.yaml`:

```yaml
ai:
  provider: "anthropic"  # or "openai"
  model: "claude-3-5-sonnet-20241022"  # or "gpt-3.5-turbo"
```

### Option 2: Environment Variable

```env
# Use Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Or use OpenAI
OPENAI_API_KEY=sk-proj-...
```

### Option 3: Auto-Detection

The system auto-detects the provider from the model name:

```yaml
model: "claude-3-5-sonnet-20241022"  # Auto-uses Anthropic
model: "gpt-4"                        # Auto-uses OpenAI
```

---

## Cost Optimization with Claude

### Strategy 1: Use Haiku for Bulk Analysis

```yaml
# For 1000+ jobs
model: "claude-3-haiku-20240307"
```

Cost: 1000 jobs × $0.0005 = **$0.50** 🎉

Compare to GPT-3.5-turbo: 1000 jobs × $0.01 = **$10.00**

**Savings: $9.50 (95%!)**

### Strategy 2: Use Sonnet for Quality

```yaml
# For regular use
model: "claude-3-5-sonnet-20241022"
```

Cost: 100 jobs × $0.003 = **$0.30**

Compare to GPT-3.5-turbo: 100 jobs × $0.01 = **$1.00**

**Savings: $0.70 (70%)**

### Strategy 3: Mix and Match

1. **Initial search** with Haiku (cheap, fast)
2. **Top candidates** with Opus (detailed analysis)

```bash
# Bulk search with Haiku
python -m src.main --search "Python Dev" --limit 100

# Then manually analyze top 10 with Opus
# (Change config to opus, run analysis on specific jobs)
```

---

## Comparison Table

| Feature | Anthropic Claude | OpenAI GPT |
|---------|------------------|------------|
| **Cheapest option** | Haiku: $0.0005 | GPT-3.5-turbo: $0.01 |
| **Best value** | Sonnet: $0.003 | GPT-3.5-turbo: $0.01 |
| **Highest quality** | Opus: $0.015 | GPT-4: $0.05 |
| **Speed** | ⚡⚡⚡ Very fast | ⚡⚡ Fast |
| **JSON reliability** | ✅ Excellent | ✅ Good |
| **Context length** | ✅ 200K tokens | ⚠️ 128K tokens |
| **Setup complexity** | 🟢 Easy | 🟢 Easy |

---

## Troubleshooting

### Error: "Anthropic package not installed"

**Solution:**
```bash
pip install anthropic
```

### Error: "Invalid API key"

**Solution:**
1. Check `.env` file has correct key
2. Ensure key starts with `sk-ant-`
3. No quotes around the key
4. Key is from https://console.anthropic.com/

### Error: "Model not found"

**Solution:**
Use exact model names:
- `claude-3-5-sonnet-20241022` ✅
- `claude-3-sonnet` ❌ (wrong format)

Check latest models at: https://docs.anthropic.com/en/docs/models-overview

### No AI analysis happening

**Solution:**
1. Make sure `analyze: true` in requests
2. Don't use `--no-analyze` flag
3. Check config has correct model name
4. Verify ANTHROPIC_API_KEY is set

---

## Monthly Cost Examples

### Light Usage (100 jobs/month)

**With Claude Haiku:**
- 100 × $0.0005 = **$0.05/month** ✅

**With Claude Sonnet:**
- 100 × $0.003 = **$0.30/month** ✅

**Compare to GPT-3.5-turbo:**
- 100 × $0.01 = **$1.00/month**

### Medium Usage (500 jobs/month)

**With Claude Sonnet:**
- 500 × $0.003 = **$1.50/month** ✅

**Compare to GPT-3.5-turbo:**
- 500 × $0.01 = **$5.00/month**

**Savings: $3.50/month**

### Heavy Usage (2000 jobs/month)

**With Claude Haiku:**
- 2000 × $0.0005 = **$1.00/month** ✅

**With Claude Sonnet:**
- 2000 × $0.003 = **$6.00/month** ✅

**Compare to GPT-3.5-turbo:**
- 2000 × $0.01 = **$20.00/month**

**Savings: $19.00/month with Haiku!**

---

## Best Practices

### 1. Start with Sonnet
```yaml
model: "claude-3-5-sonnet-20241022"
```
Best balance for most users.

### 2. Use Haiku for High Volume
If analyzing 500+ jobs/month, switch to Haiku:
```yaml
model: "claude-3-haiku-20240307"
```

### 3. Reserve Opus for Critical Jobs
Only use Opus when quality is absolutely critical.

### 4. Monitor Usage
Check your usage at: https://console.anthropic.com/

### 5. Set Budget Limits
In Anthropic console, set monthly spend limits.

---

## Migration from OpenAI

### Quick Migration

1. **Get Anthropic key**: https://console.anthropic.com/
2. **Add to .env**:
   ```env
   ANTHROPIC_API_KEY=sk-ant-...
   ```
3. **Update config.yaml**:
   ```yaml
   model: "claude-3-5-sonnet-20241022"
   ```
4. **Test**:
   ```bash
   python -m src.main --search "Test" --limit 1
   ```

### Keep Both Keys (Flexibility)

You can keep both keys and switch as needed:

```env
# .env
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
```

```yaml
# config.yaml - Switch by changing model name
model: "claude-3-5-sonnet-20241022"  # Uses Anthropic
# model: "gpt-3.5-turbo"             # Uses OpenAI
```

---

## Links

- **Anthropic Console**: https://console.anthropic.com/
- **API Documentation**: https://docs.anthropic.com/
- **Pricing**: https://www.anthropic.com/pricing
- **Model Comparison**: https://docs.anthropic.com/en/docs/models-overview

---

## Summary

**Recommended setup:**
```yaml
provider: "anthropic"
model: "claude-3-5-sonnet-20241022"
```

**Cost:** ~$0.003 per job (3x cheaper than OpenAI)

**Quality:** Excellent

**Setup time:** 5 minutes

**Savings:** 70%+ on AI analysis costs! 🎉

---

**Ready to save money? Follow the Quick Setup above!** 💰
