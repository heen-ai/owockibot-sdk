import { OwockibotClientConfig, Bounty, TreasuryStats, TokenInfo, RatioData, SwarmStats, BountyStatus } from './types';
/**
 * Main client for interacting with owockibot APIs
 */
export declare class OwockibotClient {
    private readonly http;
    private readonly baseUrl;
    constructor(config?: OwockibotClientConfig);
    /**
     * Get all bounties from the bounty board
     */
    getBounties(): Promise<Bounty[]>;
    /**
     * Get a specific bounty by ID
     */
    getBounty(id: number): Promise<Bounty | null>;
    /**
     * Get bounties by status
     */
    getBountiesByStatus(status: BountyStatus): Promise<Bounty[]>;
    /**
     * Get open bounties (convenience method)
     */
    getOpenBounties(): Promise<Bounty[]>;
    /**
     * Get completed bounties (convenience method)
     */
    getCompletedBounties(): Promise<Bounty[]>;
    /**
     * Search bounties by keyword in title or description
     */
    searchBounties(keyword: string): Promise<Bounty[]>;
    /**
     * Get bounties by creator address
     */
    getBountiesByCreator(creatorAddress: string): Promise<Bounty[]>;
    /**
     * Get bounties claimed by address
     */
    getBountiesByClaimer(claimerAddress: string): Promise<Bounty[]>;
    /**
     * Get treasury statistics
     * @note This endpoint may not be publicly available yet
     */
    getTreasuryStats(): Promise<TreasuryStats>;
    /**
     * Get token information
     * @note This endpoint may not be publicly available yet
     */
    getTokenInfo(): Promise<TokenInfo>;
    /**
     * Get ratio tracker data (speculation vs fundamentals)
     * @note This endpoint may not be publicly available yet
     */
    getRatioData(): Promise<RatioData>;
    /**
     * Get swarm statistics
     * @note This endpoint may not be publicly available yet
     */
    getSwarmStats(): Promise<SwarmStats>;
    /**
     * Test API connectivity
     */
    ping(): Promise<boolean>;
    /**
     * Get API base URL
     */
    getBaseUrl(): string;
}
