import asyncio

from decimal import Decimal
from typing import Any, Dict

from tronpy import Tron
from tronpy.providers import HTTPProvider

from app.config import settings


class TronService:

    def __init__(self):
        if settings.tron_network == "mainnet":
            self.tron = Tron()
        else:
            provider = HTTPProvider("https://api.shasta.trongrid.io")
            self.tron = Tron(provider)

    async def get_address_info(self, address: str) -> Dict[str, Any]:
        try:
            account_info = await asyncio.to_thread(self.tron.get_account, address)

            account_resources = await asyncio.to_thread(
                self.tron.get_account_resource, address
            )

            balance_sun = account_info.get("balance", 0)
            trx_balance = Decimal(balance_sun) / Decimal(1_000_000)

            free_net_limit = account_resources.get("freeNetLimit", 0)
            net_limit = account_resources.get("NetLimit", 0)
            free_net_used = account_resources.get("freeNetUsed", 0)
            net_used = account_resources.get("NetUsed", 0)

            bandwidth = free_net_limit + net_limit - free_net_used - net_used
            bandwidth = max(0, bandwidth)

            energy_limit = account_resources.get("EnergyLimit", 0)
            energy_used = account_resources.get("EnergyUsed", 0)
            energy = max(0, energy_limit - energy_used)

            return {
                "bandwidth": bandwidth,
                "energy": energy,
                "trx_balance": trx_balance,
            }

        except Exception as e:
            raise Exception(f"Error getting TRON data: {str(e)}")


tron_service = TronService()
