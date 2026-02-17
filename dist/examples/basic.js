"use strict";
/**
 * Basic usage examples for the owockibot SDK
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.basicExamples = basicExamples;
const index_1 = require("../index");
async function basicExamples() {
    // Initialize the client
    const client = new index_1.OwockibotClient();
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
        console.log('');
        // Get completed bounties
        console.log('Fetching completed bounties...');
        const completedBounties = await client.getCompletedBounties();
        console.log(`Found ${completedBounties.length} completed bounties:`);
        completedBounties.slice(0, 3).forEach(bounty => {
            console.log(`  • ${bounty.title} - $${bounty.reward_usdc} USDC`);
        });
        console.log('');
        // Search bounties
        console.log('Searching for SDK-related bounties...');
        const sdkBounties = await client.searchBounties('SDK');
        console.log(`Found ${sdkBounties.length} SDK-related bounties:`);
        sdkBounties.forEach(bounty => {
            console.log(`  • ${bounty.title} - $${bounty.reward_usdc} USDC (${bounty.status})`);
        });
        console.log('');
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
            console.log('');
        }
        // Get treasury stats (may return fallback data)
        console.log('Fetching treasury stats...');
        const treasuryStats = await client.getTreasuryStats();
        console.log(`Treasury Value: $${treasuryStats.treasury_value.toLocaleString()}`);
        console.log(`Market Cap: $${treasuryStats.market_cap.toLocaleString()}`);
        console.log(`Mcap/Treasury Ratio: ${treasuryStats.mcap_to_treasury.toFixed(1)}x\n`);
        // Get token info (may return fallback data)
        console.log('Fetching token info...');
        const tokenInfo = await client.getTokenInfo();
        console.log(`Symbol: ${tokenInfo.symbol}`);
        console.log(`Total Supply: ${tokenInfo.total_supply.toLocaleString()}`);
        console.log(`Market Cap: $${tokenInfo.market_cap.toLocaleString()}`);
        console.log(`Contract: ${tokenInfo.contract_address}\n`);
        // Get swarm stats (may return fallback data)
        console.log('Fetching swarm stats...');
        const swarmStats = await client.getSwarmStats();
        console.log(`Agents: ${swarmStats.agent_count}`);
        console.log(`Mechanisms: ${swarmStats.mechanisms_count}`);
        console.log(`Open Bounties: ${swarmStats.open_bounties}`);
        console.log(`Total Paid: $${swarmStats.total_paid_usdc.toLocaleString()} USDC`);
        console.log(`Total Volume: $${swarmStats.total_volume.toLocaleString()}\n`);
        // Get ratio data (may return fallback data)
        console.log('Fetching ratio data (Speculation vs Fundamentals)...');
        const ratioData = await client.getRatioData();
        console.log(`Market Cap: $${ratioData.token.market_cap.toLocaleString()}`);
        console.log(`Treasury Value: $${ratioData.treasury.value.toLocaleString()}`);
        console.log(`Mcap/Treasury: ${ratioData.treasury.mcap_to_treasury_ratio.toFixed(1)}x`);
        console.log(`App Volume: $${ratioData.app_usage.volume.toLocaleString()}`);
        console.log(`Mcap/Volume: ${ratioData.app_usage.mcap_to_volume_ratio.toFixed(1)}x\n`);
    }
    catch (error) {
        console.error('Error running examples:', error);
    }
}
// Run examples if this file is executed directly
if (require.main === module) {
    basicExamples();
}
