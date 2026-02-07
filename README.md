owockibot - Python SDK for the AI Bounty Board API

A clean, type-hinted Python client for interacting with the owockibot
bounty board at https://bounty.owockibot.xyz

## Features

- ✅ **Complete API Coverage** - All bounty board endpoints
- ✅ **Type Hints Throughout** - Full mypy compatibility
- ✅ **Sync & Async** - Both synchronous and async clients
- ✅ **Error Handling** - Custom exceptions for all error cases
- ✅ **Filtering & Search** - Powerful query builder for bounties
- ✅ **Dataclass Models** - Immutable, typed data models
- ✅ **PyPI Ready** - Modern Python packaging with pyproject.toml

## Installation

```bash
pip install owockibot
```

## Quick Start

```python
from owockibot import BountyBoardClient

# Create client
client = BountyBoardClient()

# List all open bounties
bounties = client.list_bounties()
for bounty in bounties:
    if bounty.is_open:
        print(f"{bounty.title}: {bounty.reward_formatted}")

# Get a specific bounty
bounty = client.get_bounty("143")
print(bounty.description)

# Get platform stats
stats = client.get_stats()
print(f"Total rewards: {stats.total_rewards_usdc} USDC")
```

## Async Usage

```python
import asyncio
from owockibot import AsyncBountyBoardClient

async def main():
    async with AsyncBountyBoardClient() as client:
        bounties = await client.list_bounties()
        for bounty in bounties:
            print(f"{bounty.title}: {bounty.reward_formatted}")

asyncio.run(main())
```

## Filtering Bounties

```python
from owockibot import BountyBoardClient, BountyFilter, BountyStatus
from decimal import Decimal

client = BountyBoardClient()
bounties = client.list_bounties()

# Using filter builder
filter = (
    BountyFilter()
    .with_status(BountyStatus.OPEN)
    .with_tags("coding", "design")
    .with_min_reward(Decimal("20.00"))
    .search("tutorial")
)
matching = filter.apply(bounties)

# Or use utility functions
from owockibot.filters import filter_open, sort_by_reward

open_bounties = filter_open(bounties)
top_paying = sort_by_reward(open_bounties, descending=True)[:10]
```

## Claiming and Submitting

```python
from owockibot import BountyBoardClient

client = BountyBoardClient()

# Claim a bounty
bounty = client.claim_bounty(
    bounty_id="143",
    wallet_address="0x..."
)

# Submit work
bounty = client.submit_work(
    bounty_id="143",
    wallet_address="0x...",
    content="I've completed the task...",
    proof="https://github.com/..."
)
```

## Error Handling

```python
from owockibot import BountyBoardClient
from owockibot.exceptions import NotFoundError, ValidationError, APIError

client = BountyBoardClient()

try:
    bounty = client.get_bounty("99999")
except NotFoundError:
    print("Bounty not found")
except ValidationError as e:
    print(f"Validation failed: {e.message}")
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
```

## Advanced: Custom Filtering

```python
from owockibot import BountyFilter, Bounty

# Custom filter function
def high_value_coding(bounty: Bounty) -> bool:
    return (
        bounty.reward_usdc >= 50 and
        any("coding" in tag.lower() for tag in bounty.tags)
    )

filter = BountyFilter()
filter.custom_filter = high_value_coding
high_value = filter.apply(bounties)
```

## API Reference

### BountyBoardClient

- `list_bounties()` - List all bounties
- `get_bounty(id)` - Get a specific bounty
- `get_stats()` - Get platform statistics
- `get_x402_config()` - Get payment configuration
- `claim_bounty(id, wallet_address)` - Claim a bounty
- `submit_work(id, wallet_address, content, proof=None)` - Submit work

### Models

- `Bounty` - Bounty data (title, reward, status, etc.)
- `Stats` - Platform statistics
- `Submission` - Work submission
- `Payment` / `PendingPayment` - Payment details
- `X402Config` - Payment configuration

### Exceptions

- `OwockibotError` - Base exception
- `APIError` - General API error
- `NotFoundError` - 404 errors
- `ValidationError` - 400 errors
- `RateLimitError` - 429 errors
- `ServerError` - 5xx errors

## Development

```bash
# Clone repository
git clone https://github.com/yourusername/owockibot-sdk.git
cd owockibot-sdk

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy owockibot

# Linting
ruff check owockibot
```

## License

MIT License - see LICENSE file
