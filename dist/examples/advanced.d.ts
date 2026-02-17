/**
 * Advanced usage examples for the owockibot SDK
 */
import { Bounty } from '../index';
declare function advancedExamples(): Promise<void>;
declare function formatBounty(bounty: Bounty): string;
declare function calculateBountyMetrics(bounties: Bounty[]): {
    total: number;
    totalRewards: number;
    avgReward: number;
    byStatus: Record<string, number>;
};
export { advancedExamples, formatBounty, calculateBountyMetrics };
