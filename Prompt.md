# Shipra MCP Prompt Examples

This file contains ready-to-copy prompts you can use with AI tools or LLMs that have access to this MCP server.

Use these prompts when the `shipra` MCP server is connected and the model can call the tools directly.

## General instruction prompt

Use this as a base instruction in your AI tool:

```text
You have access to the Shipra MCP server for stock alerts.
When the user asks to create or inspect alerts, use the MCP tools instead of describing the steps manually.
If required inputs are missing, ask one short follow-up question.
When creating alerts, confirm the exact tool used and summarize the final parameters.
```

## Tool list

- `retrieve_alerts`
- `retrieve_alert`
- `create_rsi_alert`
- `create_price_alert`
- `create_drawdown_alert`
- `create_dma_alert`
- `create_pe_alert`
- `create_opportunity_alert`

## Retrieve alerts

### Example prompt: list all alerts

```text
Use the Shipra MCP tools to fetch all my active alerts and summarize them by ticker and condition type.
```

### Example prompt: get one alert by id

```text
Use the Shipra MCP tool to fetch alert id `68f0a1234567890abcdef123` and explain what condition it is tracking.
```

## RSI alerts

### Example prompt: RSI below X

```text
Create an RSI alert for `AAPL` and `MSFT` when RSI(14) drops below 30. Make it recurring and send email alerts to `me@example.com`.
```

### Example prompt: RSI above X

```text
Create an RSI alert for `NVDA` when RSI(14) rises above 70. Keep it open ended.
```

### Example prompt: RSI in range

```text
Create an RSI alert for `TSLA` when RSI(14) stays between 40 and 60.
```

### Example prompt: one-time RSI alert with date expiry

```text
Create a one-time RSI alert for `META` when RSI(21) drops below 28. Expire it on `2026-12-31`.
```

## Price alerts

### Example prompt: price going up

```text
Create a price alert for `RELIANCE` when price is going up. Make it recurring.
```

### Example prompt: price going down

```text
Create a price alert for `INFY` when price is going down.
```

### Example prompt: crossing up by price

```text
Create a price alert for `AAPL` when it crosses up above 220 dollars.
```

### Example prompt: crossing down by price

```text
Create a price alert for `TSLA` when it crosses down below 160 dollars.
```

### Example prompt: crossing up by percentage

```text
Create a price alert for `MSFT` when price moves up by 5 percent. Use the crossing up percentage condition.
```

### Example prompt: crossing down by percentage

```text
Create a price alert for `AMZN` when price falls by 4 percent. Use the crossing down percentage condition.
```

### Example prompt: near 52-week low

```text
Create a price alert for `HDFCBANK` when the stock comes within 3 percent of its 52-week low.
```

### Example prompt: near 52-week high

```text
Create a price alert for `ICICIBANK` when the stock comes within 2 percent of its 52-week high.
```

### Example prompt: within past X days filter

```text
Create a price alert for `SBIN` when it crosses up above 900, but only if that event happens within the past 10 days condition.
```

### Example prompt: positive close

```text
Create a price alert for `GOOG` when it closes positive.
```

### Example prompt: negative close

```text
Create a price alert for `NFLX` when it closes negative and send the notification to WhatsApp number `+15551234567`.
```

## Drawdown alerts

### Example prompt: near last drawdown

```text
Create a drawdown alert for `AAPL` when price is within 5 percent of the last drawdown.
```

### Example prompt: surpass last drawdown

```text
Create a drawdown alert for `TSLA` when price surpasses the last drawdown.
```

### Example prompt: surpass multiple historical drawdowns

```text
Create a drawdown alert for `NVDA` when price surpasses multiple historical drawdowns.
```

### Example prompt: approach historical drawdown

```text
Create a drawdown alert for `MSFT` when price approaches a historical drawdown within 4 percent.
```

### Example prompt: fall below historical drawdown

```text
Create a drawdown alert for `META` when price falls below a historical drawdown.
```

### Example prompt: recover after drawdown

```text
Create a drawdown alert for `AMZN` when price recovers 6 percent after a drawdown.
```

## DMA alerts

### Example prompt: touched DMA

```text
Create a DMA alert for `AAPL` using the 200-day moving average when price touches the DMA.
```

### Example prompt: near DMA

```text
Create a DMA alert for `MSFT` using the 50-day moving average when price comes within 2 percent of the DMA.
```

### Example prompt: fall from DMA

```text
Create a DMA alert for `TSLA` using the 100-day moving average when price falls 5 percent from the DMA.
```

### Example prompt: rise from DMA

```text
Create a DMA alert for `NVDA` using the 20-day moving average when price rises 4 percent from the DMA.
```

### Example prompt: sustain above DMA

```text
Create a DMA alert for `RELIANCE` using the 50-day moving average when price stays above the DMA for 3 days.
```

### Example prompt: sustain below DMA

```text
Create a DMA alert for `INFY` using the 200-day moving average when price stays below the DMA for 5 days.
```

### Example prompt: multiple DMA windows

```text
Create a DMA alert for `SBIN` with DMA windows 50 and 200 when price comes near the DMA within 1.5 percent.
```

## PE ratio alerts

### Example prompt: PE less than X

```text
Create a PE ratio alert for `AAPL` when the PE ratio drops below 20.
```

### Example prompt: PE greater than X

```text
Create a PE ratio alert for `TSLA` when the PE ratio rises above 75.
```

### Example prompt: PE in range

```text
Create a PE ratio alert for `MSFT` when the PE ratio is between 25 and 35.
```

### Example prompt: PE near X-year low

```text
Create a PE ratio alert for `HDFCBANK` when the PE ratio is within 10 percent of its 3-year low.
```

### Example prompt: PE near X-year high

```text
Create a PE ratio alert for `ICICIBANK` when the PE ratio is within 8 percent of its 5-year high.
```

### Example prompt: PE historical extreme

```text
Create a PE ratio alert for `GOOG` when the PE ratio reaches a historical extreme.
```

### Example prompt: PE trending up

```text
Create a PE ratio alert for `META` when the PE ratio is trending up by 6.
```

### Example prompt: PE trending down

```text
Create a PE ratio alert for `NFLX` when the PE ratio is trending down by 5.
```

## Opportunity alerts

### Example prompt: opportunity going up

```text
Create an opportunity alert for `AAPL` with value 80 and sub-condition `GOING_UP`.
```

### Example prompt: opportunity going down

```text
Create an opportunity alert for `TSLA` with value 65 and sub-condition `GOING_DOWN`.
```

## Multi-parameter examples

### Example prompt: price alert with email and expiry

```text
Create a one-time price alert for `AAPL` when it crosses up above 225 dollars. Expire it on `2026-09-30` and send email to `me@example.com`.
```

### Example prompt: DMA alert with multiple stocks

```text
Create a DMA alert for `AAPL`, `MSFT`, and `NVDA` using the 50-day moving average when price stays above the DMA for 4 days.
```

### Example prompt: PE alert with recurring frequency

```text
Create a recurring PE ratio alert for `TCS` when the PE ratio is between 20 and 28.
```

## Short prompts for tool routing

These are compact prompts if you want the LLM to decide the exact MCP call:

```text
Set an RSI oversold alert for AAPL below 30.
```

```text
Alert me if TSLA crosses below 160.
```

```text
Create a drawdown recovery alert for AMZN after a 5 percent recovery.
```

```text
Create a 200 DMA touch alert for NVDA.
```

```text
Set a PE alert for MSFT above 35.
```

```text
Create an upward opportunity alert for META with value 70.
```

## Prompt template for any stock alert

```text
Use the Shipra MCP server to create an alert.

Ticker(s): <tickers>
Tool: <create_rsi_alert | create_price_alert | create_drawdown_alert | create_dma_alert | create_pe_alert | create_opportunity_alert>
Condition: <describe exact trigger>
Frequency: <RECURRING or ONCE>
Expiration: <OPEN_ENDED or DATE>
Expiration date: <optional YYYY-MM-DD>
Notify email: <optional email>
Notify WhatsApp: <optional number, only for price alerts>
```

## Notes for LLM usage

- Use stock tickers as a list when calling the MCP tools.
- Use `expiration_date` only when `expiration_type` is `DATE`.
- Use `notify_whatsapp` only with `create_price_alert`.
- `create_dma_alert` requires `dma_window`.
- `create_opportunity_alert` requires both `value` and `sub_condition`.
- If the user gives a natural-language request, map it to the nearest supported condition and ask a follow-up only if the threshold or direction is missing.
