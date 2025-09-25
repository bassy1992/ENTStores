import requests
import json
from decimal import Decimal
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class CurrencyConverter:
    """Service for converting USD to GHS for MoMo payments"""
    
    # Fallback exchange rate if API fails (updated periodically)
    FALLBACK_USD_TO_GHS = Decimal('12.50')  # Approximate rate as of 2024
    
    # Cache key for exchange rates
    CACHE_KEY = 'usd_to_ghs_rate'
    CACHE_DURATION = 3600  # 1 hour
    
    @classmethod
    def get_usd_to_ghs_rate(cls):
        """Get current USD to GHS exchange rate"""
        
        # Try to get from cache first
        cached_rate = cache.get(cls.CACHE_KEY)
        if cached_rate:
            logger.info(f"Using cached USD to GHS rate: {cached_rate}")
            return Decimal(str(cached_rate))
        
        # Try multiple exchange rate APIs
        rate = cls._fetch_from_exchangerate_api() or \
               cls._fetch_from_fixer_api() or \
               cls._fetch_from_currencyapi() or \
               cls.FALLBACK_USD_TO_GHS
        
        # Cache the rate
        cache.set(cls.CACHE_KEY, float(rate), cls.CACHE_DURATION)
        logger.info(f"Fetched and cached USD to GHS rate: {rate}")
        
        return rate
    
    @classmethod
    def _fetch_from_exchangerate_api(cls):
        """Fetch rate from exchangerate-api.com (free tier)"""
        try:
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                ghs_rate = data.get('rates', {}).get('GHS')
                
                if ghs_rate:
                    logger.info(f"ExchangeRate-API USD to GHS: {ghs_rate}")
                    return Decimal(str(ghs_rate))
                    
        except Exception as e:
            logger.warning(f"ExchangeRate-API failed: {e}")
        
        return None
    
    @classmethod
    def _fetch_from_fixer_api(cls):
        """Fetch rate from fixer.io (requires API key)"""
        api_key = getattr(settings, 'FIXER_API_KEY', None)
        if not api_key:
            return None
            
        try:
            url = f"http://data.fixer.io/api/latest?access_key={api_key}&base=USD&symbols=GHS"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    ghs_rate = data.get('rates', {}).get('GHS')
                    if ghs_rate:
                        logger.info(f"Fixer.io USD to GHS: {ghs_rate}")
                        return Decimal(str(ghs_rate))
                        
        except Exception as e:
            logger.warning(f"Fixer.io API failed: {e}")
        
        return None
    
    @classmethod
    def _fetch_from_currencyapi(cls):
        """Fetch rate from currencyapi.com (free tier)"""
        api_key = getattr(settings, 'CURRENCY_API_KEY', None)
        if not api_key:
            return None
            
        try:
            url = f"https://api.currencyapi.com/v3/latest?apikey={api_key}&base_currency=USD&currencies=GHS"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                ghs_data = data.get('data', {}).get('GHS')
                
                if ghs_data:
                    ghs_rate = ghs_data.get('value')
                    if ghs_rate:
                        logger.info(f"CurrencyAPI USD to GHS: {ghs_rate}")
                        return Decimal(str(ghs_rate))
                        
        except Exception as e:
            logger.warning(f"CurrencyAPI failed: {e}")
        
        return None
    
    @classmethod
    def convert_usd_to_ghs(cls, usd_amount_dollars):
        """
        Convert USD amount in dollars to GHS amount in pesewas
        
        Args:
            usd_amount_dollars (float/Decimal): Amount in USD dollars (e.g., 25.00 = $25.00)
            
        Returns:
            dict: {
                'ghs_amount_pesewas': int,  # Amount in pesewas (100 pesewas = 1 GHS)
                'ghs_amount_display': str,  # Formatted amount (e.g., "GH₵ 312.50")
                'usd_amount_display': str,  # Original USD amount (e.g., "$25.00")
                'exchange_rate': float,     # Exchange rate used
                'rate_source': str         # Source of exchange rate
            }
        """
        
        # Get current exchange rate
        rate = cls.get_usd_to_ghs_rate()
        
        # Convert to Decimal for precise calculation
        usd_dollars = Decimal(str(usd_amount_dollars))
        
        # Convert to GHS
        ghs_amount = usd_dollars * rate
        
        # Convert to pesewas (GHS cents)
        ghs_pesewas = int(ghs_amount * 100)
        
        # Determine rate source
        cached_rate = cache.get(cls.CACHE_KEY)
        rate_source = "cached" if cached_rate else "live_api"
        if rate == cls.FALLBACK_USD_TO_GHS:
            rate_source = "fallback"
        
        return {
            'ghs_amount_pesewas': ghs_pesewas,
            'ghs_amount_display': f"GH₵ {ghs_amount:.2f}",
            'usd_amount_display': f"${usd_dollars:.2f}",
            'exchange_rate': float(rate),
            'rate_source': rate_source,
            'conversion_note': f"1 USD = {rate:.4f} GHS"
        }
    
    @classmethod
    def get_rate_info(cls):
        """Get current rate information for display"""
        rate = cls.get_usd_to_ghs_rate()
        cached_rate = cache.get(cls.CACHE_KEY)
        
        return {
            'rate': float(rate),
            'display': f"1 USD = {rate:.4f} GHS",
            'is_cached': bool(cached_rate),
            'is_fallback': rate == cls.FALLBACK_USD_TO_GHS,
            'cache_duration': cls.CACHE_DURATION
        }


# Convenience functions
def convert_usd_to_ghs(usd_dollars):
    """Convert USD dollars to GHS pesewas"""
    return CurrencyConverter.convert_usd_to_ghs(usd_dollars)

def get_current_exchange_rate():
    """Get current USD to GHS exchange rate"""
    return CurrencyConverter.get_usd_to_ghs_rate()

def get_rate_display():
    """Get formatted exchange rate for display"""
    return CurrencyConverter.get_rate_info()