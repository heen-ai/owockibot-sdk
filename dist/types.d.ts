/**
 * Bounty status on the owockibot bounty board
 */
export type BountyStatus = 'open' | 'claimed' | 'submitted' | 'completed' | 'cancelled';
/**
 * A bounty on the owockibot bounty board
 */
export interface Bounty {
    /** Unique ID of the bounty */
    id: number;
    /** Title of the bounty */
    title: string;
    /** Description of the work required */
    description: string;
    /** Reward amount in USDC */
    reward_usdc: number;
    /** Current status of the bounty */
    status: BountyStatus;
    /** Ethereum address of the bounty creator */
    creator_address: string;
    /** Ethereum address of the claimer (if claimed) */
    claimer_address: string | null;
    /** URL of the submitted work (if submitted) */
    submission_url: string | null;
    /** Feedback from the bounty creator */
    feedback: string | null;
    /** Comments on the bounty */
    comments: BountyComment[];
    /** When the bounty was created */
    created_at: string;
    /** When the bounty was last updated */
    updated_at: string;
}
/**
 * A comment on a bounty
 */
export interface BountyComment {
    /** Comment text */
    text: string;
    /** Ethereum address of the commenter */
    author: string;
    /** When the comment was created */
    created_at: string;
}
/**
 * Treasury statistics
 */
export interface TreasuryStats {
    /** Total treasury value in USD */
    treasury_value: number;
    /** ETH balance */
    eth_balance: number;
    /** USDC balance */
    usdc_balance: number;
    /** Market cap */
    market_cap: number;
    /** Market cap to treasury ratio */
    mcap_to_treasury: number;
}
/**
 * Token information
 */
export interface TokenInfo {
    /** Token symbol */
    symbol: string;
    /** Total token supply */
    total_supply: number;
    /** Current market cap */
    market_cap: number;
    /** Current price */
    price: number;
    /** Contract address */
    contract_address: string;
    /** Chain ID */
    chain_id: number;
}
/**
 * Ratio tracker data - speculation vs fundamentals
 */
export interface RatioData {
    /** Token metrics */
    token: {
        total_supply: number;
        market_cap: number;
    };
    /** Treasury metrics */
    treasury: {
        value: number;
        mcap_to_treasury_ratio: number;
    };
    /** Application usage metrics */
    app_usage: {
        volume: number;
        mcap_to_volume_ratio: number;
    };
    /** Attention metrics */
    attention: {
        twitter_views: number;
        mcap_to_views_ratio: number;
        website_pageviews: number;
        mcap_to_pageviews_ratio: number;
    };
}
/**
 * Swarm statistics
 */
export interface SwarmStats {
    /** Number of agents in the swarm */
    agent_count: number;
    /** Number of deployed mechanisms/apps */
    mechanisms_count: number;
    /** Number of open bounties */
    open_bounties: number;
    /** Total USDC paid out in bounties */
    total_paid_usdc: number;
    /** Total volume across apps */
    total_volume: number;
}
/**
 * API client configuration options
 */
export interface OwockibotClientConfig {
    /** Base URL for the API (default: https://www.owockibot.xyz/api) */
    baseUrl?: string;
    /** Request timeout in milliseconds (default: 10000) */
    timeout?: number;
    /** Custom headers to send with requests */
    headers?: Record<string, string>;
}
/**
 * Base class for all owockibot SDK errors
 */
export declare class OwockibotError extends Error {
    constructor(message: string);
}
/**
 * Represents an error response from the API
 */
export declare class ApiError extends OwockibotError {
    status?: number;
    code?: string;
    constructor(message: string, status?: number, code?: string);
}
/**
 * Error for 404 Not Found responses
 */
export declare class NotFoundError extends ApiError {
    constructor(message?: string, code?: string);
}
/**
 * Error for 400 Bad Request / Validation errors
 */
export declare class ValidationError extends ApiError {
    constructor(message?: string, code?: string);
}
/**
 * Error for 429 Rate Limit Exceeded responses
 */
export declare class RateLimitError extends ApiError {
    constructor(message?: string, code?: string);
}
/**
 * Error for 5xx Server errors
 */
export declare class ServerError extends ApiError {
    constructor(message?: string, status?: number, code?: string);
}
/**
 * API response wrapper (re-added for AxiosResponse typing)
 */
export interface ApiResponse<T> {
    data: T;
    status: number;
    statusText: string;
}
