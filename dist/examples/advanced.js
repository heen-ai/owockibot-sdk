"use strict";
/**
 * Advanced usage examples for the owockibot SDK
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.advancedExamples = advancedExamples;
exports.formatBounty = formatBounty;
exports.calculateBountyMetrics = calculateBountyMetrics;
const index_1 = require("../index");
async function advancedExamples() {
    const client = new index_1.OwockibotClient();
    console.log('🐝 owockibot SDK Advanced Examples\n');
    try {
        // Example wallet addresses (from actual bounty data)
        const heenalAddress = '0x80370645C98f05Ad86BdF676FaE54afCDBF5BC10';
        const owockibotCreator = '0x26B7805Dd8aEc26DA55fc8e0c659cf6822b740Be';
        console.log('=== Bounty Analysis ===');
        // Get all bounties for analysis
        const allBounties = await client.getBounties();
        console.log(`Total bounties: ${allBounties.length}\n`);
        // Analyze bounties by status
        const statusCounts = allBounties.reduce((acc, bounty) => {
            acc[bounty.status] = (acc[bounty.status] || 0) + 1;
            return acc;
        }, {});
        console.log('Bounties by status:');
        Object.entries(statusCounts).forEach(([status, count]) => {
            console.log(`  ${status}: ${count}`);
        });
        console.log('');
        // Calculate total rewards by status
        const rewardsByStatus = allBounties.reduce((acc, bounty) => {
            acc[bounty.status] = (acc[bounty.status] || 0) + bounty.reward_usdc;
            return acc;
        }, {});
        console.log('Total rewards by status:');
        Object.entries(rewardsByStatus).forEach(([status, total]) => {
            console.log(`  ${status}: $${total.toLocaleString()} USDC`);
        });
        console.log('');
        // Find highest reward bounties
        console.log('Top 5 highest reward bounties:');
        const sortedByReward = [...allBounties]
            .sort((a, b) => b.reward_usdc - a.reward_usdc)
            .slice(0, 5);
        sortedByReward.forEach((bounty, index) => {
            console.log(`  ${index + 1}. ${bounty.title} - $${bounty.reward_usdc} USDC (${bounty.status})`);
        });
        console.log('');
        // Analyze creator activity
        console.log(`=== Creator Analysis: ${owockibotCreator} ===`);
        const creatorBounties = await client.getBountiesByCreator(owockibotCreator);
        console.log(`Created ${creatorBounties.length} bounties`);
        const creatorTotalRewards = creatorBounties.reduce((sum, b) => sum + b.reward_usdc, 0);
        console.log(`Total rewards offered: $${creatorTotalRewards.toLocaleString()} USDC`);
        const avgReward = creatorTotalRewards / creatorBounties.length;
        console.log(`Average reward: $${avgReward.toFixed(2)} USDC\n`);
        // Analyze claimer activity (heenal)
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
        // Search for specific types of bounties
        console.log('=== Bounty Search Examples ===');
        const searchTerms = ['SDK', 'Discord', 'Twitter', 'design', 'video'];
        for (const term of searchTerms) {
            const results = await client.searchBounties(term);
            if (results.length > 0) {
                console.log(`"${term}" bounties (${results.length}):`);
                results.slice(0, 2).forEach(bounty => {
                    console.log(`  • ${bounty.title} - $${bounty.reward_usdc} USDC`);
                });
                console.log('');
            }
        }
        // Get recent activity (bounties updated in last 7 days)
        console.log('=== Recent Activity ===');
        const weekAgo = new Date();
        weekAgo.setDate(weekAgo.getDate() - 7);
        const recentBounties = allBounties.filter(bounty => new Date(bounty.updated_at) > weekAgo);
        console.log(`Bounties updated in last 7 days: ${recentBounties.length}`);
        recentBounties.slice(0, 5).forEach(bounty => {
            const updatedDate = new Date(bounty.updated_at).toLocaleDateString();
            console.log(`  • ${bounty.title} (${bounty.status}) - ${updatedDate}`);
        });
        console.log('');
        // Analyze bounties with comments
        console.log('=== Engagement Analysis ===');
        const bountiesWithComments = allBounties.filter(b => b.comments.length > 0);
        console.log(`Bounties with comments: ${bountiesWithComments.length}`);
        const totalComments = allBounties.reduce((sum, b) => sum + b.comments.length, 0);
        console.log(`Total comments across all bounties: ${totalComments}`);
        if (bountiesWithComments.length > 0) {
            const avgComments = totalComments / bountiesWithComments.length;
            console.log(`Average comments per bounty (that have comments): ${avgComments.toFixed(1)}\n`);
            console.log('Most discussed bounties:');
            const mostDiscussed = [...bountiesWithComments]
                .sort((a, b) => b.comments.length - a.comments.length)
                .slice(0, 3);
            mostDiscussed.forEach(bounty => {
                console.log(`  • ${bounty.title} (${bounty.comments.length} comments)`);
            });
        }
        console.log('\n=== SDK Performance Metrics ===');
        const startTime = Date.now();
        // Test multiple API calls
        const [bounties, treasuryStats, tokenInfo] = await Promise.all([
            client.getBounties(),
            client.getTreasuryStats(),
            client.getTokenInfo()
        ]);
        const endTime = Date.now();
        const responseTime = endTime - startTime;
        console.log(`Concurrent API calls completed in ${responseTime}ms`);
        console.log(`Average response time per call: ${(responseTime / 3).toFixed(0)}ms`);
    }
    catch (error) {
        console.error('Error in advanced examples:', error);
    }
}
// Helper function to format bounty for display
function formatBounty(bounty) {
    const status = bounty.status.toUpperCase();
    const reward = `$${bounty.reward_usdc} USDC`;
    return `[${status}] ${bounty.title} - ${reward}`;
}
// Helper function to calculate bounty metrics
function calculateBountyMetrics(bounties) {
    const total = bounties.length;
    const totalRewards = bounties.reduce((sum, b) => sum + b.reward_usdc, 0);
    const avgReward = total > 0 ? totalRewards / total : 0;
    return {
        total,
        totalRewards,
        avgReward,
        byStatus: bounties.reduce((acc, b) => {
            acc[b.status] = (acc[b.status] || 0) + 1;
            return acc;
        }, {})
    };
}
// Run examples if this file is executed directly
if (require.main === module) {
    advancedExamples();
}
