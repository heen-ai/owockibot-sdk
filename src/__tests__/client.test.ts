import { OwockibotClient } from '../client';
import { Bounty } from '../types';
import axios from 'axios';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('OwockibotClient', () => {
  let client: OwockibotClient;
  
  beforeEach(() => {
    client = new OwockibotClient();
    // Reset all mocks
    jest.clearAllMocks();
    
    // Mock axios.create to return a mock instance
    const mockAxiosInstance = {
      get: jest.fn(),
      post: jest.fn(),
      put: jest.fn(),
      delete: jest.fn(),
      interceptors: {
        response: {
          use: jest.fn()
        }
      }
    };
    
    mockedAxios.create.mockReturnValue(mockAxiosInstance as any);
  });

  describe('constructor', () => {
    it('should create client with default config', () => {
      const client = new OwockibotClient();
      expect(client.getBaseUrl()).toBe('https://www.owockibot.xyz/api');
    });

    it('should create client with custom config', () => {
      const config = {
        baseUrl: 'https://custom.api.com',
        timeout: 5000,
        headers: { 'Custom-Header': 'value' }
      };
      const client = new OwockibotClient(config);
      expect(client.getBaseUrl()).toBe('https://custom.api.com');
    });
  });

  describe('getBounties', () => {
    it('should fetch bounties successfully', async () => {
      const mockBounties: Bounty[] = [
        {
          id: 1,
          title: 'Test Bounty',
          description: 'Test Description',
          reward_usdc: 100,
          status: 'open',
          creator_address: '0x123',
          claimer_address: null,
          submission_url: null,
          feedback: null,
          comments: [],
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z'
        }
      ];

      // Mock the HTTP client's get method
      (client as any).http.get = jest.fn().mockResolvedValue({
        data: mockBounties
      });

      const result = await client.getBounties();
      expect(result).toEqual(mockBounties);
      expect((client as any).http.get).toHaveBeenCalledWith('/bounty-board');
    });
  });

  describe('getBounty', () => {
    it('should fetch specific bounty by ID', async () => {
      const mockBounties: Bounty[] = [
        {
          id: 1,
          title: 'Test Bounty 1',
          description: 'Test Description 1',
          reward_usdc: 100,
          status: 'open',
          creator_address: '0x123',
          claimer_address: null,
          submission_url: null,
          feedback: null,
          comments: [],
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z'
        },
        {
          id: 2,
          title: 'Test Bounty 2',
          description: 'Test Description 2',
          reward_usdc: 200,
          status: 'completed',
          creator_address: '0x456',
          claimer_address: '0x789',
          submission_url: 'https://example.com',
          feedback: 'Great work!',
          comments: [],
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-02T00:00:00Z'
        }
      ];

      (client as any).http.get = jest.fn().mockResolvedValue({
        data: mockBounties
      });

      const result = await client.getBounty(2);
      expect(result).toEqual(mockBounties[1]);
    });

    it('should return null for non-existent bounty', async () => {
      (client as any).http.get = jest.fn().mockResolvedValue({
        data: []
      });

      const result = await client.getBounty(999);
      expect(result).toBeNull();
    });
  });

  describe('getOpenBounties', () => {
    it('should filter bounties by open status', async () => {
      const mockBounties: Bounty[] = [
        {
          id: 1,
          title: 'Open Bounty',
          description: 'Description',
          reward_usdc: 100,
          status: 'open',
          creator_address: '0x123',
          claimer_address: null,
          submission_url: null,
          feedback: null,
          comments: [],
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z'
        },
        {
          id: 2,
          title: 'Completed Bounty',
          description: 'Description',
          reward_usdc: 200,
          status: 'completed',
          creator_address: '0x456',
          claimer_address: '0x789',
          submission_url: 'https://example.com',
          feedback: 'Done!',
          comments: [],
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-02T00:00:00Z'
        }
      ];

      (client as any).http.get = jest.fn().mockResolvedValue({
        data: mockBounties
      });

      const result = await client.getOpenBounties();
      expect(result).toHaveLength(1);
      expect(result[0].status).toBe('open');
    });
  });

  describe('searchBounties', () => {
    it('should search bounties by keyword', async () => {
      const mockBounties: Bounty[] = [
        {
          id: 1,
          title: 'SDK Development',
          description: 'Build a JavaScript SDK',
          reward_usdc: 100,
          status: 'open',
          creator_address: '0x123',
          claimer_address: null,
          submission_url: null,
          feedback: null,
          comments: [],
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z'
        },
        {
          id: 2,
          title: 'Design Logo',
          description: 'Create a logo design',
          reward_usdc: 50,
          status: 'open',
          creator_address: '0x456',
          claimer_address: null,
          submission_url: null,
          feedback: null,
          comments: [],
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z'
        }
      ];

      (client as any).http.get = jest.fn().mockResolvedValue({
        data: mockBounties
      });

      const result = await client.searchBounties('SDK');
      expect(result).toHaveLength(1);
      expect(result[0].title).toContain('SDK');
    });
  });

  describe('ping', () => {
    it('should return true when API is accessible', async () => {
      (client as any).http.get = jest.fn().mockResolvedValue({
        data: []
      });

      const result = await client.ping();
      expect(result).toBe(true);
    });

    it('should return false when API is not accessible', async () => {
      (client as any).http.get = jest.fn().mockRejectedValue(new Error('Network error'));

      const result = await client.ping();
      expect(result).toBe(false);
    });
  });
});