// Main client export
import { OwockibotClient } from './client';
export { OwockibotClient };

// Type exports
export {
  OwockibotClientConfig,
  Bounty,
  BountyComment,
  BountyStatus,
  TreasuryStats,
  TokenInfo,
  RatioData,
  SwarmStats,
  ApiError,
  NotFoundError,
  ValidationError,
  RateLimitError,
  ServerError
} from './types';

// Re-export for convenience
export default OwockibotClient;