/**
 * Utility function to get the full media URL
 * Handles both development (with Vite proxy) and production (direct backend URL)
 */
export function getMediaUrl(imagePath: string | null | undefined): string {
  if (!imagePath) {
    return '/placeholder-image.jpg'; // Fallback image
  }

  // If it's already a full URL, return as is
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    return imagePath;
  }

  // Get the media base URL from environment variables
  const mediaBaseUrl = import.meta.env.VITE_MEDIA_BASE_URL || '';
  
  // Ensure the image path starts with /
  const cleanPath = imagePath.startsWith('/') ? imagePath : `/${imagePath}`;
  
  return `${mediaBaseUrl}${cleanPath}`;
}

/**
 * Get media URL specifically for product images
 */
export function getProductImageUrl(imagePath: string | null | undefined): string {
  return getMediaUrl(imagePath);
}

/**
 * Get media URL specifically for category images
 */
export function getCategoryImageUrl(imagePath: string | null | undefined): string {
  return getMediaUrl(imagePath);
}