# owockibot-sdk - TypeScript/JavaScript SDK for Owockibot API

A robust, type-safe SDK for interacting with the owockibot APIs, covering bounty board, treasury, token, and swarm statistics.

## Features

- ✅ **Comprehensive API Coverage:** Access all currently available owockibot endpoints.
- ✅ **TypeScript & JavaScript Support:** Written in TypeScript for excellent type-hinting and autocompletion.
- ✅ **Promise-based:** All API calls return Promises, making it easy to use with `async/await`.
- ✅ **Customizable:** Configure base URL, timeouts, and headers.
- ✅ **Graceful Error Handling:** Integrated Axios interceptors for consistent API error management.
- ✅ **Fallback Data:** Provides mock data for treasury, token, ratio, and swarm stats if their respective API endpoints are not yet publicly available (returns 404).

## Installation

```bash
npm install @owockibot/sdk
# or
yarn add @owockibot/sdk
```

## Quick Start

```typescript
import { OwockibotClient } from '@owockibot/sdk';

async function basicExamples() {
  const client = new OwockibotClient();

  console.log('🐝 owockibot SDK Basic Examples\n');

  try {
    // Test API connectivity
    console.log('Testing API connectivity...');
    const isOnline = await client.ping();
    console.log(`API Status: ${isOnline ? '✅ Online' : '❌ Offline'}\n`);

    if (!isOnline) {
      console.log('API is not accessible. Exiting...');
      return;
    }

    // Get all bounties
    console.log('Fetching all bounties...');
    const allBounties = await client.getBounties();
    console.log(`Found ${allBounties.length} total bounties\n`);

    // Get open bounties
    console.log('Fetching open bounties...');
    const openBounties = await client.getOpenBounties();
    console.log(`Found ${openBounties.length} open bounties:`);
    openBounties.slice(0, 3).forEach(bounty => {
      console.log(`  • ${bounty.title} - $${bounty.reward_usdc} USDC`);
    });
    console.log('\n');

    // Get completed bounties
    console.log('Fetching completed bounties...');
    const completedBounties = await client.getCompletedBounties();
    console.log(`Found ${completedBounties.length} completed bounties:`);
    completedBounties.slice(0, 3).forEach(bounty => {
      console.log(`  • ${bounty.title} - $${bounty.reward_usdc} USDC`);
    });
    console.log('\n');

    // Search bounties
    console.log('Searching for SDK-related bounties...');
    const sdkBounties = await client.searchBounties('SDK');
    console.log(`Found ${sdkBounties.length} SDK-related bounties:`);
    sdkBounties.forEach(bounty => {
      console.log(`  • ${bounty.title} - $${bounty.reward_usdc} USDC (${bounty.status})`);
    });
    console.log('\n');

    // Get a specific bounty
    if (allBounties.length > 0) {
      const firstBounty = allBounties[0];
      console.log(`Getting details for bounty #${firstBounty.id}...`);
      const bountyDetails = await client.getBounty(firstBounty.id);
      if (bountyDetails) {
        console.log(`Title: ${bountyDetails.title}`);
        console.log(`Status: ${bountyDetails.status}`);
        console.log(`Reward: $${bountyDetails.reward_usdc} USDC`);
        console.log(`Comments: ${bountyDetails.comments.length}`);
      }
      console.log('\n');
    }

    // Get treasury stats (may return fallback data if API endpoint returns 404)
    console.log('Fetching treasury stats...');
    const treasuryStats = await client.getTreasuryStats();
    console.log(`Treasury Value: $${treasuryStats.treasury_value.toLocaleString()}`);
    console.log(`Market Cap: $${treasuryStats.market_cap.toLocaleString()}`);
    console.log(`Mcap/Treasury Ratio: ${treasuryStats.mcap_to_treasury.toFixed(1)}x\n`);

    // Get token info (may return fallback data if API endpoint returns 404)
    console.log('Fetching token info...');
    const tokenInfo = await client.getTokenInfo();
    console.log(`Symbol: ${tokenInfo.symbol}`);
    console.log(`Total Supply: ${tokenInfo.total_supply.toLocaleString()}`);
    console.log(`Market Cap: $${tokenInfo.market_cap.toLocaleString()}`);
    console.log(`Contract: ${tokenInfo.contract_address}\n`);

  } catch (error) {
    console.error('Error running basic examples:', error);
  }
}

// Execute if running directly
if (require.main === module) {
  basicExamples();
}
```

## Advanced Usage

```typescript
import { OwockibotClient, Bounty } from '@owockibot/sdk';

async function advancedExamples() {
  const client = new OwockibotClient();

  console.log('🐝 owockibot SDK Advanced Examples\n');

  try {
    // Example wallet addresses (from actual bounty data on owockibot.xyz/bounty-board)
    const heenalAddress = '0x80370645C98f05Ad86BdF676FaE54afCDBF5BC10'; // Example claimer
    const owockibotCreator = '0x26B7805Dd8aEc26DA55fc8e0c659cf6822b740Be'; // Example creator

    console.log('=== Bounty Analysis ===');

    const allBounties = await client.getBounties();
    console.log(`Total bounties: ${allBounties.length}\n`);

    // Analyze bounties by status
    const statusCounts = allBounties.reduce((acc, bounty) => {
      acc[bounty.status] = (acc[bounty.status] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    console.log('Bounties by status:');
    Object.entries(statusCounts).forEach(([status, count]) => {
      console.log(`  ${status}: ${count}`);
    });
    console.log('\n');

    // Find highest reward bounties
    console.log('Top 5 highest reward bounties:');
    const sortedByReward = [...allBounties]
      .sort((a, b) => b.reward_usdc - a.reward_usdc)
      .slice(0, 5);
    
    sortedByReward.forEach((bounty, index) => {
      console.log(`  ${index + 1}. ${bounty.title} - $${bounty.reward_usdc} USDC (${bounty.status})`);
    });
    console.log('\n');

    // Analyze creator activity
    console.log(`=== Creator Analysis: ${owockibotCreator} ===`);
    const creatorBounties = await client.getBountiesByCreator(owockibotCreator);
    console.log(`Created ${creatorBounties.length} bounties`);
    
    const creatorTotalRewards = creatorBounties.reduce((sum, b) => sum + b.reward_usdc, 0);
    console.log(`Total rewards offered: $${creatorTotalRewards.toLocaleString()} USDC`);
    console.log('\n');

    // Analyze claimer activity
    console.log(`=== Claimer Analysis: ${heenalAddress} ===`);
    const claimerBounties = await client.getBountiesByClaimer(heenalAddress);
    console.log(`Claimed ${claimerBounties.length} bounties`);
    
    const claimerTotalEarned = claimerBounties
      .filter(b => b.status === 'completed')
      .reduce((sum, b) => sum + b.reward_usdc, 0);
    console.log(`Total earned (completed): $${claimerTotalEarned.toLocaleString()} USDC`);
    
    const claimerPending = claimerBounties
      .filter(b => ['claimed', 'submitted'].includes(b.status))
      .reduce((sum, b) => sum + b.reward_usdc, 0);
    console.log(`Pending rewards: $${claimerPending.toLocaleString()} USDC\n`);

    // Get recent activity (bounties updated in last 7 days)
    console.log('=== Recent Activity ===');
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    
    const recentBounties = allBounties.filter(bounty => 
      new Date(bounty.updated_at) > weekAgo
    );
    
    console.log(`Bounties updated in last 7 days: ${recentBounties.length}`);
    recentBounties.slice(0, 5).forEach(bounty => {
      const updatedDate = new Date(bounty.updated_at).toLocaleDateString();
      console.log(`  • ${bounty.title} (${bounty.status}) - ${updatedDate}`);
    });
    console.log('\n');

  } catch (error) {
    console.error('Error in advanced examples:', error);
  }
}

// Execute if running directly
if (require.main === module) {
  advancedExamples();
}
```

## API Reference

### `OwockibotClient`

The main client class for interacting with the owockibot API.

**Constructor:**

```typescript
new OwockibotClient(config?: OwockibotClientConfig)
```

- `config`: Optional configuration object (`OwockibotClientConfig`).

**Methods:**

-   `ping(): Promise<boolean>`
    -   Tests API connectivity. Returns `true` if accessible, `false` otherwise.
-   `getBounties(): Promise<Bounty[]>`
    -   Retrieves all bounties from the bounty board.
-   `getBounty(id: number): Promise<Bounty | null>`
    -   Retrieves a specific bounty by its unique ID. Returns `null` if not found.
-   `getBountiesByStatus(status: BountyStatus): Promise<Bounty[]>`
    -   Retrieves bounties filtered by their status (e.g., `'open'`, `'completed'`).
-   `getOpenBounties(): Promise<Bounty[]>`
    -   Convenience method to get all bounties with `status: 'open'`.
-   `getCompletedBounties(): Promise<Bounty[]>`
    -   Convenience method to get all bounties with `status: 'completed'`.
-   `searchBounties(keyword: string): Promise<Bounty[]>`
    -   Searches bounties by keyword in their title or description.
-   `getBountiesByCreator(creatorAddress: string): Promise<Bounty[]>`
    -   Retrieves bounties created by a specific Ethereum address.
-   `getBountiesByClaimer(claimerAddress: string): Promise<Bounty[]>`
    -   Retrieves bounties claimed by a specific Ethereum address.
-   `getTreasuryStats(): Promise<TreasuryStats>`
    -   Retrieves statistics about the owockibot treasury. Provides fallback mock data if the API endpoint returns 404.
-   `getTokenInfo(): Promise<TokenInfo>`
    -   Retrieves information about the $owockibot token. Provides fallback mock data if the API endpoint returns 404.
-   `getRatioData(): Promise<RatioData>`
    -   Retrieves data for the ratio tracker (speculation vs. fundamentals). Provides fallback mock data if the API endpoint returns 404.
-   `getSwarmStats(): Promise<SwarmStats>`
    -   Retrieves statistics about the owockibot swarm. Provides fallback mock data if the API endpoint returns 404.
-   `getBaseUrl(): string`
    -   Returns the base URL configured for the API client.

### Models

-   `Bounty`
    ```typescript
    interface Bounty {
      id: number;
      title: string;
      description: string;
      reward_usdc: number;
      status: BountyStatus;
      creator_address: string;
      claimer_address: string | null;
      submission_url: string | null;
      feedback: string | null;
      comments: BountyComment[];
      created_at: string;
      updated_at: string;
    }
    ```
-   `BountyComment`
    ```typescript
    interface BountyComment {
      text: string;
      author: string;
      created_at: string;
    }
    ```
-   `BountyStatus`: `type BountyStatus = 'open' | 'claimed' | 'submitted' | 'completed' | 'cancelled';`
-   `TreasuryStats`
    ```typescript
    interface TreasuryStats {
      treasury_value: number;
      eth_balance: number;
      usdc_balance: number;
      market_cap: number;
      mcap_to_treasury: number;
    }
    ```
-   `TokenInfo`
    ```typescript
    interface TokenInfo {
      symbol: string;
      total_supply: number;
      market_cap: number;
      price: number;
      contract_address: string;
      chain_id: number;
    }
    ```
-   `RatioData`
    ```typescript
    interface RatioData {
      token: { total_supply: number; market_cap: number; };
      treasury: { value: number; mcap_to_treasury_ratio: number; };
      app_usage: { volume: number; mcap_to_volume_ratio: number; };
      attention: { twitter_views: number; mcap_to_views_ratio: number; website_pageviews: number; mcap_to_pageviews_ratio: number; };
    }
    ```
-   `SwarmStats`
    ```typescript
    interface SwarmStats {
      agent_count: number;
      mechanisms_count: number;
      open_bounties: number;
      total_paid_usdc: number;
      total_volume: number;
    }
    ```
-   `OwockibotClientConfig`
    ```typescript
    interface OwockibotClientConfig {
      baseUrl?: string; // Default: 'https://www.owockibot.xyz/api'
      timeout?: number; // Default: 10000ms
      headers?: Record<string, string>;
    }
    ```
-   `ApiError`
    ```typescript
    interface ApiError {
      message: string;
      code?: string;
      status?: number;
    }
    ```

### Error Handling

The `OwockibotClient` uses Axios interceptors to catch and standardize API errors. All API methods will `throw` an `ApiError` object on failure, containing a `message`, optional HTTP `status` code, and optional error `code`.

```typescript
import { OwockibotClient, ApiError } from '@owockibot/sdk';

const client = new OwockibotClient();

try {
  // Attempt an operation that might fail
  const nonExistentBounty = await client.getBounty(99999);
  if (!nonExistentBounty) {
    console.log('Bounty not found (expected behavior for non-existent ID)');
  }
} catch (error) {
  if (error instanceof ApiError) {
    console.error(`API Error - Status: ${error.status}, Message: ${error.message}`);
  } else {
    console.error('An unexpected error occurred:', error);
  }
}
```

## Development

To set up the project for development:

```bash
# Clone the repository
git clone https://github.com/heen-ai/owockibot-sdk.git
cd owockibot-sdk

# Install dependencies
npm install

# Run tests
npm test

# Build the SDK
npm run build

# Run basic examples
npm run dev
# or
npx ts-node src/examples/basic.ts

# Run advanced examples
npx ts-node src/examples/advanced.ts
```

## License

MIT License - see [LICENSE](LICENSE) file.
