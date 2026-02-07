"""Test fixtures and configuration."""

import pytest


@pytest.fixture
def sample_bounty_data():
    """Sample bounty data from the API."""
    return {
        "id": "143",
        "uuid": "7c590dc7-93f0-4ba7-a2e6-7c430bb29b96",
        "title": "Write AI Agent Negotiation Simulation",
        "description": "Create a simulation showing two AI agents negotiating...",
        "reward": "20000000",
        "rewardFormatted": "20.00 USDC",
        "status": "open",
        "creator": "0xccD7200024A8B5708d381168ec2dB0DC587af83F",
        "deadline": "2026-02-20",
        "claimedBy": None,
        "createdAt": 1770449294859,
        "updatedAt": 1770449294859,
        "tags": ["coding", "simulation", "agents", "coordination"],
        "submissions": [],
        "requirements": [
            "Working negotiation demo",
            "2+ agent interaction",
            "Protocol documentation",
            "Source code"
        ],
    }


@pytest.fixture
def sample_completed_bounty_data():
    """Sample completed bounty with payment data."""
    return {
        "id": "108",
        "uuid": "ab244eb8-a44f-4e68-a907-a68dad4ee04d",
        "title": "Build Farcaster Mini-App for Bounties",
        "description": "Create a Farcaster Frame or mini-app...",
        "reward": "573000000",
        "rewardFormatted": "573.00 USDC",
        "status": "completed",
        "creator": "0xA85bf3202d9716F2dD263ED3dE090D350f0822E4",
        "deadline": 1771045906751,
        "claimedBy": "0xa85bf3202d9716f2dd263ed3de090d350f0822e4",
        "claimedAt": 1770441109598,
        "createdAt": 1770441106751,
        "updatedAt": 1770441207394,
        "approvedAt": 1770441179737,
        "completedAt": 1770441207394,
        "tags": ["coding", "farcaster"],
        "submissions": [
            {
                "id": "12e9eccd-6abd-4468-9bb1-2ef07db781af",
                "proof": None,
                "content": "submitted bounty",
                "submittedAt": 1770441177949
            }
        ],
        "requirements": [],
        "payment": {
            "fee": 28650000,
            "chain": "base",
            "token": "USDC",
            "txHash": "0x5c95e030384679c67b4ebbbcaa78d34683e9db366e53622a3f3ae880792b51a1",
            "netReward": 544350000,
            "feePercent": "5%",
            "grossReward": 573000000,
            "processedAt": "2026-02-07T05:13:27.394Z",
            "processedBy": "payment-relay",
            "feeFormatted": "28.65 USDC",
            "netRewardFormatted": "544.35 USDC"
        }
    }


@pytest.fixture
def sample_stats_data():
    """Sample stats data from the API."""
    return {
        "totalBounties": 137,
        "openBounties": 21,
        "completedBounties": 34,
        "totalRewardsUSDC": 1912.61,
        "totalAgents": 11,
        "dbConnected": True
    }


@pytest.fixture
def sample_x402_config_data():
    """Sample x402 config data."""
    return {
        "version": "1.0",
        "network": "base",
        "chainId": 8453,
        "accepts": [
            {
                "network": "base",
                "token": "USDC",
                "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                "minAmount": "100000"
            }
        ],
        "facilitator": "https://x402.org/facilitator",
        "treasury": "0xccD7200024A8B5708d381168ec2dB0DC587af83F"
    }
