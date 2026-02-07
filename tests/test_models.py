"""Tests for data models."""

from decimal import Decimal
from datetime import datetime

import pytest

from owockibot.models import (
    Bounty,
    BountyStatus,
    Stats,
    Submission,
    Payment,
    PendingPayment,
    X402Config,
    TokenConfig,
)


class TestBountyStatus:
    """Test the BountyStatus enum."""
    
    def test_enum_values(self):
        """Test that all expected statuses exist."""
        assert BountyStatus.OPEN == "open"
        assert BountyStatus.CLAIMED == "claimed"
        assert BountyStatus.SUBMITTED == "submitted"
        assert BountyStatus.COMPLETED == "completed"
        assert BountyStatus.CANCELLED == "cancelled"
        assert BountyStatus.PAYMENT_FAILED == "payment_failed"


class TestSubmission:
    """Test the Submission model."""
    
    def test_from_dict(self):
        """Test creating Submission from dict."""
        data = {
            "id": "test-id",
            "proof": "https://github.com/test",
            "content": "Completed the task",
            "submittedAt": 1770441177949
        }
        
        submission = Submission.from_dict(data)
        
        assert submission.id == "test-id"
        assert submission.proof == "https://github.com/test"
        assert submission.content == "Completed the task"
        assert isinstance(submission.submitted_at, datetime)
    
    def test_from_dict_no_proof(self):
        """Test creating Submission without proof."""
        data = {
            "id": "test-id",
            "proof": None,
            "content": "Completed",
            "submittedAt": 1770441177949
        }
        
        submission = Submission.from_dict(data)
        assert submission.proof is None


class TestPayment:
    """Test the Payment model."""
    
    def test_from_dict(self):
        """Test creating Payment from dict."""
        data = {
            "fee": 28650000,
            "chain": "base",
            "token": "USDC",
            "txHash": "0xabc123",
            "netReward": 544350000,
            "grossReward": 573000000,
            "processedAt": "2026-02-07T05:13:27.394Z",
            "processedBy": "payment-relay",
            "feePercent": "5%",
            "feeFormatted": "28.65 USDC",
            "netRewardFormatted": "544.35 USDC"
        }
        
        payment = Payment.from_dict(data)
        
        assert payment.fee == 28650000
        assert payment.chain == "base"
        assert payment.tx_hash == "0xabc123"
        assert payment.fee_usdc == Decimal("28.65")
        assert payment.net_reward_usdc == Decimal("544.35")
        assert payment.gross_reward_usdc == Decimal("573.00")


class TestPendingPayment:
    """Test the PendingPayment model."""
    
    def test_usdc_conversions(self):
        """Test micro-USDC to USDC conversions."""
        data = {
            "fee": 1500000,
            "chain": "base",
            "token": "USDC",
            "netReward": 28500000,
            "grossReward": 30000000,
            "recipient": "0x123"
        }
        
        payment = PendingPayment.from_dict(data)
        
        assert payment.fee_usdc == Decimal("1.5")
        assert payment.net_reward_usdc == Decimal("28.5")
        assert payment.gross_reward_usdc == Decimal("30.0")


class TestBounty:
    """Test the Bounty model."""
    
    def test_from_dict_open_bounty(self, sample_bounty_data):
        """Test creating an open bounty from dict."""
        bounty = Bounty.from_dict(sample_bounty_data)
        
        assert bounty.id == "143"
        assert bounty.title == "Write AI Agent Negotiation Simulation"
        assert bounty.reward == 20000000
        assert bounty.reward_usdc == Decimal("20.00")
        assert bounty.reward_formatted == "20.00 USDC"
        assert bounty.status == BountyStatus.OPEN
        assert bounty.is_open is True
        assert bounty.is_completed is False
        assert bounty.claimed_by is None
        assert len(bounty.tags) == 4
        assert "coding" in bounty.tags
    
    def test_from_dict_completed_bounty(self, sample_completed_bounty_data):
        """Test creating a completed bounty with payment."""
        bounty = Bounty.from_dict(sample_completed_bounty_data)
        
        assert bounty.id == "108"
        assert bounty.status == BountyStatus.COMPLETED
        assert bounty.is_completed is True
        assert bounty.claimed_by == "0xa85bf3202d9716f2dd263ed3de090d350f0822e4"
        assert bounty.payment is not None
        assert bounty.payment.tx_hash is not None
        assert len(bounty.submissions) == 1
    
    def test_reward_usdc_conversion(self, sample_bounty_data):
        """Test reward conversion from micro-USDC."""
        bounty = Bounty.from_dict(sample_bounty_data)
        
        # 20000000 micro-USDC = 20.00 USDC
        assert bounty.reward_usdc == Decimal("20.00")
    
    def test_bounty_status_helpers(self, sample_bounty_data, sample_completed_bounty_data):
        """Test status helper properties."""
        open_bounty = Bounty.from_dict(sample_bounty_data)
        completed_bounty = Bounty.from_dict(sample_completed_bounty_data)
        
        assert open_bounty.is_open is True
        assert open_bounty.is_claimed is False
        assert open_bounty.is_completed is False
        
        assert completed_bounty.is_open is False
        assert completed_bounty.is_completed is True


class TestStats:
    """Test the Stats model."""
    
    def test_from_dict(self, sample_stats_data):
        """Test creating Stats from dict."""
        stats = Stats.from_dict(sample_stats_data)
        
        assert stats.total_bounties == 137
        assert stats.open_bounties == 21
        assert stats.completed_bounties == 34
        assert stats.total_rewards_usdc == 1912.61
        assert stats.total_agents == 11
        assert stats.db_connected is True
    
    def test_completion_rate(self, sample_stats_data):
        """Test completion rate calculation."""
        stats = Stats.from_dict(sample_stats_data)
        
        # 34 / 137 * 100 = ~24.82%
        expected_rate = (34 / 137) * 100
        assert stats.completion_rate == pytest.approx(expected_rate)
    
    def test_average_reward(self, sample_stats_data):
        """Test average reward calculation."""
        stats = Stats.from_dict(sample_stats_data)
        
        # 1912.61 / 34 = ~56.25
        expected_avg = 1912.61 / 34
        assert stats.average_reward_usdc == pytest.approx(expected_avg)
    
    def test_zero_division_protection(self):
        """Test handling of zero values."""
        data = {
            "totalBounties": 0,
            "openBounties": 0,
            "completedBounties": 0,
            "totalRewardsUSDC": 0,
            "totalAgents": 0,
            "dbConnected": True
        }
        stats = Stats.from_dict(data)
        
        assert stats.completion_rate == 0.0
        assert stats.average_reward_usdc == 0.0


class TestX402Config:
    """Test the X402Config model."""
    
    def test_from_dict(self, sample_x402_config_data):
        """Test creating X402Config from dict."""
        config = X402Config.from_dict(sample_x402_config_data)
        
        assert config.version == "1.0"
        assert config.network == "base"
        assert config.chain_id == 8453
        assert config.facilitator == "https://x402.org/facilitator"
        assert config.treasury == "0xccD7200024A8B5708d381168ec2dB0DC587af83F"
        assert len(config.accepts) == 1
    
    def test_token_config(self, sample_x402_config_data):
        """Test TokenConfig parsing."""
        config = X402Config.from_dict(sample_x402_config_data)
        token = config.accepts[0]
        
        assert token.network == "base"
        assert token.token == "USDC"
        assert token.address == "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
        assert token.min_amount == "100000"
