// Countries that require payment processing
export const PAYMENT_REQUIRED_COUNTRIES = [
  'US', // United States
  'GH', // Ghana
  'GB', // United Kingdom
  // European Union countries
  'DE', // Germany
  'FR', // France
  'IT', // Italy
  'ES', // Spain
  'NL', // Netherlands
  'BE', // Belgium
  'CH', // Switzerland
  'AT', // Austria
  'SE', // Sweden
  'NO', // Norway
  'DK', // Denmark
  'FI', // Finland
  'IE', // Ireland
  'PT', // Portugal
  'GR', // Greece
  'PL', // Poland
  'CZ', // Czech Republic
  'HU', // Hungary
  'SK', // Slovakia
  'SI', // Slovenia
  'HR', // Croatia
  'RO', // Romania
  'BG', // Bulgaria
  'EE', // Estonia
  'LV', // Latvia
  'LT', // Lithuania
  'LU', // Luxembourg
  'MT', // Malta
  'CY', // Cyprus
];

/**
 * Check if a country requires payment processing
 * @param countryCode - ISO 2-letter country code
 * @returns true if payment is required, false for free checkout
 */
export const requiresPayment = (countryCode: string): boolean => {
  return PAYMENT_REQUIRED_COUNTRIES.includes(countryCode.toUpperCase());
};

/**
 * Get the checkout flow type for a country
 * @param countryCode - ISO 2-letter country code
 * @returns 'payment' or 'free'
 */
export const getCheckoutFlow = (countryCode: string): 'payment' | 'free' => {
  return requiresPayment(countryCode) ? 'payment' : 'free';
};

/**
 * Get user-friendly message about checkout flow
 * @param countryCode - ISO 2-letter country code
 * @returns message explaining the checkout flow
 */
export const getCheckoutMessage = (countryCode: string): string => {
  if (requiresPayment(countryCode)) {
    return 'Payment required to complete your order';
  }
  return 'No payment required - Your order will be confirmed immediately';
};